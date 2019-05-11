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
parameters = pika.ConnectionParameters('rabbitmq_server',
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
   address="0xc3757CF49348f6be51e0eFA95da8349e4b8ba2bD",
   abi=contract_interface['abi'])


# +--------------------------------------------------------------+
# |        CLASS FOR THREAD AND RUN THE TRANSACTION              |
# +--------------------------------------------------------------+
class TransactionBlockchainMetadoc(Thread):

    def __init__(self, body):
        Thread.__init__(self)
        self.body = body

    def run(self):
        time_redis = redis.time()
        # Send statistics to the test container : START 
        

        link="http://stats:80/api/receive.php?request="+self.body['path']+"///"+str(time_redis[0])+"."+str(time_redis[1])+"///Start"
        requests.get(link)
        print("Thread started for metadoc ", self.body['path'], "currently time in redis: ", time_redis)
        
        tx_hash = store_var_contract.functions.addMetadocMap(self.body['path'], self.body['creation_date'], self.body['blocks'], self.body['original_size'], self.body['entangling_blocks']).transact()
        receipt = wait_for_receipt(w3, tx_hash, 1)
        redis.hset("files:{:s}".format(self.body['path']), "flag", 1)
        time_redis = redis.time()
        print("Thread finished for metadoc ", self.body['path'], "currently time in redis: ", time_redis)
        
        # Send statistics to the test container : FINISH
        link="http://stats:80/api/receive.php?request="+self.body['path']+"///"+str(time_redis[0])+"."+str(time_redis[1])+"///Finish"
        requests.get(link)
class TransactionBlockchainMetablock(Thread):

    def __init__(self, body):
        Thread.__init__(self)
        self.body = body

    def run(self):
        time_redis = redis.time()
        
        print("Thread started for metablock ", self.body['key'], "currently time in redis: ", time_redis, "type: ", self.body['block_type'])
        tx_hash = store_var_contract.functions.addMetablockMap(self.body['key'], self.body['creation_date'], self.body['providers'], self.body['block_type'], self.body['checksum'], self.body['size'], self.body['entangled_with']).transact()
        receipt = wait_for_receipt(w3, tx_hash, 1)
        redis.hset("blocks:{:s}".format(self.body['key']), "flag", 1)
        time_redis = redis.time()
        print("Thread finished for metablock ", self.body['key'], "currently time in redis: ", time_redis)

# +--------------------------------------------------------------+
# |   FUNCTION CALLED WHEN AN ELEMENT IS FOUND IN THE QUEUE      |
# +--------------------------------------------------------------+
def callback(ch, method, properties, body):
    
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