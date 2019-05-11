#!/bin/bash

PORT=30304
RPCPORT=8001
NETWORKID=42
IDENTITY="MyPrivateChain"
DATADIR=/home/priv/data
NAT=none
RPCADDR="0.0.0.0"
WSPORT=9001
BOOTNODEID=c3ee4d19e4a97ae5372ee8f939837d79b1d14472005c3605827b7b954ff0c5383cd7a6b2e5998e16ab0e180bde7552e3e11321a1f28a0978a60a7011f8d5e6a4
BOOTNODEIP="172.18.0.2"

geth --rpc --ws --port $PORT --rpcport $RPCPORT --networkid $NETWORKID --bootnodes "enode://$BOOTNODEID@$BOOTNODEIP:30301" --mine --syncmode "fast" --datadir $DATADIR --nat $NAT --identity $IDENTITY --rpcapi web3,admin,eth,personal,miner,net --gasprice '1' -unlock '0xaf7cacff716936721ab1a11298ed4e05f6272dfc' --password /home/priv/data/password.txt --rpcaddr $RPCADDR --wsaddr $RPCADDR --wsport $WSPORT --rpccorsdomain \* 

