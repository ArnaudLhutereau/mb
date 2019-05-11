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
This script is used to rebuild all Redis database by erase old database and fill it again
with all blockchain metadata
It uses the same syntax that check_corruption.py
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
ip_address_node_container="http://cluster_node1:1234/serveur.html"
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
# Snapshot of file stored in blockchain                          |
# +--------------------------------------------------------------+
# Get number metablock in blockchain
nb_metablock = store_var_contract.functions.getNumberMetablock().call()
# Get number metadoc in blockchain
nb_metadoc = store_var_contract.functions.getNumberMetadoc().call()

print("\n")
print("*********************************************************************")
print("REBUILD ALL REDIS DATABASE")
print("*********************************************************************")
print("This script will erase all Redis database and push all blockchain metadata in Redis.\n\n")

# +--------------------------------------------------------------+
# |                 SCRIPT                                       |
# +--------------------------------------------------------------+

print("*********************************************************************")
print("Erase actual Redis database")
print("*********************************************************************")
print("-- Clear all keys...")
redis.flushdb()
print("---- All keys deleted\n\n")



print("*********************************************************************")
print("Copy all entries from blockchain to Redis database")
print("*********************************************************************")

# Metablock
print("-- Copy all metablocks")
cpt = 0
while(cpt < nb_metablock):
    # Get metadata in blockchain
    metablock = store_var_contract.functions.getFromListMetablock(cpt).call()
    #metablock[0] = key
    #metablock[5] = size
    if(metablock[5] == 0):
        #if not exists in blockchain: quit loop
        break;
    print("---- blocks:"+metablock[0])
    channel.basic_publish(exchange='', routing_key='rebuild', body=json.dumps("blocks:"+metablock[0]))
    cpt=cpt+1

# Metadoc
print("\n-- Copy all metadoc")
cpt = 0
while(cpt < nb_metadoc):
    metadoc = store_var_contract.functions.getFromListMetadoc(cpt).call()
    #metadoc[0] = path
    #metadoc[3] = original size
    if(metadoc[3] == 0):
        #if not exists in blockchain: quit loop
        break;
    print("---- files:"+metadoc[0])
    channel.basic_publish(exchange='', routing_key='rebuild', body=json.dumps("files:"+metadoc[0]))
    cpt=cpt+1

print("\n\n")
print("All metadata from blockchain are sending to the rebuilding script.")
# Close Rabbitmq connection
connection.close()


