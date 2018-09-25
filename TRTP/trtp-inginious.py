#!/usr/bin/python3

#
# A python script to create a set of INGINIOUS exercises on
# a simple network protocol. This is intended to let the students
# learn how to decode simple protocol headers
#
# (c) Olivier Bonaventure, UCLouvain, 2018
#
# License: GPLv3, see https://www.gnu.org/licenses/gpl-3.0.en.html

from random import randint, seed
import os,sys 
import zipfile
import yaml
import gettext
_ = gettext.gettext

# testBit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.
# source: https://wiki.python.org/moin/BitManipulation
def testBit(byte, offset):
    mask = 1 << offset
    return(byte & mask)

# setBit() returns an integer with the bit at 'offset' set to 1.
    
def setBit(byte, offset):
    mask = 1 << offset
    return(byte | mask)
   
# clearBit() returns an integer with the bit at 'offset' cleared.

def clearBit(byte, offset):
    mask = ~(1 << offset)
    return(byte & mask)

# toggleBit() returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0.

def toggleBit(byte, offset):
    mask = 1 << offset
    return(byte ^ mask)


#
# byte: the first byte of the packet header 
# type: the type (PTYPE_DATA,PTYPE_ACK,PTYPE_NACK)
def setType(byte, type):
        PTYPE_DATA=1
        PTYPE_ACK=2
        PTYPE_NACK=3
        if(type==PTYPE_DATA):
            byte=clearBit(byte,7)
            byte=setBit(byte,6)
            return byte
        if(type==PTYPE_ACK):
            byte=setBit(byte,7)
            byte=clearBit(byte,6)
            return byte
        if(type==PTYPE_NACK):
            byte=setBit(byte,7)
            byte=setBit(byte,6)
            return byte
        # unknown
        return byte

# byte : the first byte of the packet header    
def setTruncate(byte):
    return setBit(byte,5)

# byte : the first byte of the packet header
# window: the window field
def setWindow(byte, window):
    if( (window<0) or (window>31) ) :
        return byte
    else:
        return ( ( byte & int('0b11100000',2)) | window )

# creates the first four bytes of the packet header and
# returns them as a bytearray
# type: packet type
# truncate: truncate bit
# window: window field
# seq: sequence number
# length: packet length 
def packet(type, truncate, window, seq, length):
    header=bytearray(4)
    header[0]=setType(header[0],type)
    header[0]=setWindow(header[0],window)
    if(truncate and type==1):   # only data can be truncated
        header[0]=setTruncate(header[0])
    header[1]=seq
    header[2]=(length & int('0x0000ff00',16))>> 8
    header[3]=(length & int('0x000000ff',16))
    return header

# inginious helper functions


# the memory limits (unused)
def inginious_limits(memory, output, time):
    ret={}
    ret['memory']=str(memory)
    ret['time']=str(time)
    ret['output']=str(output)
    return ret


# amount: maximum number of submissions (negative for strict limit)
# period: duration (-1) for infinite
def inginious_submission_limit(amount,period):
    ret={}
    ret['amount']=amount
    ret['period']=period
    return ret

# valid: is it a valid choice
# text: the text shown to the students
# feedback: the feedback returned to the student ('' for empty)
def inginious_choice(valid, text, feedback):
    ret={}
    ret['text']=text
    if(valid):
        ret['valid']=valid
    if(feedback!=''):    
        ret['feedback']=feedback
    return ret


# id: the identifier of the question
# name: the name of the question
# context: a restructured text describing the question
# success_msg: message shown in case of success
# success_msg: message shown in case of error
# limit: the number of answers proposed to the student
# choices: a list of possible choices
def inginious_mcq(id,name,context,success_msg,error_msg,limit,choices):
    mcq={}
    mcq['choices']=choices
    mcq['type']='multiple_choice'
    mcq['name']=name
#    mcq['multiple']=True # only if there are several positive answers
    mcq['success_message']=success_msg
    mcq['error_message']=error_msg
    mcq['limit']=limit
    mcq['header']=context
    ret={}
    ret[id]=mcq
    return ret

#
# context: restructured text describing the context of the task
# name: the name of the task
# mcq: a multiple choice question
# tags: should bea list of tags associated to the question
# weight: the weight of the question (floating point number)
# accessible: the duration when the question is accessible, e.g.  2018-09-20 20:05:01/2018-09-27 20:05:05 or True
# limit: maximum number of submissions
def inginious_task(context, name, mcq, weight,accessible,limit):
    ret={}
    ret['accessible']=accessible
    ret['author']='Olivier Bonaventure'
    ret['context']=context
    ret['environment']='mcq'
    ret['evaluate']='best'
    ret['groups']=False
    ret['network_grading']=False
    ret['name']=name
    ret['input_random']='0'
    ret['limits']=inginious_limits(100,2,30)
    ret['problems']=mcq
    ret['stored_submissions']= 0
    ret['submission_limit']=inginious_submission_limit(limit,-1)
    ret['tags']={}
    ret['weight']=weight
    return ret
    
# main

PTYPE_DATA=1
PTYPE_ACK=2
PTYPE_NACK=3
seed()

# return MCQ choices for PTYPE_DATA
def choices_ptype_data():
#Find the PTYPE_DATA in the first byte of a packet
    choices=[]
    for i in range(1,20):
        header=bytearray(1)
        type=randint(1,3)
        header[0]=setType(header[0],type)
        window=randint(0,31)
        header[0]=setWindow(header[0],window)
        if(randint(0,10)<5 and type==PTYPE_DATA):   # only data can be truncated
            header[0]=setTruncate(header[0])
            
        str='{:08b}'.format(header[0])
            
        if(type==PTYPE_DATA) :
            choices.append(inginious_choice(True,str,_('This first byte corresponds to a packet of type PTYPE_DATA')))
        else:
            if(type==PTYPE_ACK):
                choices.append(inginious_choice(False,str,_('This first byte corresponds to a packet of type PTYPE_ACK')))
            else:
                choices.append(inginious_choice(False,str,_('This first byte corresponds to a packet of type PTYPE_NACK')))
    return choices


                
def choices_truncated():
#Find a truncated packet
    
    choices=[]

    for i in range(1,20):

        header=bytearray(1)
        type=PTYPE_DATA
        header[0]=setType(header[0],type)
        window=randint(0,31)
        header[0]=setWindow(header[0],window)
        if(randint(0,10)<5 ):
            truncated=True
            header[0]=setTruncate(header[0])
        else:
            truncated=False
            
        str='{:08b}'.format(header[0])
            
        if(truncated):
            choices.append(inginious_choice(True,str,_('This first byte corresponds to a packet of type PTYPE_DATA that has been truncated')))
        else:
            choices.append(inginious_choice(False,str,_('This first byte corresponds to a packet of type PTYPE_DATA that has *not* been truncated')))
    return choices


def choices_window():
#Find packet with longest window
    
    choices=[]

    for i in range(1,20):

        header=bytearray(1)
        type=PTYPE_ACK
        header[0]=setType(header[0],type)
        window=randint(0,31)
        header[0]=setWindow(header[0],window)
            
        str='{:08b}'.format(header[0])
            
        if(window>22):
            choices.append(inginious_choice(True,str,_('This first byte corresponds to a packet of type PTYPE_ACK with a window of {:d}'.format(window))))
        else:
            choices.append(inginious_choice(False,str,_('This first byte corresponds to a packet of type PTYPE_ACK with a window of {:d}'.format(window))))
    return choices
    
def choices_window_packet():
# Exercise : Find the packet with the largest window 
    choices=[]
    for seq in range(0,20):
        type=PTYPE_ACK
        win=randint(0,31)
        truncate=False
        length=randint(1,511)
        str=''.join('{:02x}'.format(x) for x in packet(type,truncate,win,seq,length))
        if(win>22) :
            choices.append(inginious_choice(True,str,_('This header corresponds to a packet of type PTYPE_ACK with a window of {:d}'.format(win))))
        else:
            choices.append(inginious_choice(False,str,_('This header corresponds to a packet of type PTYPE_ACK with a window of {:d}'.format(win))))
    return choices
    
def choices_ack():
# Exercise : Find packet of type positive ack
    choices=[]
    for i in range(0,20):
        type=randint(1,3)
        win=randint(0,31)
        truncate=False
        if(type==PTYPE_ACK or type==PTYPE_NACK):
            length=0
        else:
            length=randint(1,512)
        seq=randint(1,255)
        str=''.join('{:02x}'.format(x) for x in packet(type,truncate,win,seq,length))
        if(type==PTYPE_ACK) :
            choices.append(inginious_choice(True,str,_('This header corresponds to a packet of type PTYPE_ACK')))
        else:
            if(type==PTYPE_NACK):
                choices.append(inginious_choice(False,str,_('This header corresponds to a packet of type PTYPE_NACK')))
            else:
                choices.append(inginious_choice(False,str,_('This header corresponds to a packet of type PTYPE_DATA'))) 
    return choices

def choices_longest_data():
# Exercise : Find longest packet of type ptype_data
    choices=[]
    for i in range(0,20):
        type=PTYPE_DATA
        win=randint(0,31)
        truncate=False
        length=randint(100,500)
        seq=randint(1,255)
        str=''.join('{:02x}'.format(x) for x in packet(type,truncate,win,seq,length))
        if(length>400) :
            choices.append(inginious_choice(True,str,_('This packet has a length of {:d} bytes'.format(length))))
        else:
            choices.append(inginious_choice(False,str,_('This packet has a length of only {:d} bytes'.format(length))))
    return choices



def choices_truncated_packet():
# Exercise : Find truncated packets
    choices=[]    
    for i in range(0,20):
        type=PTYPE_DATA
        win=randint(0,31)
        if(randint(0,10)>7):
            truncated=True
        else:
            truncated=False
        length=randint(1,512)
        seq=randint(1,255)
        str=''.join('{:02x}'.format(x) for x in packet(type,truncated,win,seq,length))
        if(truncated) :
            choices.append(inginious_choice(True,str,_('This packet has been truncated')))
        else:
            choices.append(inginious_choice(False,str,_('This packet has *not* been truncated')))
    return choices


def choices_valid_packet():
# Exercise : Find the valid packets
    choices=[]    
    for i in range(0,20):
        num=randint(0,10)
        if(num<3) : # valid data packet
            type=PTYPE_DATA
            length=randint(1,512)
            if(randint(0,1)==0):
                truncated=True
            else:
                truncated=False
            seq=randint(1,255)
            win=randint(0,31)
            str=''.join('{:02x}'.format(x) for x in packet(type,truncated,win,seq,length))
            choices.append(inginious_choice(True,str,_('This is a valid packet of type PTYPE_DATA')))
        else:
            if(num<5): # valid ack or nack packet, length of zero
                type=randint(2,3)
                length=0
                truncated=False
                seq=randint(1,255)
                win=randint(0,31)
                str=''.join('{:02x}'.format(x) for x in packet(type,truncated,win,seq,length))
                if(type==PTYPE_ACK):
                    choices.append(inginious_choice(True,str,_('This is a valid packet of type PTYPE_ACK')))
                else:
                    choices.append(inginious_choice(True,str,_('This is a valid packet of type PTYPE_NACK')))
            else: # invalid type
                if(num<7):
                    type=0
                    truncated=False
                    length=randint(1,511)
                    seq=randint(1,255)
                    win=randint(0,31)
                    str=''.join('{:02x}'.format(x) for x in packet(type,truncated,win,seq,length))
                    choices.append(inginious_choice(False,str,_('This packet has an invalid type of 0 ')))
                else:
                    if(num==8):
                        truncated=False
                        type=randint(2,3)
                        length=randint(1,511)
                        seq=randint(1,255)
                        win=randint(0,31)
                        str=''.join('{:02x}'.format(x) for x in packet(type,truncated,win,seq,length))
                        if(type==PTYPE_ACK):
                            choices.append(inginious_choice(False,str,_('This is an invalid packet of type PTYPE_ACK that has a length of {:d}'.format(length))))
                        else:
                            choices.append(inginious_choice(False,str,_('This is an invalid packet of type PTYPE_NACK that has a length of {:d}'.format(length))))
                    else:
                        if(num==9):
                            type=randint(2,3)
                            length=0
                            seq=randint(1,255)
                            win=randint(0,31)
                            truncated=True
                            str=''.join('{:02x}'.format(x) for x in packet(type,truncated,win,seq,length))
                            if(type==PTYPE_ACK):
                                choices.append(inginious_choice(False,str,_('This is an invalid packet of type PTYPE_ACK that has been truncated')))
                            else:
                                choices.append(inginious_choice(False,str,_('This is an invalid packet of type PTYPE_NACK that has been truncated')))

                        else:   
                            type=PTYPE_DATA
                            length=randint(513,16000)
                            seq=randint(1,255)
                            win=randint(0,31)
                            truncated=False
                            str=''.join('{:02x}'.format(x) for x in packet(type,truncated,win,seq,length))
                            choices.append(inginious_choice(False,str,_('This is an invalid packet of type PTYPE_DATA whose length field is longer than 512 ({:d} in this packet)'.format(length))))

    return choices





#########################


def ptype_data_task():
    context_task=_('''
The packet header of our simple protocol has the following format:

.. code-block:: console


     01 2 3 7 8     15 16     23 24    31
    +--+-+---+--------+---------+--------+
    |Ty|T|Win|   Seq  |     Length       |
    |pe|R|dow|   num  |                  |
    +--+-+---+--------+---------+--------+
    |    Timestamp   (4 bytes)           |
    |                                    |
    +------------------------------------+
    |        CRC1  (4 bytes)             | 
    |                                    |
    +------------------------------------+
    |            Payload                 |  
    .                                    . 
    .                                    . 
    +------------------------------------+
    |        CRC2  (4 bytes)             |
    |                                    | 
    +------------------------------------+

In this exercise, we focus on the first byte of this header.
''')
    task_name=_('[TRTP] Identify Packet Types')
    mcq_title=_('Identify the packets of type PTYPE_DATA')
    mcq_description=_('''

The two high order bits of the first byte indicate the packet type. Three packet types are defined in this protocol:
    - PTYPE_DATA (value 1, i.e. 01 in binary) corresponds to data packets
    - PTYPE_ACK (value 2, i.e. 10 in binary) corresponds to acknowledgements
    - PTYPE_NACK (value 3, i.e. 11 in binary) corresponds to negative acknowledgements

In the binary representations below, select the ones that correspond to a data packet.
''')
    q=inginious_task(context_task, task_name,inginious_mcq('test',mcq_title,mcq_description,_('Valid answer'),_('Invalid answer'),4,choices_ptype_data()) , 1.0, True,3)
    os.mkdir("inginious_tasks/ptype_data")
    with open('inginious_tasks/ptype_data/task.yaml', 'w') as outfile:
        yaml.dump(q, outfile, default_flow_style=False)
#print (yaml.dump(q,default_flow_style=False))


def truncated_data_task():
    context_task=_('''
The packet header of our simple protocol has the following format:

.. code-block:: console


     01 2 3 7 8     15 16     23 24    31
    +--+-+---+--------+---------+--------+
    |Ty|T|Win|   Seq  |     Length       |
    |pe|R|dow|   num  |                  |
    +--+-+---+--------+---------+--------+
    |    Timestamp   (4 bytes)           |
    |                                    |
    +------------------------------------+
    |        CRC1  (4 bytes)             | 
    |                                    |
    +------------------------------------+
    |            Payload                 |  
    .                                    . 
    .                                    . 
    +------------------------------------+
    |        CRC2  (4 bytes)             |
    |                                    | 
    +------------------------------------+

In this exercise, we focus on the first byte of this header.
''')
    task_name=_('[TRTP] Identify truncated packets')
    mcq_title=_('Identify the data packets with the truncated bit set')
    mcq_description=_('''

The TR bit in the first byte of our header is set to 1 to indicate that the corresponding packet has been truncated. 

In the binary representations below, select the ones that correspond to a truncated data packet.
''')
    q=inginious_task(context_task, task_name,inginious_mcq('test',mcq_title,mcq_description,_('Valid answer'),_('Invalid answer'),4,choices_truncated()) , 1.0, True,3)
    os.mkdir("inginious_tasks/truncated")
    with open('inginious_tasks/truncated/task.yaml', 'w') as outfile:
        yaml.dump(q, outfile, default_flow_style=False)
#print (yaml.dump(q,default_flow_style=False))

def long_window_task():
    context_task=_('''
The packet header of our simple protocol has the following format:

.. code-block:: console


     01 2 3 7 8     15 16     23 24    31
    +--+-+---+--------+---------+--------+
    |Ty|T|Win|   Seq  |     Length       |
    |pe|R|dow|   num  |                  |
    +--+-+---+--------+---------+--------+
    |    Timestamp   (4 bytes)           |
    |                                    |
    +------------------------------------+
    |        CRC1  (4 bytes)             | 
    |                                    |
    +------------------------------------+
    |            Payload                 |  
    .                                    . 
    .                                    . 
    +------------------------------------+
    |        CRC2  (4 bytes)             |
    |                                    | 
    +------------------------------------+

In this exercise, we focus on the first byte of this header.
''')
    task_name=_('[TRTP] Identify packets with the longest window')
    mcq_title=_('Identify the packets that advertise the longest window ')
    mcq_description=_('''

The five low order bits of the first byte of our header contain the window field. 

In the binary representations below, select the one that contains the longest window field. 
''')
    q=inginious_task(context_task, task_name,inginious_mcq('test',mcq_title,mcq_description,_('Valid answer'),_('Invalid answer'),4,choices_window()) , 1.0, True,3)
    os.mkdir("inginious_tasks/windowbyte")
    with open('inginious_tasks/windowbyte/task.yaml', 'w') as outfile:
        yaml.dump(q, outfile, default_flow_style=False)
#print (yaml.dump(q,default_flow_style=False))


def long_window_packet_task():
    context_task=_('''
The packet header of our simple protocol has the following format:

.. code-block:: console


     01 2 3 7 8     15 16     23 24    31
    +--+-+---+--------+---------+--------+
    |Ty|T|Win|   Seq  |     Length       |
    |pe|R|dow|   num  |                  |
    +--+-+---+--------+---------+--------+
    |    Timestamp   (4 bytes)           |
    |                                    |
    +------------------------------------+
    |        CRC1  (4 bytes)             | 
    |                                    |
    +------------------------------------+
    |            Payload                 |  
    .                                    . 
    .                                    . 
    +------------------------------------+
    |        CRC2  (4 bytes)             |
    |                                    | 
    +------------------------------------+

In this exercise, we focus on the first four bytes of this header.
''')
    task_name=_('[TRTP] Identify packets with the longest window based on the header')
    mcq_title=_('Identify the packets that advertise the longest window ')
    mcq_description=_('''

The five low order bits of the first byte of our header contain the window field. 

In the hexadecimal representations of the first four bytes of packet headers below, select the one that contains the longest window field. 
''')
    q=inginious_task(context_task, task_name,inginious_mcq('test',mcq_title,mcq_description,_('Valid answer'),_('Invalid answer'),4,choices_window_packet()) , 1.0, True,3)
    os.mkdir("inginious_tasks/windowpacket")
    with open('inginious_tasks/windowpacket/task.yaml', 'w') as outfile:
        yaml.dump(q, outfile, default_flow_style=False)
#print (yaml.dump(q,default_flow_style=False))

def ack_packet_task():
    context_task=_('''
The packet header of our simple protocol has the following format:

.. code-block:: console


     01 2 3 7 8     15 16     23 24    31
    +--+-+---+--------+---------+--------+
    |Ty|T|Win|   Seq  |     Length       |
    |pe|R|dow|   num  |                  |
    +--+-+---+--------+---------+--------+
    |    Timestamp   (4 bytes)           |
    |                                    |
    +------------------------------------+
    |        CRC1  (4 bytes)             | 
    |                                    |
    +------------------------------------+
    |            Payload                 |  
    .                                    . 
    .                                    . 
    +------------------------------------+
    |        CRC2  (4 bytes)             |
    |                                    | 
    +------------------------------------+

In this exercise, we focus on the first four bytes of this header.
''')
    task_name=_('[TRTP] Identify acknowledgement packets ')
    mcq_title=_('Identify the packets that are of type PTYPE_ACK ')
    mcq_description=_('''


The two high order bits of the first byte of the header indicate the packet type. Three packet types are defined in this protocol:
    - PTYPE_DATA (value 1, i.e. 01 in binary) corresponds to data packets
    - PTYPE_ACK (value 2, i.e. 10 in binary) corresponds to positive acknowledgements
    - PTYPE_NACK (value 3, i.e. 11 in binary) corresponds to positive acknowledgements


In the hexadecimal representations of the first four bytes of packet headers below, select the one that corresponds to packets of type PTYPE_ACK.  
''')
    q=inginious_task(context_task, task_name,inginious_mcq('test',mcq_title,mcq_description,_('Valid answer'),_('Invalid answer'),4,choices_ack()) , 1.0, True,3)
    os.mkdir("inginious_tasks/ackpacket")
    with open('inginious_tasks/ackpacket/task.yaml', 'w') as outfile:
        yaml.dump(q, outfile, default_flow_style=False)

        

def longest_data_task():
    context_task=_('''
The packet header of our simple protocol has the following format:

.. code-block:: console


     01 2 3 7 8     15 16     23 24    31
    +--+-+---+--------+---------+--------+
    |Ty|T|Win|   Seq  |     Length       |
    |pe|R|dow|   num  |                  |
    +--+-+---+--------+---------+--------+
    |    Timestamp   (4 bytes)           |
    |                                    |
    +------------------------------------+
    |        CRC1  (4 bytes)             | 
    |                                    |
    +------------------------------------+
    |            Payload                 |  
    .                                    . 
    .                                    . 
    +------------------------------------+
    |        CRC2  (4 bytes)             |
    |                                    | 
    +------------------------------------+

In this exercise, we focus on the first four bytes of this header.
''')
    task_name=_('[TRTP] Find the longest data packet')
    mcq_title=_('Find the longest data packet based on protocol headers')
    mcq_description=_('''


The third and fourth bytes of the header contain the Length field. Remember that this field is encoded in network byte order. 


In the hexadecimal representations of the first four bytes of packet headers below, select the one that corresponds to the longest packet. 
''')
    q=inginious_task(context_task, task_name,inginious_mcq('test',mcq_title,mcq_description,_('Valid answer'),_('Invalid answer'),4,choices_longest_data()) , 1.0, True,3)
    os.mkdir("inginious_tasks/longestdatapacket")
    with open('inginious_tasks/longestdatapacket/task.yaml', 'w') as outfile:
        yaml.dump(q, outfile, default_flow_style=False)


def truncated_packet_task():
    context_task=_('''
The packet header of our simple protocol has the following format:

.. code-block:: console


     01 2 3 7 8     15 16     23 24    31
    +--+-+---+--------+---------+--------+
    |Ty|T|Win|   Seq  |     Length       |
    |pe|R|dow|   num  |                  |
    +--+-+---+--------+---------+--------+
    |    Timestamp   (4 bytes)           |
    |                                    |
    +------------------------------------+
    |        CRC1  (4 bytes)             | 
    |                                    |
    +------------------------------------+
    |            Payload                 |  
    .                                    . 
    .                                    . 
    +------------------------------------+
    |        CRC2  (4 bytes)             |
    |                                    | 
    +------------------------------------+

In this exercise, we focus on the first four bytes of this header.
''')
    task_name=_('[TRTP] Find the truncated data packet')
    mcq_title=_('Find the truncated data packet based on protocol headers')
    mcq_description=_('''

The third bit of the first byte of our header indicates whether the packet has been truncated. 

In the hexadecimal representations of the first four bytes of packet headers below, select the one that corresponds to a truncated packet. 
''')
    q=inginious_task(context_task, task_name,inginious_mcq('test',mcq_title,mcq_description,_('Valid answer'),_('Invalid answer'),4,choices_truncated_packet()) , 1.0, True,2)
    os.mkdir("inginious_tasks/truncatedpacket")
    with open('inginious_tasks/truncatedpacket/task.yaml', 'w') as outfile:
        yaml.dump(q, outfile, default_flow_style=False)


def valid_packet_task():
    context_task=_('''
The packet header of our simple protocol has the following format:

.. code-block:: console


     01 2 3 7 8     15 16     23 24    31
    +--+-+---+--------+---------+--------+
    |Ty|T|Win|   Seq  |     Length       |
    |pe|R|dow|   num  |                  |
    +--+-+---+--------+---------+--------+
    |    Timestamp   (4 bytes)           |
    |                                    |
    +------------------------------------+
    |        CRC1  (4 bytes)             | 
    |                                    |
    +------------------------------------+
    |            Payload                 |  
    .                                    . 
    .                                    . 
    +------------------------------------+
    |        CRC2  (4 bytes)             |
    |                                    | 
    +------------------------------------+

In this exercise, we focus on the first four bytes of this header.
''')
    task_name=_('[TRTP] Find the valid packets')
    mcq_title=_('Find the valid packet based on protocol headers')
    mcq_description=_('''

The protocol specification describes the rules that specify which sequences of bytes correspond to a valid and an invalid protocol header. Read these rules carefully and identify the valid packet in the hexadecimal representations of the first four bytes of packet headers below.
''')
    q=inginious_task(context_task, task_name,inginious_mcq('test',mcq_title,mcq_description,_('Valid answer'),_('Invalid answer'),6,choices_valid_packet()) , 1.0, True,-1)
    os.mkdir("inginious_tasks/validpacket")
    with open('inginious_tasks/validpacket/task.yaml', 'w') as outfile:
        yaml.dump(q, outfile, default_flow_style=False)
        

def main():
    os.makedirs("inginious_tasks",exist_ok=True)
    ptype_data_task()
    truncated_data_task()
    long_window_task()
    long_window_packet_task()
    ack_packet_task()
    longest_data_task()
    truncated_packet_task()
    valid_packet_task()
    zf = zipfile.ZipFile("project.zip", "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath("inginious_tasks")
    for dirname, subdirs, files in os.walk(abs_src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]

            zf.write(absname, arcname)
    zf.close()
    



if __name__ == "__main__":
    main()
