#!/bin/bash

cd /home/
rabbitmq-server &
sleep 4
./scriptrabbit.sh
tail -f /dev/null