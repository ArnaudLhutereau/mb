#!/bin/bash

DATADIR=/home/priv/data
GENESIS=/home/priv/config/CustomGenesis.json
NETWORKID=42
IDENTITY="MyPrivateChain"
PORT=30326
RPCPORT=8023

# Initialize the private blockchain
geth --networkid $NETWORKID --datadir=$DATADIR --identity $IDENTITY --port $PORT --rpcport $RPCPORT init $GENESIS

