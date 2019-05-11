import sys
import time
import redis
import requests
import pika
import json

from threading import Thread
from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3
from web3.middleware import geth_poa_middleware
from solc import compile_source

'''
This script is used to verify all metadata stored in Redis database and in the blockchain
to check if metadata are missing (due to an attack?) or if metatada are corrupted (due to an attack?)
If a difference is found, metadata are sent in a message queue where a script read again metadata
in the blockchain, delete redis entry and push metadata from blockchain to redis
'''

# +--------------------------------------------------------------+
# | INITIALIZATION REDIS                                         |
# +--------------------------------------------------------------+
host="cluster_metadata"
port=6379
pool = redis.ConnectionPool(host=host,
                                        port=port,
                                        db=0,
                                        max_connections=128,
                                        socket_keepalive=True)
redis = redis.StrictRedis(connection_pool=pool,
                                       encoding=None,
                                       socket_keepalive=True)

# ****************************************
# *                                      *
# *   INITIALISATION RABBITMQ            *
# *                                      *
# ****************************************
# Account
credentials = pika.PlainCredentials('client_rebuild', 'client_rebuild')
# RabbitMQ server
parameters = pika.ConnectionParameters("cluster_rabbitmq_server", 5672, 'vhost_rebuild', credentials)
# Connection
connection = pika.BlockingConnection(parameters)
# Start channel
channel = connection.channel()
channel.queue_declare(queue='rebuild')

# +--------------------------------------------------------------+
# |                FUNCTIONS FOR THE BLOCKCHAIN                  |
# +--------------------------------------------------------------+

def split_ip_adress():
  ip_address_node_container="http://cluster_node1:1234/serveur.html"
  ip_response = requests.get(ip_address_node_container)
  ip = ip_response.text
  ip = ip.split(" ")
  print(ip)
  if(ip[0][0:4] == "10.0"):
    return "http://"+ip[0]+":8001"
  elif(ip[1][0:4] == "10.0"):
    return "http://"+ip[1]+":8001"
  else:
    return "http://"+ip[2]+":8001"


# Compile the contract
def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()

   return compile_source(source)

# Wait the result of the transaction from script to smart contract
def wait_for_receipt(w3, tx_hash, poll_interval):
   while True:
       tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
       if tx_receipt:
         return tx_receipt
       time.sleep(poll_interval)


# +--------------------------------------------------------------+
# |        INITIALISATION OF THE BLOCKCHAIN AND ACCOUNT          |
# +--------------------------------------------------------------+
ip_adress_final = split_ip_adress()
my_provider = Web3.HTTPProvider(ip_adress_final)
w3 = Web3(my_provider)
w3.middleware_stack.inject(geth_poa_middleware, layer=0)
w3.eth.defaultAccount = w3.eth.accounts[0]


# Compilation of the contract
contract_source_path = 'contrat.sol'
compiled_sol = compile_source_file('contrat.sol')
contract_id, contract_interface = compiled_sol.popitem()
store_var_contract = w3.eth.contract(
   address="0x4831CB4ebD5a3504030a379d36e07d014b05C389",
   abi=contract_interface['abi'])

def convert_binary_to_hex_digest(binary_digest):
    """
    Converts a binary digest from hashlib.sha256.digest
    Args:
        binary_digest(str): Binary digest from hashlib.sha256.digest()
    Returns:
        str: Equivalent of the hexdigest for the same input
    """
    return "".join(["{:02x}".format(ord(c)) for c in binary_digest])

def convert_redis_metablock_responses(result):
  metadata_redis = {}
  try:
      metadata_redis['key'] = result[b'key'].decode('utf-8')
  except KeyError:
      metadata_redis['key'] = ""
  try:
      metadata_redis['creation_date'] = result[b'creation_date'].decode('utf-8')
  except KeyError:
      metadata_redis['creation_date'] = ""
  try:
      metadata_redis['providers'] = result[b'providers'].decode('utf-8')
  except KeyError:
      metadata_redis['providers'] = "0"
  try:
      metadata_redis['block_type'] = result[b'block_type'].decode('utf-8')
  except KeyError:
      metadata_redis['block_type'] = ""
  try:
      checksum_temp = result[b'checksum'].decode('latin-1')
      metadata_redis['checksum'] = convert_binary_to_hex_digest(checksum_temp)
      metadata_redis['checksum_new'] = checksum_temp
  except KeyError:
      metadata_redis['checksum'] = ""
      metadata_redis['checksum_new'] = ""
  try:
      metadata_redis['size'] = result[b'size'].decode('utf-8')
  except KeyError:
      metadata_redis['size'] = "0"
  try:
      metadata_redis['entangled_with'] = result[b'entangled_with'].decode('utf-8')
  except KeyError:
      metadata_redis['entangled_with'] = ""
  return metadata_redis


def convert_redis_metadoc_responses(result):
  metadata_redis = {}
  try:
      metadata_redis['path'] = result[b'path'].decode('utf-8')
  except KeyError:
      metadata_redis['path'] = ""
  try: 
      metadata_redis['creation_date'] = result[b'creation_date'].decode('utf-8')
  except KeyError:
      metadata_redis['creation_date'] = ""
  try:
      metadata_redis['blocks'] = result[b'blocks'].decode('utf-8')
  except KeyError:
      metadata_redis['blocks'] = ""
  try:
      metadata_redis['original_size'] = result[b'original_size'].decode('utf-8')
  except KeyError:
      metadata_redis['original_size'] = ""
  try:
      metadata_redis['entangling_blocks'] = result[b'entangling_blocks'].decode('utf-8')
  except KeyError:
      metadata_redis['entangling_blocks'] = ""
  return metadata_redis

def convert_redis_index(result):

  decoded_list = []
  for key in result:
    decoded_list.append(key.decode('utf-8'))

  return decoded_list

# +--------------------------------------------------------------+
# |        					SCRIPT        					                     |
# +--------------------------------------------------------------+

audit_number = 50
missing_entries = 0
bad_entries = 0
corrupted_entries = 0

# +--------------------------------------------------------------+
# Snapshot                                                       |
# +--------------------------------------------------------------+
time_begin = redis.time()
# Get metablock from Redis
all_metadata_metablock_entries = redis.zrange("block_index",0,-1)
all_decoded_metablock_metadata = convert_redis_index(all_metadata_metablock_entries)
# Get metablock from Redis
all_metadata_metadoc_entries = redis.zrange("file_index",0,-1)
all_decoded_metadoc_metadata = convert_redis_index(all_metadata_metadoc_entries)
# Get number metablock in blockchain
nb_metablock = store_var_contract.functions.getNumberMetablock().call()
# Get number metadoc in blockchain
nb_metadoc = store_var_contract.functions.getNumberMetadoc().call()
# Stats
fichier = open("save_check_corruption.txt", "a")

print("\n")
print("*********************************************************************")
print("AUDIT CONFIGURATION")
print("*********************************************************************")
print("This audit will check if there are missing entries, corrupted entries or bad entries.")
print("It will check "+str(nb_metablock+nb_metadoc)+" entries in the blockchain")
print("and "+str(len(all_decoded_metablock_metadata)+len(all_decoded_metadoc_metadata))+" in Redis database.")
print("Audit number: "+ str(audit_number))
print("Started at: "+str(time_begin[0])+"."+str(time_begin[1]))

# +--------------------------------------------------------------+
# METADATA FROM BLOCKCHAIN = SAME ENTRIES ON REDIS?              |
# +--------------------------------------------------------------+

# Check for metablock first
print("\n")
print("*********************************************************************")
print("Check all metablock metadata stored in blockchain with Redis database")
print("*********************************************************************")

metablock_corrupted = []
cpt = 0
while(cpt < nb_metablock):
    iter_start = time.time()
    # Get metadata in blockchain
    metablock = store_var_contract.functions.getFromListMetablock(cpt).call()
    #metablock[0] = key
    #metablock[1] = creation_date
    #metablock[2] = providers
    #metablock[3] = block_type
    #metablock[4] = checksum
    #metablock[5] = size
    #metablock[6] = entangled_with
    if(metablock[5] == 0):
        break;
    print("Check metablock "+metablock[0])
    #Convert uint type from blockchain to string for block type
    if(metablock[3] == 1):
        metablock[3] = "DATA"
    else:
        metablock[3] = "PARITY"
    #Delete double quote added by transaction return
    metablock[2] = metablock[2].replace('"','')

    # Get metadata in Redis
    metablock_redis = redis.hgetall("blocks:"+metablock[0])
    if(not(metablock_redis)):
      #Not exists in Redis ==> Entry deleted in Redis during an attack?
      channel.basic_publish(exchange='', routing_key='rebuild', body=json.dumps("blocks:"+metablock[0]))
      print("-- Entry doesn't exist in Redis. Sent to rebuild script")
      missing_entries = missing_entries + 1
      try:
        all_decoded_metablock_metadata.remove(metablock[0])
      except ValueError:
        pass

      cpt=cpt+1
      continue

    metablock_redis = convert_redis_metablock_responses(metablock_redis)

    # Compare
    error_detected = 0
    #Key
    if(metablock[0] != metablock_redis['key']):
      print("-- Error for key ")
      print("---- Values: "+ str(metablock[0])+" != "+str(metablock_redis['key']))
      error_detected = error_detected + 1
    #Creation_date
    if(metablock[1] != metablock_redis['creation_date']):
      print("-- Error for creation_date ")
      print("---- Values: "+ str(metablock[1])+" != "+str(metablock_redis['creation_date']))
      error_detected = error_detected + 1
    #Providers
    if(metablock[2] != metablock_redis['providers']):
      print("-- Error for providers ")
      print("---- Values: "+ str(metablock[2])+" != "+str(metablock_redis['providers']))
      error_detected = error_detected + 1
    #Block type
    if(metablock[3] != metablock_redis['block_type']):
      print("-- Error for block type ")
      print("---- Values: "+ str(metablock[3])+" != "+str(metablock_redis['block_type']))
      error_detected = error_detected + 1
    #Checksum
    if(metablock[4] != metablock_redis['checksum']):
      if(metablock[4] != metablock_redis['checksum_new']):
        print("-- Error for checksum ")
        error_detected = error_detected + 1
    #Size
    if(int(metablock[5]) != int(metablock_redis['size'])):
      print("-- Error for size ")
      print("---- Values: "+ str(metablock[5])+" != "+str(metablock_redis['size']))
      error_detected = error_detected + 1
    #Entangled_with
    # -- Ignored
    
    if(error_detected != 0):
      print("-- Error detected: "+ str(error_detected))
      metablock_corrupted.append(metablock[0])
      corrupted_entries = corrupted_entries + 1
      all_decoded_metablock_metadata.remove(metablock[0])
      channel.basic_publish(exchange='', routing_key='rebuild', body=json.dumps("blocks:"+metablock[0]))
    else:
      redis.hset("blocks:{:s}".format(metablock[0]), "audit", audit_number)
      #time_redis = redis.time()
    #Write stats in file
    iter_stop = time.time()
    iter_delta = iter_stop - iter_start
    fichier.write("blocks:"+metablock[0]+" "+str(iter_stop)+" "+str(iter_delta)+"\n")
    cpt=cpt+1



print("\n")
# Check for metadoc in a second time
print("*********************************************************************")
print("Check all metadoc metadata stored in blockchain with Redis database  ")
print("*********************************************************************")

metadoc_corrupted = []
cpt = 0
while(cpt < nb_metadoc):
    iter_start = time.time()
    # Get metadata in blockchain
    metadoc = store_var_contract.functions.getFromListMetadoc(cpt).call()
    #metadoc[0] = path
    #metadoc[1] = date of the creation
    #metadoc[2] = list of blocks
    #metadoc[3] = original size
    #metadoc[4] = entangling_blocks
    if(metadoc[3] == 0):
        break;
    print("Check metadoc "+metadoc[0])
    #Delete double quote added by transaction return
    metadoc[2] = metadoc[2].replace('"','')

    # Get metadata in Redis
    metadoc_redis = redis.hgetall("files:"+metadoc[0])
    if(not(metadoc_redis)):
      #Not exists in Redis ==> Entry deleted in Redis during an attack?
      channel.basic_publish(exchange='', routing_key='rebuild', body=json.dumps("files:"+metadoc[0]))
      print("-- Entry doesn't exist in Redis. Sent to rebuild script "+ metadoc[0])
      missing_entries = missing_entries + 1
      try:
        all_decoded_metadoc_metadata.remove(metadoc[0])
      except ValueError:
        pass
      cpt=cpt+1
      continue

    metadoc_redis = convert_redis_metadoc_responses(metadoc_redis)

    # Compare
    error_detected = 0
    #Path
    if(metadoc[0] != metadoc_redis['path']):
      print("-- Error for path")
      print("---- Values: "+ str(metadoc[0])+" != "+str(metadoc_redis['path']))
      error_detected = error_detected + 1
    #Creation_date
    if(metadoc[1] != metadoc_redis['creation_date']):
      print("-- Error for creation_date ")
      print("---- Values: "+ str(metadoc[1])+" != "+str(metadoc_redis['creation_date']))
      error_detected = error_detected + 1
    #List of blocks
    if(metadoc[2] != metadoc_redis['blocks']):
      print("-- Error for list of blocks ")
      print("---- Values: "+ str(metadoc[2])+" != "+str(metadoc_redis['blocks']))
      error_detected = error_detected + 1
    #Original Size
    if(int(metadoc[3]) != int(metadoc_redis['original_size'])):
      print("-- Error for original size ")
      print("---- Values: "+ str(metadoc[3])+" != "+str(metadoc_redis['original_size']))
      error_detected = error_detected + 1
    #Entangling_blocks
    if(metadoc[4] != metadoc_redis['entangling_blocks']):
      print("-- Error for entangled with ")
      print("---- Values: "+ str(metadoc[4])+" != "+str(metadoc_redis['entangling_blocks']))
      error_detected = error_detected + 1
    
    if(error_detected != 0):
      print("-- Error detected: "+ str(error_detected))
      metadoc_corrupted.append(metadoc[0])
      corrupted_entries = corrupted_entries + 1
      all_decoded_metadoc_metadata.remove(metadoc[0])
      channel.basic_publish(exchange='', routing_key='rebuild', body=json.dumps("files:"+metadoc[0]))
    else:
      redis.hset("files:{:s}".format(metadoc[0]), "audit", audit_number)
      #time_redis = redis.time()
    #Write stats in file
    iter_stop = time.time()
    iter_delta = iter_stop - iter_start
    fichier.write("files:"+metadoc[0]+" "+str(iter_stop)+" "+str(iter_delta)+"\n")
    cpt=cpt+1

print("\n")




# +-------------------------------------------------------------------+
# IS THERE ENTRIES IN REDIS WHICH NO MATCHES WITH BLOCKCHAIN ENTRIES? |
# +-------------------------------------------------------------------+
print("*********************************************************************")
print("Check all entries in Redis to be sure there is no bad entries")
print("*********************************************************************")

#Metablock
for key in all_decoded_metablock_metadata:
  iter_start = time.time()
  validation_blockchain = redis.hget("blocks:"+key, "flag")
  if(validation_blockchain.decode('utf-8') == "0"):
    continue
  else:
    already_checked = redis.hexists("blocks:"+key, "audit")
    if(already_checked == False):
      print("-- blocks:"+key+" : Not associated with an entry in the blockchain!")
      redis.delete("blocks:"+key)
      print("---- blocks:"+key+ " deleted.")
      bad_entries = bad_entries +1
    else:
      # This metablock was already checked in the first way blockchain ==> redis
      # Delete audit field
      redis.hdel("blocks:"+key,"audit")
      print("-- blocks:"+key+" : already checked (Audit field deleted in Redis)")
  #Write stats in file
  #time_redis = redis.time()
  iter_stop = time.time()
  iter_delta = iter_stop - iter_start
  fichier.write("blocks:"+key+" "+str(iter_stop)+" "+str(iter_delta)+"\n")
#Metadoc
for key in all_decoded_metadoc_metadata:
  iter_start = time.time()
  validation_blockchain = redis.hget("files:"+key, "flag")
  if(validation_blockchain.decode('utf-8') == "0"):
    continue
  else:
    already_checked = redis.hexists("files:"+key, "audit")
    if(already_checked == False):
      print("-- files:"+key+" : Not associated with an entry in the blockchain!")
      redis.delete("files:"+key)
      print("---- files:"+key+ " deleted.")
      bad_entries = bad_entries +1
    else:
      # This metablock was already checked in the first way blockchain ==> redis
      # Delete audit field
      redis.hdel("files:"+key,"audit")
      print("-- files:"+key+" : already checked (Audit field deleted in Redis)")
  #Write stats in file
  #time_redis = redis.time()
  iter_stop = time.time()
  iter_delta = iter_stop - iter_start
  fichier.write("files:"+key+" "+str(iter_stop)+" "+str(iter_delta)+"\n")
time_end = redis.time()
print("\n\n")

# +-------------------------------------------------------------------+
# Audit results                                                       |
# +-------------------------------------------------------------------+
print("*********************************************************************")
print("Audit results number "+str(audit_number))
print("*********************************************************************")

corrupted_number = len(metadoc_corrupted)+len(metablock_corrupted)
# Missing entries
if(missing_entries==0):
  print("There was no missing entry in Redis database.")
elif(missing_entries==1):
  print("There was 1 missing entry in Redis database.")
else:
  print("There were "+str(missing_entries)+" missing entries in Redis database.")
# Corrupted entries
if(corrupted_entries==0):
  print("There was no corrupted entry in Redis database.")
elif(corrupted_entries==1):
  print("There was 1 corrupted entry in Redis database.")
else:
  print("There were "+str(corrupted_entries)+" corrupted entries in Redis database")
# Bad entries
if(bad_entries==0):
  print("There was no bad entry in Redis database.")
elif(bad_entries==1):
  print("There was 1 bad entry in Redis database.")
else:
  print("There were "+str(bad_entries)+" bad entries in Redis database.")

time1 = str(time_begin[0])+"."+str(time_begin[1])
time2 = str(time_end[0])+"."+str(time_end[1])
duration = float(time2) - float(time1)
print("\nRunning in "+str(duration)+ " seconds")
fichier.close()