# Metablock on cluster

## What do you need?

To deploy Metablock (and Recast) on cluster, you have to modify the docker-compose file and change build path by image name
which will be downloaded from a repository ([Docker Hub](https://hub.docker.com/) for example).

Recast uses some compiled files that force you to build images inside your cluster environment. If you don't build on it, you may
encounter some bugs.


## How to deploy

* First you have to install Docker and Docker-compose on each machine. You can find a bash script in this folder
to do it (install_docker.sh)

* In a second time, you have to clone Recast and Metablock project on the master machine. Check the folder metablock/Recast to
see what files you need to change to include metablock connection in Recast.

* Now you can build each containers writes in docker-compose, and upload it on a repository

* To deploy a cluster, we use Docker swarm. On master node, init the cluster with "docker swarm init". Copy the return line and
paste it on each slave node. They will join the cluster.

* Deploy services with "docker stack deploy --compose-file  	docker-compose-cluster.yml cluster" (cluster is the name of the stack, don't change it)

Because Docker swarm use the stack name for each container name, all useful scripts used for cluster are in special folder "cluster" of "client_put" and "client_rebuild" containers. 

For example if you want to start and audit in "client_rebuild" container, you have to launch the script in /meta_blockchain/cluster/ and not in /meta_blockchain/ .




