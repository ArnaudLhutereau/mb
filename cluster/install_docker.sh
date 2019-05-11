#!/bin/bash
apt-get update

apt-get install \
-y apt-transport-https \
-y ca-certificates \
-y curl \
-y software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add –

add-apt-repository \
"deb [arch=amd64] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) \
stable"

apt-get update

apt-get install docker-ce

curl -L https://github.com/docker/compose/releases/download/1.22.0-rc2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

chmod +x /usr/local/bin/docker-compose
