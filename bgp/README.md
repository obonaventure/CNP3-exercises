This folder contains all the scripts and files necessary for the exercises on
BGP.

The INGInious exercises are supposed to launch a docker which will launch a 
Debian VM with qemu (hopefully qemu-kvm in the future), which will in turn launch a 
virtual network using `ipmininet`. You will find the VM image here :
https://uclouvain-my.sharepoint.com/:f:/g/personal/silardinois_oasis_uclouvain_be/ElZ4dSYtHntGjRJfAGiSmqwBW0r2Ll72ZuV08-vCImN4KA?e=G3Dpdc


In the `vm` folder you will find the ssh keys used to connect to the VM via SSH.
You can also find a python package used to easily create and run ipmininet networks.
For now this package supports simple BGP networks but it can be easily modified
to support other types of network.


In the `inginious-docker` folder you will find all the necessary files to properly
build the INGInious docker container. As we need to launch qemu at the
container startup, we have to modify the INGInious python script from
the base container to execute qemu at startup, this is done is the `docker-scripts`
subfolder, alongside some scripts to easily interact with the VM.


Finally, in the `inginious-task` folder is an example of INGInious task using
the container built for the project and some utilitary scripts to simplify the work.
You'll find a proper description of the API in the [README file](inginious-tasks/README.md).