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
number_file = 400

# Counter
cpt = 0

# Thread
global nb_thread
nb_thread = 0
# Stats
fichier = open("save_benchmark_disk_space.txt", "w")

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
        nb_thread = nb_thread - 1
        time_transaction = time_mid - time_start
        time_receipt = time_end - time_start

        print("Thread finished for "+ self.body['path']+" / Time receipt: "+str(time_receipt))

        fichier.write("files:"+self.body['path']+" "+str(time_end)+" "+str(time_receipt)+"\n")
        if((self.cpt%100) == 0):
            print("\n\n"+str(self.cpt)+" files in the blockchain ! Check disk space on nodes ;)\n\n")

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
        nb_thread = nb_thread - 1
        time_transaction = time_mid - time_start
        time_receipt = time_end - time_start

        #print("Thread finished for "+ self.body['key'] +" / Time receipt: "+str(time_receipt))



        

while(cpt < number_file):
    meta_doc = {
        "flag": 0,
        "path": "path_"+str(cpt),
        "creation_date": "2018-08-30 08:25:25.672362"+str(cpt),
        "original_size": cpt,
        "blocks": "test2_10.txt-00,test2_10.txt-01,test2_10.txt-02",
        "entangling_blocks": "test2_10.txt-00,test2_10.txt-01,test2_10.txt-02"
    }
    meta_bloc_1 = {
        "key": "key_1_"+str(cpt),
        "creation_date": "2018-08-30 08:22:28.978242_"+str(cpt),
        "providers": "storage-node-13,storage-node-3,storage-node-4",
        "block_type": 1,
        "checksum": "650254ee541376f11025bd0e0f6e38cb8f28884cbcbaeb9ea39841478dc125a7",
        "entangled_with": "test2_10.txt-00,test2_10.txt-01,test2_10.txt-02",
        "size": cpt
    }
    meta_bloc_2 = {
        "key": "key_2_"+str(cpt),
        "creation_date": "2018-08-30 08:22:28.978242_"+str(cpt),
        "providers": "storage-node-13,storage-node-3,storage-node-4",
        "block_type": 1,
        "checksum": "650254ee541376f11025bd0e0f6e38cb8f28884cbcbaeb9ea39841478dc125a7",
        "entangled_with": "test2_10.txt-00,test2_10.txt-01,test2_10.txt-02",
        "size": cpt
    }
    meta_bloc_3 = {
        "key": "key_3_"+str(cpt),
        "creation_date": "2018-08-30 08:22:28.978242_"+str(cpt),
        "providers": "storage-node-13,storage-node-3,storage-node-4",
        "block_type": 1,
        "checksum": "650254ee541376f11025bd0e0f6e38cb8f28884cbcbaeb9ea39841478dc125a7",
        "entangled_with": "test2_10.txt-00,test2_10.txt-01,test2_10.txt-02",
        "size": cpt
    }

    # Start thread
    while(nb_thread > 4):
        time.sleep(0.1)

    nb_thread = nb_thread + 4

    thread_bloc1 = TransactionBlockchainMetablock(meta_bloc_1)
    thread_bloc1.start()
    thread_bloc2 = TransactionBlockchainMetablock(meta_bloc_2)
    thread_bloc2.start()
    thread_bloc3 = TransactionBlockchainMetablock(meta_bloc_3)
    thread_bloc3.start()
    thread_doc = TransactionBlockchainMetadoc(meta_doc, cpt)
    thread_doc.start()

    cpt=cpt+1

print("Benchmark finished for "+str(cpt)+" files")


