FROM ubuntu

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update

RUN apt-get install -y apache2 php mysql-server libapache2-mod-php php-mysql
RUN service apache2 restart

RUN usermod -a -G www-data root
RUN chown -R root:www-data /var/www/

RUN apt-get install -y phpmyadmin
RUN ln -s /usr/share/phpmyadmin/ /var/www/html/phpmyadmin

RUN rm /var/www/html/index.html
COPY ./stats /var/www/html
COPY ./script.sh /home/script.sh
RUN chmod u+x /home/script.sh

EXPOSE 80:80/tcp
EXPOSE 80:80/udp

WORKDIR /var/www/html

ENTRYPOINT /home/script.sh
