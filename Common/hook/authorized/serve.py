#!/usr/bin/python
# -*- coding:utf-8 -*-

from access import repo_access, log
import sys, re, os

REPO_DIR = "repositories"


COMMANDS_READONLY = [
    'git-upload-pack',
    'git upload-pack',
    ]


COMMANDS_WRITE = [
    'git-receive-pack',
    'git receive-pack',
    ]

username = sys.argv[1]

def serve(command):
    verb, args = command.split(None, 1)
    if verb == "git":
        try:
            subverb, args = args.split(None, 1)
        except ValueError:
            sys.exit('[ERROR] UnknownCommand')

        verb = '%s %s' % (verb, subverb)

    if (verb not in COMMANDS_WRITE and verb not in COMMANDS_READONLY):
        sys.exit('[ERROR] UnknownCommand')
    
    args = args.replace("'","") 
    access = repo_access(username, re.sub("\.git$","",args))
    
    if not access:
        sys.exit('[ERROR] You do not have any permission for this project')

    if "w" not in access and verb in COMMANDS_WRITE:
        sys.exit('[ERROR] You do not have write permission for this project')


    return verb + " '%(repo_dir)s/%(repo_path)s'"%dict(
            repo_dir=REPO_DIR,
            repo_path=args
        )

cmd = os.environ.get('SSH_ORIGINAL_COMMAND', None)

try:
    newcmd = serve(cmd)
except Exception,e:
    sys.exit("[Error] %s"%str(e))    

os.execvp('git', ['git', 'shell', '-c', serve(cmd)])
