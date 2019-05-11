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

# Copy the keystore
COPY ./keystore/UTC--2018-06-04T09-00-25.423677385Z--af7cacff716936721ab1a11298ed4e05f6272dfc priv/data/keystore/UTC--2018-06-04T09-00-25.423677385Z--af7cacff716936721ab1a11298ed4e05f6272dfc
# Copy the password
COPY ./password.txt priv/data/password.txt

# Get all scripts
COPY ./scripts/ priv/scripts/

# Server for hostname
COPY ./serveur/ /home/priv/serveur/

EXPOSE 1234

WORKDIR /home/priv/scripts/
RUN chmod +x LAUNCH.sh
RUN chmod +x LAUNCH_CLUSTER.sh
RUN chmod +x INIT_PRIV_CHAIN.sh
RUN chmod +x START_CHAIN_DAEMON.sh

RUN apt-get update


# Initialise and launch the blockchain
ENTRYPOINT /home/priv/scripts/LAUNCH.sh
#ENTRYPOINT /home/priv/scripts/LAUNCH_CLUSTER.sh
