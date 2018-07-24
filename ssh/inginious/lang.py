# -*- coding: utf-8 -*-
#
# This file is part of INGInious. See the LICENSE and the COPYRIGHTS files for
# more information about the licensing of this file.

# init language management

import gettext
import os

import inginious.input
import builtins


def get_lang_dir_path():
    if inginious.DEBUG:
        return "./__lang"
    else:
        return "/task/lang"


def init():
    """ Install gettext with the default parameters """
    if "_" not in builtins.__dict__:  # avoid installing lang two times
        os.environ["LANGUAGE"] = inginious.input.get_lang()
        if inginious.DEBUG:
            gettext.install("messages", get_lang_dir_path())
        else:
            gettext.install("messages", get_lang_dir_path())
