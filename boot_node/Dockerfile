FROM ubuntu:18.04

# Install softwares
RUN apt-get update &&\
    apt-get dist-upgrade -y &&\
    apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:ethereum/ethereum &&\
    apt-get update &&\
    apt-get install -y python

# Get Ethereum
RUN apt-get install bootnode

WORKDIR /home/


RUN apt-get install -y git
RUN git clone https://github.com/ethereum/go-ethereum.git

RUN apt-get install make
RUN apt-get install -y golang-go

WORKDIR /home/go-ethereum/

RUN git checkout -b v1.8.14

RUN make all

# Creation of directories
WORKDIR /home/

# Get scripts for the launch
COPY ./scripts/LAUNCH.sh priv/scripts/LAUNCH.sh

# Give the permission
WORKDIR /home/priv/scripts/
RUN chmod +x LAUNCH.sh

COPY ./scripts/entry.sh /home/priv/scripts/entry.sh
RUN chmod +x entry.sh

# hostname
COPY ./serveur/index.html /home/priv/serveur/index.html
COPY ./serveur/serveur.py /home/priv/serveur/serveur.py

EXPOSE 1234

# Launch bootnode
ENV nodekeyhex=$nodekeyhex

ENTRYPOINT /home/priv/scripts/entry.sh
# ENTRYPOINT bootnode -nodekeyhex $nodekeyhex
