import os
import time
import json
import redis
import requests
from threading import Thread
from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3
from web3.middleware import geth_poa_middleware
from solc import compile_source

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









# ****************************************
# *                                      *
# *	  PARAMETERS                         *
# *                                      *
# ****************************************
# Total number of file sending
# For each file, 4 transactions in the blockchain will be send
number_file = 100

# Counter
cpt = 0

# Thread
global nb_thread
nb_thread = 0
# Stats
fichier = open("save_benchmark_throughtput.txt", "w")

# ****************************************
# *                                      *
# *	  SCRIPTS                            *
# *                                      *
# ****************************************

class TransactionBlockchainMetadoc(Thread):

    def __init__(self, body, cpt):
        Thread.__init__(self)
        self.body = body
        self.cpt = cpt

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


while(cpt < number_file):
    meta_doc = {
        "flag": 0,
        "path": "path_test2_1_"+str(cpt),
        "creation_date": "date_"+str(cpt),
        "original_size": cpt,
        "blocks": "1,2,3",
        "entangling_blocks": "1,2,3"
    }
    meta_bloc1 = {
        "key": "key_test2_1_"+str(cpt),
        "creation_date": "date_"+str(cpt),
        "providers": "1,2,3",
        "block_type": 1,
        "checksum": "112545",
        "entangled_with": "entangling_blocks": "test2_10.txt-00,test2_10.txt-01,test2_10.txt-02",
        "size": cpt
    }
    meta_bloc2 = {
        "key": "key_test2_2_"+str(cpt),
        "creation_date": "date_"+str(cpt),
        "providers": "1,2,3",
        "block_type": 1,
        "checksum": "112545",
        "entangled_with": "entangling_blocks": "test2_10.txt-00,test2_10.txt-01,test2_10.txt-02",
        "size": cpt
    }
    meta_bloc3 = {
        "key": "key_test2_3_"+str(cpt),
        "creation_date": "date_"+str(cpt),
        "providers": "1,2,3",
        "block_type": 1,
        "checksum": "112545",
        "entangled_with": "entangling_blocks": "test2_10.txt-00,test2_10.txt-01,test2_10.txt-02",
        "size": cpt
    }


    # Start thread metablock 1
    while(nb_thread > 0):
        time.sleep(0.1)
    nb_thread = nb_thread + 1
    thread_bloc1 = TransactionBlockchainMetablock(meta_bloc1)
    thread_bloc1.start()

    # Start thread metablock 2
    while(nb_thread > 0):
        time.sleep(0.1)
    nb_thread = nb_thread + 1
    thread_bloc2 = TransactionBlockchainMetablock(meta_bloc2)
    thread_bloc2.start()

    # Start thread metablock 3
    while(nb_thread > 0):
        time.sleep(0.1)
    nb_thread = nb_thread + 1
    thread_bloc3 = TransactionBlockchainMetablock(meta_bloc3)
    thread_bloc3.start()

    # Start thread metadoc
    while(nb_thread > 0):
        time.sleep(0.1)
    nb_thread = nb_thread + 1
    thread_doc = TransactionBlockchainMetadoc(meta_doc, cpt)
    thread_doc.start()

    cpt=cpt+1



print("Benchmark finished for "+str(cpt)+" files")


while(nb_thread != 0):
  time.sleep(0.1)
fichier.close()
print("Close file results")