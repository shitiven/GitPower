#!/usr/bin/python
# -*- coding:utf-8 -*-

from access import filter_users_bykey, log 
import sys, re, os

SCRIPT_PATH = "/home/git/.gitpower/authorized/serve.py"

pubkey = sys.stdin.readline()

try:
    pubkey = re.match("(^ssh-(?:dss|rsa) [A-Za-z0-9+\/]+)", pubkey).group()
except:
    sys.exit(1)

#if not re.match('^ssh-(?:dss|rsa) [A-Za-z0-9+\/]+$', pubkey):
#    log("[ERROR] invalide key")
#    exit("[ERROR] invalide key")

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
