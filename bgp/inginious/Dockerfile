# DOCKER-VERSION 1.1.0

#inherit from the base container, which have all the needed script to launch tasks
FROM    ingi/inginious-c-base

LABEL   org.inginious.grading.name="qemu-Debian-bgp"
	
RUN     yum -y install qemu seabios openssh-clients rsync && \
        yum clean all

RUN     rm /bin/INGInious
ADD     docker-scripts /scripts
RUN     chmod -R 755 /scripts && chmod 700 /scripts/INGInious && \
        mv /scripts/* /bin && rm -rf /scripts

# Set the VM and ssh config for communication with that VM
ADD     vm /add
RUN     chmod 600 /add/ssh/id_rsa && \
        chmod 644 /add/ssh/id_rsa.pub && \
        chown worker:worker /add/ssh/* && \
        echo StrictHostKeyChecking no >> /etc/ssh/ssh_config