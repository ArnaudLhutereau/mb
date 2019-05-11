import sys
import time
import redis
import requests
import json




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

def convert_redis_index(result):

  decoded_list = []
  for key in result:
    decoded_list.append(key.decode('utf-8'))

  return decoded_list


# Get all keys in Redis
all_metadata_metablock_entries = redis.zrange("block_index",0,-1)
all_decoded_metablock_metadata = convert_redis_index(all_metadata_metablock_entries)
# Get metablock from Redis
all_metadata_metadoc_entries = redis.zrange("file_index",0,-1)
all_decoded_metadoc_metadata = convert_redis_index(all_metadata_metadoc_entries)


# Delete one field in each metadoc
for key in all_decoded_metadoc_metadata:
	redis.hdel("files:"+key,"entangling_blocks")
print("Metadoc: All entangling_blocks field deleted")

# Delete one field in each mtablock
for key in all_decoded_metablock_metadata:
	redis.hdel("blocks:"+key,"size")
print("Metablock: All size field deleted")


