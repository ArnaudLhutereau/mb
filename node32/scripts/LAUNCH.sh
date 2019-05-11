#!/bin/bash


export PATH=$PATH:/home/go-ethereum/build/bin

sleep 15

#Get IP and put it on a python server web
hostname -I > /home/priv/serveur/serveur.html
cd /home/priv/serveur/
python -m SimpleHTTPServer 1234 &

cd /home/priv/scripts/

./INIT_PRIV_CHAIN.sh
curl bootnode:1234/serveur.html > ip_bootnode.txt
python3 get_ip.py
python3 gen.py
chmod u+x gen.sh

./gen.sh
./new_start.sh
#tail -f /dev/null