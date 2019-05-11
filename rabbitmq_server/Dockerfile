FROM ubuntu

# Update
RUN apt-get update


# Software
RUN apt-get install -y python
RUN apt-get install -y rabbitmq-server


COPY ./start.sh /home/start.sh
RUN chmod +x /home/start.sh
COPY ./scriptrabbit.sh /home/scriptrabbit.sh
RUN chmod +x /home/scriptrabbit.sh


# Launch
ENTRYPOINT /home/$USER/start.sh