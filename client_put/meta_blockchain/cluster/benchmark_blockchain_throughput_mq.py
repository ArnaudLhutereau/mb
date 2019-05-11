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
credentials = pika.PlainCredentials('client', 'client')
parameters = pika.ConnectionParameters('cluster_rabbitmq_server',
                                       5672,
                                       'vhost_put',
                                       credentials)
# CONNECTION
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# INITIALISATION
channel.queue_declare(queue='hello')

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


# Thread
global nb_thread
global max_thread
nb_thread = 0
max_thread = 1

# Stats
fichier = open("save_benchmark_throughtput_mq.txt", "w")

# +--------------------------------------------------------------+
# |        CLASS FOR THREAD AND RUN THE TRANSACTION              |
# +--------------------------------------------------------------+


class TransactionBlockchainMetadoc(Thread):

    def __init__(self, body,):
        Thread.__init__(self)
        self.body = body

    def run(self):
        # Store a metadoc
        global nb_thread

        time_start = time.time()

        tx_hash = store_var_contract.functions.addMetadocMap(self.body['path'], self.body['creation_date'], self.body['blocks'], self.body['original_size'], self.body['entangling_blocks']).transact()
        time_mid = time.time()
        receipt = wait_for_receipt(w3, tx_hash, 0.1)
        
        redis.hset("files:{:s}".format(self.body['path']), "flag", 1)
        time_end = time.time()
        
        time_transaction = time_mid - time_start
        time_receipt = time_end - time_start

        print("Thread finished for "+ self.body['path']+" / Time receipt: "+str(time_receipt))

        fichier.write("files:"+self.body['path']+" "+str(time_end)+" "+str(time_receipt)+"\n")
        nb_thread = nb_thread - 1
    
class TransactionBlockchainMetablock(Thread):

    def __init__(self, body):
        Thread.__init__(self)
        self.body = body

    def run(self):
        # Store a metablock
        global nb_thread
        time_start = time.time()

        tx_hash = store_var_contract.functions.addMetablockMap(self.body['key'], self.body['creation_date'], self.body['providers'], self.body['block_type'], self.body['checksum'], self.body['size'], self.body['entangled_with']).transact()
        time_mid = time.time()
        receipt = wait_for_receipt(w3, tx_hash, 0.1)
        redis.hset("blocks:{:s}".format(self.body['key']), "flag", 1)
        time_end = time.time()
        
        time_transaction = time_mid - time_start
        time_receipt = time_end - time_start
        #print("Thread finished for "+ self.body['key'] +" / Time receipt: "+str(time_receipt))
        nb_thread = nb_thread - 1



# +--------------------------------------------------------------+
# |   FUNCTION CALLED WHEN AN ELEMENT IS FOUND IN THE QUEUE      |
# +--------------------------------------------------------------+

def callback(ch, method, properties, body):
    
    global nb_thread
    global max_thread
    body = json.loads(body)
    # Determine if body contains a metablock or a metadoc

    if(body['hash_type'] == 0):
        # Case Metadoc

        '''
        # PRINT
        print("Path: " + body['path'])
        print("Creation date: " + body['creation_date'])
        print("Original size: " + str(body['original_size']))
        print("Blocks: " + body['blocks'])
        print("Entangling blocks: " + body['entangling_blocks'])
        '''
        # Transaction with the smart contract in the blockchain
        while(nb_thread > (max_thread-1)):
          time.sleep(0.1)
        nb_thread = nb_thread + 1
        thread = TransactionBlockchainMetadoc(body)
        thread.start()

    else:
        # Case Metablock
        # TEST TIME
        '''
        # PRINT
        print("Key: " + body['key'])
        print("Creation_date: " + body['creation_date'])
        print("Block_type: " + str(body['block_type']))
        print("Checksum: " + body['checksum'])
        print("Providers: " + body['providers'])
        print("entangled_with: " + body['entangled_with'])
        print("size: " + str(body['size']))
        '''
        # Transaction with the smart contract in the blockchain
        while(nb_thread > (max_thread-1)):
          time.sleep(0.1)
        nb_thread = nb_thread + 1
        thread = TransactionBlockchainMetablock(body)
        thread.start()

    #print("\n\n")
    #print('[*] Waiting for new messages. To exit press CTRL+C')


channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

# +--------------------------------------------------------------+
# |               START LISTENING ON RABBITMQ                    |
# +--------------------------------------------------------------+
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()