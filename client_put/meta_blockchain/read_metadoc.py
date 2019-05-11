import sys
import time
import pprint

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

my_provider = Web3.HTTPProvider('http://172.18.0.5:8001')
w3 = Web3(my_provider)
w3.middleware_stack.inject(geth_poa_middleware, layer=0)
w3.eth.defaultAccount = w3.eth.accounts[0]
contract_source_path = 'contrat.sol'
compiled_sol = compile_source_file('contrat.sol')

contract_id, contract_interface = compiled_sol.popitem()

#address = deploy_contract(w3, contract_interface)
#print("Deployed {0} to: {1}\n".format(contract_id, address))

store_var_contract = w3.eth.contract(
   address="0x4831CB4ebD5a3504030a379d36e07d014b05C389",
   abi=contract_interface['abi'])

path_given = ""
key = store_var_contract.functions.getMetadocMap(path_given).call()
print("Metadata de path_given : ")
print(key)