This folder contains all the scripts and files necessary for the exercises on
BGP.

The INGInious exercises are supposed to launch a docker which will launch a 
Debian VM with qemu (hopefully qemu-kvm), which will in turn launch a 
virtual network using `ipmininet`. You can download the VM image here :
https://uclouvain-my.sharepoint.com/:f:/g/personal/silardinois_oasis_uclouvain_be/ElZ4dSYtHntGjRJfAGiSmqwBW0r2Ll72ZuV08-vCImN4KA?e=G3Dpdc

In the `ipmininet` folder you will find the scripts used to create and control
an ipmininet virtual network, along with an example of use ([bgp.py](ipmininet/bgp.py)).

In the `vm` folder you will find some necessary files for the VM to work 
properly, such as the ssh keys or some scripts.

## The VM

We use a Debian VM since it is fairly easy to install `ipmininet` on it.
In order for it to work properly it needed some configuration:

- A proper installation of `Quagga` (No need for the services to run)
- A propoer installation of `mininet`
- The sources of `ipmininet` (The scripts provided in the `scripts` folder
	assume the sources of `ipmininet` are located alongside)

We also disabled lots of services on the VM in order for it to boot quickly.
Here is a list of disabled services:

- anacron
- cron
- bluetooth
- bgpd
- isisd
- ospfd
- ospf6d
- pimd
- ripd
- ripngd
- zebra
- syslog
- systemd-timesyncd
- openvswitch-switch
- apt-daily.timer
- apt-daily-upgrade.timer
- anacron.timer
- keyboard-setup

The last one can be usefull if you want to do some debugging on the VM,
you can reactivate it with the command `systemctl enable keyboard-setup`.

The VM is also setup to boot automatically on the root user. So we have no
other users and we deleted the root password.