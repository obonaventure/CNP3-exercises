# The VM

We use a Debian VM since it is fairly easy to install `ipmininet` on it.
In order for it to work properly it needed some configuration:

- A proper installation of `Quagga` (No need for the services to run)
- A propoer installation of `mininet`
- The sources of `ipmininet` supporting BGP communities (currently located at https://github.com/slardinois/ipmininet)

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
you can start it with the command `systemctl start keyboard-setup`.

The VM is also setup to boot automatically on the root user. So we have no
other users and we deleted the root password.