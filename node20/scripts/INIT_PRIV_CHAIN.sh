#!/bin/bash

DATADIR=/home/priv/data
GENESIS=/home/priv/config/CustomGenesis.json
NETWORKID=42
IDENTITY="MyPrivateChain"
PORT=30323
RPCPORT=8020

# Initialize the private blockchain
geth --networkid $NETWORKID --datadir=$DATADIR --identity $IDENTITY --port $PORT --rpcport $RPCPORT init $GENESIS

