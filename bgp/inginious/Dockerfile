# DOCKER-VERSION 1.1.0

FROM    ingi/inginious-c-base

LABEL   org.inginious.grading.name="qemu"

RUN     yum -y install qemu seabios openssh-clients

ADD vm/debian.vdi /add/debian.vdi
ADD vm/ssh/id_rsa /root/.ssh/id_rsa
ADD vm/ssh/id_rsa.pub /root/.ssh/id_rsa.pub
RUN chmod 600 /root/.ssh/id_rsa
RUN chmod 644 /root/.ssh/id_rsa.pub

CMD ["qemu-system-x86_64 -hda /add/debian.vdi -m 1024M -net user,hostfwd=tcp:127.0.0.1:20002-:22 -net nic -vnc 127.0.0.1:6"]