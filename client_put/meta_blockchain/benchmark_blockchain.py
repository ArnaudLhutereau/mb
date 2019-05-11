import pika
import json

# ****************************************
# *                                      *
# *   INITIALISATION RABBITMQ            *
# *                                      *
# ****************************************
# Account
credentials = pika.PlainCredentials('client', 'client')
# RabbitMQ server
parameters = pika.ConnectionParameters("rabbitmq_server", 5672, 'vhost_put', credentials)
# Connection
connection = pika.BlockingConnection(parameters)
# Start channel
channel = connection.channel()
channel.queue_declare(queue='hello')

# ****************************************
# *                                      *
# *	  PARAMETERS                         *
# *                                      *
# ****************************************
# Total number of file sending
# For each file, 4 transactions in the blockchain will be send
number_file = 100

# Counter
cpt = 0

# ****************************************
# *                                      *
# *	  SCRIPTS                            *
# *                                      *
# ****************************************

while(cpt < number_file):
    meta_doc = {
        "hash_type" : 0,
        "flag": 0,
        "path": "path_"+str(cpt),
        "creation_date": "date_"+str(cpt),
        "original_size": cpt,
        "blocks": "1,2,3",
        "entangling_blocks": "1,2,3"
    }
    meta_bloc_1 = {
        "hash_type": 1,
        "key": "key_"+str(cpt),
        "creation_date": "date_"+str(cpt),
        "providers": "1,2,3",
        "block_type": 1,
        "checksum": "112545",
        "entangled_with": "1,2,3",
        "size": cpt
    }
    meta_bloc_2 = {
        "hash_type": 1,
        "key": "key_"+str(cpt),
        "creation_date": "date_"+str(cpt),
        "providers": "1,2,3",
        "block_type": 1,
        "checksum": "112545",
        "entangled_with": "1,2,3",
        "size": cpt
    }
    meta_bloc_3 = {
        "hash_type": 1,
        "key": "key_"+str(cpt),
        "creation_date": "date_"+str(cpt),
        "providers": "1,2,3",
        "block_type": 1,
        "checksum": "112545",
        "entangled_with": "1,2,3",
        "size": cpt
    }

    channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(meta_bloc_1))
    channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(meta_bloc_2))
    channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(meta_bloc_3))
    channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(meta_doc))
    print("File "+str(cpt)+" send to RabbitMQ\n")

    cpt=cpt+1

connection.close()



