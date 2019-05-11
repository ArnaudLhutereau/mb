import sys
import time
import redis

# +--------------------------------------------------------------+
# | GOAL OF THE SCRIPT                                           |
# |																 |
# | The goal is to delete one of metablock metadata for          |
# | each file. By default it's the first ( -00 according to the) |
# | Recast syntax). Metadoc aren't delete.               		 |
# |																 |
# +--------------------------------------------------------------+


# +--------------------------------------------------------------+
# | INITIALIZATION REDIS                                         |
# +--------------------------------------------------------------+

host="cluster_metadata"
port=6379
pool = redis.ConnectionPool(host=host,
                                        port=port,
                                        db=0,
                                        max_connections=128,
                                        socket_keepalive=True)
redis = redis.StrictRedis(connection_pool=pool,
                                       encoding=None,
                                       socket_keepalive=True)

# +--------------------------------------------------------------+
# | SCRIPT                                                       |
# +--------------------------------------------------------------+

# Parameters
file_name = "test_"
number_of_file = 100
number_of_block = "-00"


# Start
cpt = 0
while (cpt<100):
	metadata_to_delete = file_name+str(cpt)+".txt"+number_of_block # test0-00, test1-00 ...
	# Request to delete this entry key in database
	redis.delete("blocks:"+metadata_to_delete)
	cpt=cpt+1