import sys
import time
import pprint
import pika
import json
import redis
import requests

from threading import Thread
from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3
from web3.middleware import geth_poa_middleware
from solc import compile_source


# +--------------------------------------------------------------+
# | INITIALIZATION RABBITMQ                                      |
# +--------------------------------------------------------------+
credentials = pika.PlainCredentials('client_rebuild', 'client_rebuild')
parameters = pika.ConnectionParameters('rabbitmq_server',
                                       5672,
                                       'vhost_rebuild',
                                       credentials)
# CONNECTION
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# INITIALISATION
channel.queue_declare(queue='rebuild')

# +--------------------------------------------------------------+
# | INITIALIZATION REDIS                                         |
# +--------------------------------------------------------------+

host="metadata"
port=6379
pool = redis.ConnectionPool(host=host,
                                        port=port,
                                        db=0,
                                        max_connections=128,
                                        socket_keepalive=True)
redis = redis.StrictRedis(connection_pool=pool,
                                       encoding=None,
                                       socket_keepalive=True)


# +--------------------------------------------------------------+
# |                FUNCTIONS FOR THE BLOCKCHAIN                  |
# +--------------------------------------------------------------+

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
ip_address_node_container="http://node1:1234/serveur.html"
ip_adress = requests.get(ip_address_node_container)
ip_adress_final = "http://"+ip_adress.text[:-2]+":8001"
my_provider = Web3.HTTPProvider(ip_adress_final)
w3 = Web3(my_provider)
w3.middleware_stack.inject(geth_poa_middleware, layer=0)
w3.eth.defaultAccount = w3.eth.accounts[0]


# Compilation of the contract
contract_source_path = 'contrat.sol'
compiled_sol = compile_source_file('contrat.sol')
contract_id, contract_interface = compiled_sol.popitem()
store_var_contract = w3.eth.contract(
   address="0x8d1b9E0e3668c7cFAD756BA275EB36b0a4D39d63",
   abi=contract_interface['abi'])


#Function from Recast used to convert the checksum
def convert_binary_to_hex_digest(binary_digest):
    """
    Converts a binary digest from hashlib.sha256.digest
    Args:
        binary_digest(str): Binary digest from hashlib.sha256.digest()
    Returns:
        str: Equivalent of the hexdigest for the same input
    """
    return "".join(["{:02x}".format(ord(c)) for c in binary_digest])


# +--------------------------------------------------------------+
# |        CLASS FOR THREAD AND RUN THE SCRIPT                   |
# +--------------------------------------------------------------+
class TransactionRebuildMetadata(Thread):

    def __init__(self, body):
        Thread.__init__(self)
        self.body = body

    def run(self):
        key = store_var_contract.functions.getMetadocMap(self.body).call()
        #[0] = date of the creation
        #[1] = list of blocks
        #[2] = original size
        #[3] = entangling_blocks
        print("Searching metadata in blockchain for path_given (metadoc) : "+self.body)
        if(key[2] == 0):
          #Error, metadata of this file not in BC
          print("-- Metadoc have an original size of 0, means he's not in blockchain.\n")
          return
        print("-- A metadoc key was found in blockchain")
        #Request Redis part :
        #Delete metadata of metadoc in Redis database, then push it again with blockchain metadata
        redis.delete("files:"+self.body)
        print("---- Metadoc key deleted in Redis")
        key[1] = key[1].replace('"','')
        # Parse data from blockchain, same thing that in metadata.py in Recast
        metadoc_to_redis = {
            "path": self.body,
            "creation_date": key[0],
            "original_size": key[2],
            "blocks": key[1],
            "entangling_blocks": key[3]
        }
        #Add metadoc in Redis database
        redis.hmset("files:{:s}".format(self.body), metadoc_to_redis)
        print("---- Metadoc key added in Redis")
        #Get each metablock
        list_blocks = key[1].split(",")
        print("-- List of all blocks of "+self.body)
        print(key[1])
        for block in list_blocks:
            print("-- Metablock: "+block)
            #Get metablock from blockchain
            metablock = store_var_contract.functions.getMetablockMap(block).call()
            #metablock[0] = creation_date
            #metablock[1] = providers
            #metablock[2] = block_type
            #metablock[3] = checksum
            #metablock[4] = size
            #metablock[5] = entangled_with

            #Convert uint type from blockchain to string for block type
            if(metablock[2] == 1):
              metablock[2] = "DATA"
            else:
              metablock[2] = "PARITY"
            #Delete double quote added by transaction return
            metablock[1] = metablock[1].replace('"','')
            #Delete metablock entry in Redis
            redis.delete("blocks:"+block)
            print("---- Metablock key deleted in Redis")
            metablock_to_redis = {
                "key": block,
                "creation_date": metablock[0],
                "providers": metablock[1],
                "block_type": metablock[2],
                "checksum": metablock[3],
                "entangled_with": metablock[5],
                "size": metablock[4]
                }
            #Add metadoc in Redis database
            redis.hmset("blocks:{:s}".format(block), metablock_to_redis)
        time_redis = redis.time()
        
        link="http://stats:80/api/receive_rebuild.php?request="+self.body+"///"+str(time_redis[0])+"."+str(time_redis[1])+"///All"
        requests.get(link)
            

# +--------------------------------------------------------------+
# |   FUNCTION CALLED WHEN AN ELEMENT IS FOUND IN THE QUEUE      |
# +--------------------------------------------------------------+
def callback(ch, method, properties, body):
    
    body = json.loads(body)
    print("\nThread started for one request:\n")
    # Determine if body contains a metadoc name
    thread = TransactionRebuildMetadata(body)
    thread.start()


channel.basic_consume(callback,
                      queue='rebuild',
                      no_ack=True)

# +--------------------------------------------------------------+
# |               START LISTENING ON RABBITMQ                    |
# +--------------------------------------------------------------+
print(' [*] Waiting for metadata path. To exit press CTRL+C')
channel.start_consuming()