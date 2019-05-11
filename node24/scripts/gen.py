import os


# Read the adress IP from the bootnode
file = open("ip_bootnode.txt", "r")
adresse_ip = file.readline().rstrip('\n')
adresse_ip = adresse_ip.replace(' ','')

file.close()

file = open("gen.sh", "a")

command = "touch new_start.sh\nchmod u+x new_start.sh\necho \"\n#!/bin/bash\nPORT=30327\nRPCPORT=8024\nNETWORKID=42\nIDENTITY=\\\"MyPrivateChain\\\"\nDATADIR=/home/priv/data\nNAT=none\nRPCADDR=\\\"0.0.0.0\\\"\nWSPORT=9024\nBOOTNODEID=c3ee4d19e4a97ae5372ee8f939837d79b1d14472005c3605827b7b954ff0c5383cd7a6b2e5998e16ab0e180bde7552e3e11321a1f28a0978a60a7011f8d5e6a4\nBOOTNODEIP=\\\""+adresse_ip+"\\\""


command2 = "\ngeth --rpc --ws --port \\$PORT --rpcport \\$RPCPORT --networkid \\$NETWORKID --bootnodes \"enode://\\$BOOTNODEID@\\$BOOTNODEIP:30301\" --datadir \\$DATADIR --nat \\$NAT --identity \\$IDENTITY --rpcapi web3,admin,eth,personal,miner,net --rpcaddr \\$RPCADDR --wsaddr \\$RPCADDR --wsport \\$WSPORT --rpccorsdomain \* \n \" > new_start.sh"
file.write(command)
file.write(command2)
file.close()