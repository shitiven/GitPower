# -*- coding:utf-8 -*-

from Account.models import *
from pygments.util import ClassNotFound
from django.utils.safestring import mark_safe
import GitPower.settings as settings 
import os, time, re
import math
import pygments
import pygments.lexers as lexers
import pygments.formatters as formatters

def create_repo(owner, repo_name):
    path = "%s/%s/%s.git"%(settings.REPOS_PATH, owner.username, repo_name)
    if os.path.exists(path) is False:
        os.makedirs(path)
    os.popen('%s init --bare %s'%(settings.GIT_PATH, path))

    owner_profile = owner.get_profile()

    if owner_profile.is_team:
        
        members = owner_profile.members.all()

    else:

        members = [owner]
    
    for member in members:
        create_gl_conf(repo_name, member)

def _render_authorized_content(key_name, key_content):
    '''get authorized_keys content format with gitolite'''
    return
    content = "command=\"%s/bin/gitolite-shell %s\","\
              "no-port-forwarding,no-X11-forwarding,"\
              "no-agent-forwarding,no-pty %s\n"%(os.getenv("HOME"), key_name, key_content)

    return content


def append_authorized_key(key_name, key_content):
    '''append sshkey content to authorized_keys'''
    return
    content = _render_authorized_content(key_name, key_content)
    
    authorized_keys_file = "%s/.ssh/authorized_keys"%os.getenv("HOME")

    os.popen("echo '%s' >> %s"%(content, authorized_keys_file))


def create_access_conf(repo, rules):
    '''create project access conf file'''
    return
    repo_path = "%s/%s/%s.git"%(settings.REPOS_PATH, repo.owner.username, repo.name)
    conf_path = "%s/gl-conf"%repo_path

    conf = open(conf_path, "w")
    conf.write("%one_repo = (\n")
    conf.write("'%s/%s' => {\n"%(repo.owner.username, repo.name))
    conf.write(",\n".join(rules))
    conf.write("\n}\n);")
    conf.close()


def create_sshkey_file(filepath, content):
    return
    keyfile = open(filepath,"w")
    keyfile.write(content)
    keyfile.close()


def human_filesize(bytes):
    bytes = int(bytes)
    if bytes is 0:
        return '0 bytes'
    log = math.floor(math.log(bytes, 1024))
    return "%0.2f %s" % (bytes / math.pow(1024, log), ['bytes', 'kb', 'mb', 'gb', 'tb'][int(log)])


def unescape_amp(text):
    return text.replace('&amp;', '&')


class NakedHtmlFormatter(formatters.HtmlFormatter):
    def wrap(self, source, outfile):
        return self._wrap_code(source)
    def _wrap_code(self, source):
        for i, t in source:
            yield i, t


def pygmentize(mime, blob):
    try:
        lexer = lexers.get_lexer_for_mimetype(mime)
    except ClassNotFound:
        try:
            lexer = lexers.get_lexer_by_name(mime)
        except:
            lexer = lexers.get_lexer_by_name('text')
        
    pygmented_string = pygments.highlight(blob, lexer, NakedHtmlFormatter())
    pygmented_string = unescape_amp(pygmented_string)
    
    return mark_safe(pygmented_string)
