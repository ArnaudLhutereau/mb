FROM ubuntu:18.04

# Install softwares
RUN apt-get update &&\
    apt-get dist-upgrade -y &&\
    apt-get install -y software-properties-common &&\
    add-apt-repository -y ppa:ethereum/ethereum &&\
    apt-get update &&\
    apt-get install -y python


RUN apt-get install -y curl

WORKDIR /home/


RUN apt-get install -y git
RUN git clone https://github.com/ethereum/go-ethereum.git

RUN apt-get install make
RUN apt-get install -y golang-go

WORKDIR /home/go-ethereum/

RUN git checkout -b v1.8.14

RUN make all


# Creation of directories
COPY ./scripts/DirectoryCreation.sh /home/DirectoryCreation.sh
WORKDIR /home/
RUN chmod +x DirectoryCreation.sh
RUN ./DirectoryCreation.sh

# Creation of genesis block
COPY ./CustomGenesis.json priv/config/CustomGenesis.json

# Get scripts for blockchain
COPY ./scripts/ priv/scripts/

# Server for hostname
COPY ./serveur/ /home/priv/serveur/

# Port
EXPOSE 1234

WORKDIR /home/priv/scripts/
RUN chmod +x LAUNCH.sh
RUN chmod +x LAUNCH_CLUSTER.sh
RUN chmod +x INIT_PRIV_CHAIN.sh
RUN chmod +x START_CHAIN_DAEMON.sh

#RUN chmod u+x gen.sh

RUN apt-get update

# Initialise and launch the blockchain
ENTRYPOINT /home/priv/scripts/LAUNCH.sh
#ENTRYPOINT /home/priv/scripts/LAUNCH_CLUSTER.sh
