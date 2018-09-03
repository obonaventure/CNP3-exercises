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

The project architecture is made in such a way that any modification can be done 
pretty easily.

The docker container is already provided with scripts to interact with the VM
(**upload-file** and **execute-command** and their python equivalent) and with 
the actual VM, containing ipmininet. As such, there should be no need to modify 
anything about the container.

All the useful files and API are directly in the INGInious tasks so are easily 
extensible.

### Modify BGP exercises

If you want to modify the way BGP is handled in the task or to add new BGP
functionalities, you should modify the bgp_utils file, located in the utils/ 
subfolder of the tasks. There you'll find the network file parser that you can 
modify to modify the network file, and some other methods to simplify BGP, that
you can modify as well.

You can also modify the file network_manager.py located in the scripts/ subfolder
if you want to add some BGP functionalities to the ipmininet network, this is
explained in the next part as it is similar to add support for a new protocol.

### Adding support for a new protocol

Adding a new protocol to the project is quite simple. There is only one mandatory 
step for you to do, which is to create a file describing the topology of the
ipmininet virtual network and launching it.

As for BGP, there are two ways to create such a file, the easiest one is to directly write
the file using the ipmininet API, and to use this file in your tests.

The second way, is a bit more difficult but when done it would be much
easier to create new exercises with another topology. The idea, as it is done
now for BGP, is to use a network file that will describe the topology, then
parse the file in an ipmininet script, as done by the method **parse_bgp** in
the file utils/bgp_utils.py (note that the parser provided uses the file 
scripts/network_manager.py).

If you want you can also abstract the topology by a class deriving from **IPTopo**, 
as done in the class **EBGPTopo** in the file scripts/network_manager.py, and add 
method to support it in the class **NetworkManager** of the same file, but it is
really not mandatory. At the end, the only thing really needed is to have a working 
ipmininet script.