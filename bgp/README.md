# LINGI1341 - BGP exercises

This folder contains all the scripts and files necessary for the exercises on
BGP.

The INGInious exercises are supposed to launch a docker which will launch a 
Debian VM with qemu (hopefully qemu-kvm in the future), which will in turn launch a 
virtual network using `ipmininet`. You will find the VM image here :
https://uclouvain-my.sharepoint.com/:f:/g/personal/silardinois_oasis_uclouvain_be/ElZ4dSYtHntGjRJfAGiSmqwBW0r2Ll72ZuV08-vCImN4KA?e=G3Dpdc


In the `inginious-docker` folder you will find all the necessary files to properly
build the INGInious docker container. As we need to launch qemu at the
container startup, we have to modify the INGInious python script from
the base container to execute qemu at startup, this is done is the `docker-scripts`
subfolder, alongside some scripts to easily interact with the VM.
One important point is the addition of two binaries: **upload-file** and
**execute-command**, which allow to upload a file in the VM and to execute a 
command in the VM, alongside their python equivalent **upload_file(file)** and
**execute_command(command)**, that you can use by adding the line `from inginious.vm
import vm_utils` in your python script.


Finally, in the `inginious-task` folder is an example of INGInious task using
the container built for the project and some utilitary scripts to simplify the work.
You'll find a proper description of the scripts in the [README file](inginious-tasks/README.md).

## Extend the project

TODO