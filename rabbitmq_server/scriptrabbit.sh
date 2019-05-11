#!/bin/bash
sleep 3
# PUT
rabbitmqctl add_vhost vhost_put
rabbitmqctl add_user client client
rabbitmqctl set_user_tags client administrator
rabbitmqctl set_permissions -p vhost_put client ".*" ".*" ".*"
sleep 3
# REBUILD
rabbitmqctl add_vhost vhost_rebuild
rabbitmqctl add_user client_rebuild client_rebuild
rabbitmqctl set_user_tags client_rebuild administrator
rabbitmqctl set_permissions -p vhost_rebuild client_rebuild ".*" ".*" ".*"