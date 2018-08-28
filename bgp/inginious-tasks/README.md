# INGInious task

You'll find in this folder some usefull scripts and example in order to create
an INGInious task on BGP.

The main idea of such task is to simply create a text file describing the network
on which students will have to answer some questions. This text file will then be
parsed in a python script to create and launch an ipmininet network, which will in
turn be uploaded and executed on a virtual machine inside the docker container launched
by INGInious, thanks to a usefull little API.

The file describing the network is in the `public` subfolder and is described 
[here](#Network file). The main reason for that is to be able to use it both in 
the docker container and in the frontend, by presenting the network to the students 
thanks to a javascript graphic library. For now, in the `public` folder there is
only one javascript file alongside the network file, in order to reflect the network 
with which we have to work. In the future this javascript file is supposed to be 
replaced by a proper library that will draw the network.

In the `utils` subfolder are two utilitaries files. The [inginious_utils](utils/iniginious_utils.py)
file contains methods to ease the utilization of the INGInious API. It is of course
not mandatory to use it but the methods found in the second file assume a certain
format of answer, the one given by the methods of this script. There is a complete
description of the methods provided by the file [here](#inginious_utils).
The second file in the subdirectory is [bgp_utils](bgp_utils.py). This python file
contains lots of methods related to BGP, such as a method to parse the network file,
a method to compare the answer of a student with an actual RIB of an AS, ...
Again, you'll find a complete description of the methods [here](#bgp_utils).

Then, in the `scripts` subfolder is a python file containing classes and
methods to ease the use of ipmininet. The parser of the network file produces
code that uses the methods and classes provided in this folder. The files inside
the folder should be uploaded to the VM before trying to launch the network.
We decided to have the file directly in INGInious, and to have to upload it to the
VM each time, instead of putting it directly in the VM. The reason is simply that
it allows a better extensibility of the project: no need to rebuild the VM and
the docker container at each improvement of the scripts or addition of protocols.
[Here](#network_manager) is a description of the `network_manager.py` file.

The other two files, [bgp.py](bgp.py) and the [run file](run) are example files
that are described in the sections [bgp.py](#bgp.py) and [run file](#run file)

Basically, when you submit a task you will have this on the container:

	/
	├── run - The run file
	├── scripts/
	|    ├── bgp.py - The file to create and run the virtual network. Created either
	|    |            by hand or by the method **parse_bgp_file**. It will be uploaded
	|    |            in the VM.
	|    └── network_manager.py - File containing lots of useful methods
	|                             and classes to be used in bgp.py
	├── public/
	|    ├── network - The network file. A text file describing the network.
	|    |		   Can be parsed by the method **parse_bgp_file** to 
	|    |		   generate the file bgp.py
	|    └── shuffle_network.js - File to shuffle and "draw" the network
	|                             described in the network file. Should be 
	|			      replaced by a proper library.
	└── utils/
	     ├── bgp_utils.py - File containing useful methods to work with BGP.
	     └── inginious_utils.py - File containing useful methods to work
	                              with INGInious

## Network file

This simple text file should contain a description of the network topology.
It will be parsed by the method **parse_bgp_file** and by the javascript,
so if you want to extend or modify the format of the file you should modify
those.

The description is fairly simple: you can declare an AS by typing this line
`AS name prefix` where *name* is the name of the as (as1, as2, ...) and *prefix* is
the prefix to be advertised. The name should always be formatted as "as" followed
by the AS number.

You can then create peering between ASes by typing either `SHARED_COST as1 as2`
`PROVIDER_CUSTOMER provider customer` where as1, as2, provider and customer has
to be replaced by the corresponding AS names.

You can also specify that you want to shuffle the network by adding a line containing
`SHUFFLE`. This will shuffle the network for the students (and only the students,
therefore the python file created when parsing the network file will be the same
with or without "SHUFFLE").

## inginious_utils

Here is a complete description of the methods provided by the file 
[inginious_utils.py](utils/iniginious_utils.py). To use these methods add the line 
`from utils import inginious_utils` on the top of the run file.

- **get_single_line_answer(problem_id)**: Return the answer of the student to a 
single line code question identified by *problem_id*. Return "NONE" if the answer 
was "None", otherwise return a list of string which is the answer of the student, 
split by the coma. All the strings are in capital letters.
- **get_multiple_line_answer(problem_id)**: Return the answer of the student to 
a multiple line code question identified by the argument. Return "NONE" if the 
answer was "None", otherwise return a bidimensional list, where the the first list 
is a split of the answer according to new lines, and the second list according to 
comas. (Example: "1,2,3\n4,4,6" will return [[1, 2, 3], [4, 5, 6]])
- **set_problem_result(problem_id, result, fb)**: Set the result and the feedback 
to a problem. *result* should be either "success", "failed" or "crash".
- **shuffle(list_to_shuffle)**: Shuffle a list. This method is used instead of 
the method provided in python in order to be able to shuffle a list in python
and a list in javascript in the exact same way.
- **get_random(i=0, upper=1000)**: Return a random number. *i* is the index of
the element of the random list provided by INGInious. It is necessary for the 
shuffle method since we need multiple random numbers. *upper* is the upper limit
of the random number.

## bgp_utils

Here is a complete description of the methods provided by the file 
[bgp_utils.py](utils/bgp_utils.py). To use this API add the line 
`from utils import bgp_utils`.

- **parse_bgp_file(filename, fileout)**: This method parse the file describing a 
bgp network and write the necessary code to create such a network in the file *fileout*.
It returns a tuple where the first element is the ordered list of the ASes and the
second is the shuffled list of the ASes, if SHUFFLE was in the network file, None
otherwise. This is the method you have to modify if you want to change the way the 
text file describing the network is formated.
- **deshuffle_answer(answer, ordered, shuffled)**: This method replace the
AS names and the prefixes seen by the student by the ones whith which the virtual
network actually ran. Indeed, since we run the virtual network with the configuration
given in the network file, and then we shuffle the ASes and prefixes before showing
it to the students, we need to be able to know which AS seen by the student 
corresponds to which AS in the network. This is done thanks to the list of ASes
ran by the network, *ordered* (that you can retrieve with the method **parse_bgp_file**),
and the list of the shuffled ASes, *shuffled*.
- **get_ribs(file)**: This method takes a python script containing code to create 
and run a virtual network using ipmininet, and return the RIB of each node of the 
network in a dictionnary.
- **compare_best_route(answer, rib, prefix)**: This method check whether the answer 
of the student contains the best route toward a prefix known by the AS to which 
the RIB belongs. If the prefix is not known by the AS the answer should be "None".
*answer* must be a list.
- **compare_all_routes(answer, rib, prefix)**: This method check whether the answer 
of the student contains all the routes toward a prefix known by the AS to which 
the RIB belongs. If the prefix is not known by the AS the answer should be "None".
*answer* must be a bidimensional list.
- **compare_known_prefixes(answer, rib)**: This method check whether the answer 
of the student contains all the prefixes known by the AS to which the RIB belongs. 
If no prefixes are known by the AS the answer should be "None".
*answer* must be a bidimensional list.


## network_manager

This file contains classes and methods used to ease the use of ipmininet.
It is the main file to update if you want to add new fonctionalities to the
ipmininet network that you will create.

For now it contains two classes: **EBGPTopo**, a class to easily creates network
topology running BGP (multiple ASes, each with one router running a BGP daemon),
and **NetworkManager**, a class providing easy to use methods to start, stop
and interact with the network.

**EBGPTopo** is quite simple, it only contains 3 methods: 

- **add_AS(asn, prefixes)**: A method that adds an AS to the topology, advertising
the prefixes given in argument
- **shared_cost_peering(as1, as2)**: A method to peer two ASes following the
shared cost peering principle.
- **provider_customer_peering(provider, customer)**: A method to peer two ASes
following the customer provider principle.

The **NetworkManager** contains a little bit more methods:

- **start_network(self)**: Start the network
- **stop_network(self)**: Stop the network
- **set_topology(self, topo)**: Set the topology to use. Useful to run another
topology after the stopping of the first one.
- **get_all_ribs_per_router(self)**: Retrieve the RIBs of all routers and return
a python dictionary parsed this way: {router1_id: {prefix1: {"primary": 
best_AS_path_list, "secondary": list_of_other_AS_path}, prefix2: "primary":best_AS_path_list,
"secondary": []}, router2_id: {prefix1: ...}}
- **get_all_ribs_per_as(self)**: Same as above but instead of router ids in the
dictionary are the AS name (as1, as2, ...).
- **get_converged_ribs_per_router(self)**: Same as **get_all_ribs_per_router** but 
first wait for BGP to converge.
- **get_converged_ribs_per_as(self)**: Same as **get_all_ribs_per_as** but first
wait for BGP to converge.
- **get_rib(self, node)**: Get the RIB of the router given in argument.

## bgp.py

This file is the file containing the code to create an ipmininet virtual network
and to run it. In the example file it is called *bgp.py* but you can call it
whatever you like.

This file can be created either by hand or by calling the method **parse_bgp_file**,
if a network file is provided. This second method should be prefered as it allows
to draw the network in the frontend by using javascript, but you can write the
script yourself, draw the network by hand in the frontend or provide a file
similar to the network file in the `public` folder for the javascript to draw
the network.

Here is a description if you want to write the script by hand or simply modify
the way the method **parse_bgp_file** works.
To run a simple BGP network, you first have to import the classes and method 
provided in the `scripts` subfolder on the VM. To do so, add the line `from scripts
import *` at the top of the file. Then you have to describe the topology of the 
network to run. You can therefore create an *EBGPTopo* object, that provides basic
methods to easily create a BGP network: **add_AS(asn, prefixes)** that return
an new AS that will advertise the prefixes given, and **shared_cost_peering(as1, as2)**
and **provider_customer_peering(provider, customer)** that creates peering between
two ASes.
If you don't want to create a simple BGP network but a network using iBGP or other
protocols, you should create your own topology by using the API of ipmininet. 
This is described in detailed [here](../README.md).

Once the topology is created, you can run the network and work on it. If you created
a simple BGP network you can use the class **NetworkManager** provided in the 
`scripts` subfolder. To use it, create an **NetworkManager** object by giving it
the topology on which it should work, then call the method **start_network(self)** to
actually start the network. Once started, you can finally work with the network.
You can then interact with the network by using the methods provided by the class.

Once the information is retrieved, you should print it on the standard output to 
retrieve it inside the container (as we use SSH to launch the script from the
container, printing something inside the script will result in SSH catching it).

Finally you can either end the script here, or gracefully stop the network by 
calling the **stop_network(self)** method. This last method allow you to restart
a network with another topology using the **set_topology(self, topology)** method as
long as you have created another topology.

Again, if you want to work on a topology that is not a simple BGP topology, the 
methods above will be of no use to you. You should therefore implement your own
behavior, as explained [here](../README.md).

## run file

Thanks to all the methods explained above, writing a run file has never been 
that easy.

The first thing to do in the run file is to parse the network file describing the
network, which should be in the public folder. Parse it by using the method
**parse_bgp_file** of *bgp_utils*. Catch the output of the method as it return
the list of the ASes of the network, which will be usefull later on to compare
the answers of the students. This call is of course useless if wrote the python
script to launch the network yourself.

Now you should upload the files inside the `scripts` subfolder to the VM, before
trying to upload and launch the network. You can do that by using the 
**upload_file(file)** method of the python package vm_utils inside the container.
(`from inginious.vm import vm_utils`)
The third thing to do is to upload the resulting python file to the VM, to
launch the virtual network and to retrieve some information about it.
This can be all done by a single method call: **get_ribs** from *bgp_utils*,
which will return a dictionary containing all the RIBs, formatted in the format 
described above. Ideally, this information should be stored in some sort of cache 
in order not to have to relaunch the network each time, which takes some time.

You can now finally start working on the answers of the students. Retrieve
their answers either by yourself or by using the methods provided by
*inginious_utils* so that you have them in the correct format for later.
Now before comparing the answers, you have to "deshuffle" them if you shuffled the
network shown to the students: use the **deshuffle_answer** method to do so.

Now compare the answers of the students to the actual RIBs by using the method
of *bgp_utils*.