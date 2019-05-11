import os
import time
import json
import redis
import requests


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
   address="0xA65ccD60219572a1be7321E1E21C4f9e179c79B7",
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
fichier = open("save_get_metadata_to_recast.txt", "w")

# ****************************************
# *                                      *
# *	  SCRIPTS                            *
# *                                      *
# ****************************************

        

while(cpt < number_file):
    
    time_start = time.time()
    path = "test_"+str(cpt)
    # Get metadoc
    metadoc = store_var_contract.functions.getMetadocMap(path).call()
    # Get Metablock

    list_blocks = metadoc[1].split(",")
    print("---- Blocks list: ")
    print(metadoc)
    metablock_list = []
    for block in list_blocks:
        #Get metablock from blockchain
        metablock = store_var_contract.functions.getMetablockMap(block).call()
        print("---- Get one block ")
        metablock_list.append(metablock)

    time_end = time.time()
    delta_time = time_end - time_start
    print("files:"+str(path)+" in "+str(delta_time) + " seconds")
    fichier.write("files:"+str(path)+" "+str(time_end)+" "+str(delta_time)+"\n")
    cpt = cpt +1



print("Benchmark finished for "+str(cpt)+" files")


