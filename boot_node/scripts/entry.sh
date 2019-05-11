#!/bin/bash

hostname -I > /home/priv/serveur/serveur.html
cd /home/priv/serveur/
python -m SimpleHTTPServer 1234 &
#bootnode -nodekeyhex $nodekeyhex
bootnode --genkey=boot.key
bootnode --nodekey=boot.key