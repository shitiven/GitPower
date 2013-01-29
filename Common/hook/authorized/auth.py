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

users = []
for sshkey in sshkey_objects:
    users.append(sshkey.user.username)

users = ",".join(users)

log(users)

params = [
    'command="'+ SCRIPT_PATH + ' %s"'%users,
    'no-port-forwarding',
    'no-X11-forwarding',
    'no-agent-forwarding',
    'no-pty'
]
sys.stdout.write(",".join(params))
