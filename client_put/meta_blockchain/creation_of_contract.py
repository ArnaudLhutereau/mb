import sys
import time
import pprint
import requests

from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3
from web3.middleware import geth_poa_middleware
from solc import compile_source


def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()

   return compile_source(source)


def deploy_contract(w3, contract_interface):
    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).deploy()

    address = w3.eth.waitForTransactionReceipt(tx_hash)['contractAddress']
    #address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
    
    return address


def wait_for_receipt(w3, tx_hash, poll_interval):
   while True:
       tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
       if tx_receipt:
         return tx_receipt
       time.sleep(poll_interval)



print("---------- START")
print("Connection to the node1...")
ip_address_node_container="http://node1:1234/serveur.html"
ip_adress = requests.get(ip_address_node_container)
ip_adress_final = "http://"+ip_adress.text[:-2]+":8001"

my_provider = Web3.HTTPProvider(ip_adress_final)
w3 = Web3(my_provider)
w3.middleware_stack.inject(geth_poa_middleware, layer=0)
w3.eth.defaultAccount = w3.eth.accounts[0]

print("Compile the contract...")
contract_source_path = 'contrat.sol'
compiled_sol = compile_source_file('contrat.sol')

contract_id, contract_interface = compiled_sol.popitem()

print("Deploy the contract...")
address = deploy_contract(w3, contract_interface)
print("Deployed {0} to: {1}\n".format(contract_id, address))

print("---------- END")