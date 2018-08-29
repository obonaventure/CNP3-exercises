#!/bin/python3
# -*- coding: utf-8 -*-
#
# This file is part of INGInious. See the LICENSE and the COPYRIGHTS files for
# more information about the licensing of this file.

import sys
import subprocess
from inginious import feedback

def error(msg):
    feedback.set_global_result("crash")
    feedback.set_global_feedback(msg)
    exit(0)

def upload_file(file):
    r = subprocess.run(["/bin/upload-file", file], stdout=subprocess.PIPE)
    if r.returncode != 0:
        error("Unable to send the file {} to the VM.".format(file))

def execute_command(command):
    r = subprocess.run(["/bin/execute-command", "{}".format(command)], 
               stdout=subprocess.PIPE)
    if r.returncode != 0:
        error("Unable to execute the file " + file)
    return r.stdout.decode("utf-8")

