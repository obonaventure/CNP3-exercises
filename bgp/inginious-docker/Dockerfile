# DOCKER-VERSION 1.1.0

#inherit from the base container, which have all the needed script to launch tasks
FROM    ingi/inginious-c-base

LABEL   org.inginious.grading.name="qemu-Debian-bgp"
	
RUN     yum -y install qemu seabios openssh-clients rsync && \
        yum clean all

RUN     rm /bin/INGInious
ADD     docker-scripts /scripts
RUN     chmod -R 755 /scripts && chmod 700 /scripts/INGInious && \
        cp /scripts/* /bin && rm /bin/vm_utils.py

RUN     chmod -R 644 /scripts/vm_utils.py && \
        mkdir -p /usr/lib/python3.5/site-packages/inginious/vm && \
        cp /scripts/vm_utils.py /usr/lib/python3.5/site-packages/inginious/vm && \
        touch /usr/lib/python3.5/site-packages/inginious/vm/__init__.py && \
        rm -rf /scripts

# Set the VM and ssh config for communication with that VM
ADD     vm /add
RUN     chmod 600 /add/ssh/id_rsa && \
        chmod 644 /add/ssh/id_rsa.pub && \
        chown worker:worker /add/ssh/* && \
        echo StrictHostKeyChecking no >> /etc/ssh/ssh_config