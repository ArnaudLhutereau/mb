import pika
import json

# ****************************************
# *                                      *
# *   INITIALISATION RABBITMQ            *
# *                                      *
# ****************************************
# Account
credentials = pika.PlainCredentials('client_rebuild', 'client_rebuild')
# RabbitMQ server
parameters = pika.ConnectionParameters("rabbitmq_server", 5672, 'vhost_rebuild', credentials)
# Connection
connection = pika.BlockingConnection(parameters)
# Start channel
channel = connection.channel()
channel.queue_declare(queue='rebuild')

# ****************************************
# *                                      *
# *	  PARAMETERS                         *
# *                                      *
# ****************************************
# Total number of file sending
# For each file, 4 transactions in the blockchain will be send
number_file = 1

# Counter
cpt = 0

# ****************************************
# *                                      *
# *	  SCRIPTS                            *
# *                                      *
# ****************************************

while(cpt < number_file):
    path = "test.txt"
    channel.basic_publish(exchange='', routing_key='rebuild', body=json.dumps(path))
    
    #channel.basic_publish(exchange='', routing_key='rebuild', body=json.dumps(meta_doc))
    print("Path file \""+path+"\" send to RabbitMQ Rebuild channel\n")

    cpt=cpt+1

connection.close()



