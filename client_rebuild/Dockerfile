FROM ubuntu:18.04

# Install softwares
RUN apt-get update &&\
    apt-get -y dist-upgrade &&\
    apt-get install -y git \
                      python3 \
                      libssl-dev libffi-dev autoconf automake libtool \
                      pandoc \
                      lib32ncurses5-dev \
                      libdpkg-perl \
                      python3-dev \
                      python3-pip \
                      software-properties-common
RUN add-apt-repository ppa:ethereum/ethereum &&\
    apt-get update &&\
    apt-get install -y solc \
                       nano



RUN apt-get install -y curl

WORKDIR /home/


RUN apt-get install -y git
RUN git clone https://github.com/ethereum/go-ethereum.git

RUN apt-get install make
RUN apt-get install -y golang-go

WORKDIR /home/go-ethereum/

RUN git checkout -b v1.8.14

RUN make all



# Cloning git
WORKDIR /home/
RUN git clone https://github.com/ethereum/web3.py.git
WORKDIR /home/web3.py
RUN git checkout v4.6.0


# Run pip
RUN pip3 install -U pip setuptools wheel
RUN pip3 install -e .[tester] -r requirements-dev.txt
RUN pip3 install py-solc
RUN pip3 install pika
RUN pip3 install redis

COPY ./start.sh /home/start.sh
RUN chmod +x /home/start.sh

WORKDIR /home/
RUN mkdir meta_blockchain
COPY ./meta_blockchain/ /home/meta_blockchain/

EXPOSE 8001

# Launch
ENTRYPOINT /home/$USER/start.sh
