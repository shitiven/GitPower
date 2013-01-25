#!/usr/bin/python
# encoding: utf-8

from common import log
import os, sys, subprocess, git, re, time

head = sys.argv[1]
REPOS_PATH = "/home/git/repositories"
PAGES_PATH = "/home/git/pages"

def is_gp_pages():
    '''check head is gp-pages branch'''

    global head
    gp_pages_re = re.compile("heads/gp-pages")
    if gp_pages_re.search(head) is not None:
        return True
    return False


def get_repo_name(rename = True):
    '''get project name and format with {username}_{project_name}'''

    name = os.getcwd()
    name = name.replace(REPOS_PATH+"/","")
    if rename:
        name = name.replace("/","_")
    return name


def update_pages(repo_name):
    pages_dir = PAGES_PATH+"/"+repo_name.replace(".git","").lower()

    #if pages exits git pull to update else clone new pages
    if os.path.isdir(pages_dir):
	os.popen("cd %s && env -i git pull"%pages_dir)
    else:
        os.execvp('git', ['git','clone', os.getcwd(), '-b', 'gp-pages', pages_dir])
    
repo_name = get_repo_name(rename=False)
#if is gp-pages branch then update
if is_gp_pages:
    update_pages(repo_name)    
