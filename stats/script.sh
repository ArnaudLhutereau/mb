#!/bin/bash

service apache2 start
/etc/init.d/mysql start

hostname -I > /var/www/priv/serveur/serveur.html

mysql -e "CREATE USER 'metablockdb'@'localhost' IDENTIFIED BY 'metablockpassword'"
mysql -e "GRANT ALL PRIVILEGES ON * . * TO 'metablockdb'@'localhost'"
mysql -e "FLUSH PRIVILEGES"
mysql -e "CREATE DATABASE metablock"
mysql -u metablockdb --password=metablockpassword metablock < metablock.sql


tail -f /dev/null