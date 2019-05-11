import sys
import time
import pprint
import pika
import json
import redis


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
global file_begin
file_begin = "test105.txt-00"
global file_end
file_end = "test105.txt"
global time_begin
time_begin = None
global time_end
time_end = None

# +--------------------------------------------------------------+
# |                FUNCTIONS FOR THE BLOCKCHAIN                  |
# +--------------------------------------------------------------+

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()

   return compile_source(source)


def deploy_contract(w3, contract_interface):
    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).deploy()

    address = w3.eth.waitForTransactionReceipt(tx_hash)['contractAddress']
    
    return address


def wait_for_receipt(w3, tx_hash, poll_interval):
   while True:
       tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
       if tx_receipt:
         return tx_receipt
       time.sleep(poll_interval)


# +--------------------------------------------------------------+
# |        INITIALISATION OF THE BLOCKCHAIN AND ACCOUNT          |
# +--------------------------------------------------------------+
my_provider = Web3.HTTPProvider('http://172.18.0.5:8001')
w3 = Web3(my_provider)
w3.middleware_stack.inject(geth_poa_middleware, layer=0)
w3.eth.defaultAccount = w3.eth.accounts[0]

# Compilation of the contract
contract_source_path = 'contrat.sol'
compiled_sol = compile_source_file('contrat.sol')
contract_id, contract_interface = compiled_sol.popitem()

store_var_contract = w3.eth.contract(
   address="0x7b6D4FA12d78E6Ba15d31F36495362D3bbe08691",
   abi=contract_interface['abi'])







# FUNCTION CALLED WHEN AN ELEMENT IS FOUND IN THE QUEUE
def callback(ch, method, properties, body):
    
    body = json.loads(body)
    # Determine if body contains a metablock or a metadoc

    if(body['hash_type'] == 0):
        # Case Metadoc
        print("[!] Received a metadoc")
        print("Path: " + body['path'])
        print("Creation date: " + body['creation_date'])
        print("Original size: " + str(body['original_size']))
        print("Blocks: " + body['blocks'])
        print("Entangling blocks: " + body['entangling_blocks'])
        # Transaction with the smart contract in the blockchain
        print("Sending transaction to the smart contract...\n")
        tx_hash = store_var_contract.functions.addMetadoc(body['path'], body['creation_date'], body['blocks'], body['original_size']).transact()
        receipt = wait_for_receipt(w3, tx_hash, 1)
        redis.hset("files:{:s}".format(body['path']), "flag", 1)
        print("Transaction receipt mined")
        
        # TEST
        
        if(body['path'] == file_end):
            global time_end
            time_end = redis.time()
            print("Derniere requete: ")
            print(time_end)
            global time_begin
            print("Premiere requete: ")
            print(time_begin)
        #pprint.pprint(dict(receipt))

    else:
        if(body['key'] == file_begin):

            time_begin = redis.time()
            print("Time_begin to store in blockchain and time end for rabbitrequest")
        # Case Metablock
        print("[!] Received a metablock")
        print("Key: " + body['key'])
        print("Creation_date: " + body['creation_date'])
        print("Block_type: " + str(body['block_type']))
        print("Checksum: " + body['checksum'])
        print("Providers: " + body['providers'])
        print("entangled_with: " + body['entangled_with'])
        print("size: " + str(body['size']))
        # Transaction with the smart contract in the blockchain
        print("Sending transaction to the smart contract...\n")
        tx_hash = store_var_contract.functions.addMetablock(body['key'], body['creation_date'], body['block_type'], body['checksum'], body['providers'], body['size']).transact()
        receipt = wait_for_receipt(w3, tx_hash, 1)
        print("Transaction receipt mined")
        #pprint.pprint(dict(receipt))
    print("\n\n")
    print('[*] Waiting for new messages. To exit press CTRL+C')

    
    

    '''
    # +--------------------------------------------------------------+
    # |         PLAY TRANSACTION IN THE SMART CONTRACT         |
    # +--------------------------------------------------------------+
    print("ENVOIE VERS LA BLOCKCHAIN")
    print("Transaction addMetablockToBlockchain")
    print("Sending transaction to addBlock...\n")

    tx_hash = store_var_contract.functions.addMetablock(body['key'], body['creation_date'], body['block_type'], body['checksum'], body['providers'], body['size']).transact()
    receipt = wait_for_receipt(w3, tx_hash, 1)
    print("Transaction receipt mined: \n")
    
    if receipt['blockNumber'] == None:
        while receipt['blockNumber'] == None:
            print("Try to send again the transaction")
            tx_hash = store_var_contract.functions.addMetablock(body['key'], body['creation_date'], body['block_type'], body['checksum'], body['providers'], body['size']).transact()
            receipt = wait_for_receipt(w3, tx_hash, 1)

    
    '''

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

# LAUNCH
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()