# Truncated Reliable Transport Protocol (TRPT)

TRTP is a simple protocol that students implement to learn socket programming in C. It includes some features that force students to parse and generate packet headers, manage timers, manage receive windows, compute CRCs, ... It provides a service similar to [TFTP](https://tools.ietf.org/html/rfc1350), except that it supports the truncation of packets. This has been inspired by [NDP](http://www.cs.ucl.ac.uk/news/article/sigcomm_best_paper_award_for_mark_handley/) that assumes that routers/switches can truncate packets when they are overloaded.

This repository contains :
- a python script that creates [INGINIOUS](https://www.inginious.org) exercises to allow students to learn how to parse packets represented as binary numbers and in hexadecimal format


