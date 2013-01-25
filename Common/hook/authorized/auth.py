#!/usr/bin/python
# -*- coding:utf-8 -*-

from access import filter_users_bykey, log 
import sys, re

SCRIPT_PATH = "/var/openssh/authorized/serve.py"

pubkey = sys.stdin.readline()

if not re.match('^ssh-(?:dss|rsa) [A-Za-z0-9+\/]+$', pubkey):
    log("[ERROR] invalide key")
    exit("[ERROR] invalide key")

try:
    sshkey_objects = filter_users_bykey(pubkey)
except Exception,e:
    log(str(e))

if not sshkey_objects: sys.exit("[Error] GitPower can't find your sshkey, more about: http://www.gitpower.com")

outlines = []

for sshkey in sshkey_objects:
    params = [
        'command="'+ SCRIPT_PATH + ' %s"'%sshkey.user.username,
        'no-port-forwarding',
        'no-X11-forwarding',
        'no-agent-forwarding',
        'no-pty'
    ]
    outlines.append(",".join(params))

sys.stdout.write("\n".join(outlines))
