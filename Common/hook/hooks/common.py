#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging

DEBUG = False
logging.basicConfig(filename="/tmp/git-hooks.log", level=logging.DEBUG)

def log(msg):

    if DEBUG: logging.debug(msg)