# DOCKER-VERSION 1.1.0
FROM    centos

LABEL org.inginious.grading.name="qemu-Debian"

ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8

# Install python, needed for scripts used in INGInious
RUN     yum clean metadata && \
        yum -y install https://centos7.iuscommunity.org/ius-release.rpm && \
        yum -y upgrade && \
        yum -y install python python35u-pip python35u zip unzip tar sed openssh-server openssl bind-utils iproute file qemu seabios openssh-clients && \
        pip3.5 install msgpack-python pyzmq jinja2 PyYAML timeout-decorator && ln -s /usr/bin/python3.5 /usr/bin/python3 && \
        yum clean all

# Allow to run commands
ADD     bin /INGInious/bin
ADD     inginious /INGInious/inginious
RUN     chmod -R 755 /INGInious/bin && \
        chmod 700 /INGInious/bin/INGInious && \
        mv /INGInious/bin/* /bin

# Install everything needed to allow INGInious' python libs to be loaded
RUN     chmod -R 644 /INGInious/inginious && \
        mkdir -p /usr/lib/python3.5/site-packages/inginious && \
        cp -R /INGInious/inginious/*.py  /usr/lib/python3.5/site-packages/inginious && \
        echo "inginious" > /usr/lib/python3.5/site-packages/inginious.pth

# Install locale support
RUN     sed -i "s/override_install_langs=en_US.utf8/#override_install_langs=en_US.utf8/g" /etc/yum.conf && \
        yum -y reinstall glibc-common

# Delete unneeded folders
RUN     rm -R /INGInious

# Set the VM and ssh config for communication with that VM
ADD vm/debian.vdi /add/debian.vdi
ADD vm/id_rsa /root/.ssh/id_rsa
ADD vm/id_rsa.pub /root/.ssh/id_rsa.pub
RUN chmod 600 /root/.ssh/id_rsa
RUN chmod 644 /root/.ssh/id_rsa.pub
RUN echo StrictHostKeyChecking no >> /etc/ssh/ssh_config

CMD ["INGInious"]
