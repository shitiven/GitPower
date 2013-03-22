# encoding: utf-8

from django import template
from Account.models import UserProfile
from pygments import highlight 
from pygments.lexers import get_lexer_by_name, PhpLexer 
from pygments.formatters import HtmlFormatter 
from pygments.util import ClassNotFound 
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from Pull.models import PullRequest
from django.utils.encoding import force_unicode

import pygments
import GitPower.settings as settings
import git, re, time, datetime, difflib

register = template.Library()

@register.simple_tag
def assets():
  return re.sub("\/$","",settings.STATIC_URL)


@register.simple_tag
def app_domain():
  return settings.APP_DOMAIN


@register.filter
def is_not_None(val):
    return val is not None


@register.filter
def owner_teams(owner):
  teams = UserProfile.objects.filter(owners__in = [owner])
  return teams 
 
@register.filter 
def highlight_code(code, lang): 
  if code is not None: 
    try: 
      lexer = get_lexer_by_name(lang, encoding='utf-8', stripall=True, startinline=True) 
    except ClassNotFound: 
      lexer = get_lexer_by_name('text') 
    formatter = HtmlFormatter(encoding='utf-8', style='colorful', linenos='table', cssclass='highlight', lineanchors="line") 
    return highlight(code, lexer, formatter)   
  else: 
    return code 


@register.filter
def arrayIndex(arr, item):
  print arr, item
  try:
    arr.index(item)
    print True
    return True
  except:
    print False
    return False


#获取submodule
@register.filter
def get_submodule(element, submodules):
  for sub in submodules:
    
    if sub.path == element.path:
      print dir(sub)
      parttern  = re.compile(":(.*)$")
      try:
        url  = parttern.search(sub.url).groups()[0]
        path = sub.path.split("/")
        return '<a href="/%s">%s</a>'%(url, path[-1])
      except:
        return sub.url

  return None


@register.filter
def code2Css(style, lang):
  lexer = get_lexer_by_name(lang, encoding='utf-8', stripall=True)
  formatter = HtmlFormatter(
          linenos=True,
          encoding='utf-8',
          style = style,
          noclasses="True")
  result = highlight("", lexer, formatter)
  css = formatter.get_style_defs()
  return css


@register.filter
def code2html(code,lang):
  lexer = get_lexer_by_name(lang, encoding='utf-8', stripall=True)
  formatter = HtmlFormatter(
          linenos=True,
          encoding='utf-8',
          style = 'friendly',
          noclasses="False")
  result = highlight(code, lexer, formatter)
  css = formatter.get_style_defs()
  return result


@register.filter
def timesince(dt, default="刚刚", future=False):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """
    dt  = dt.replace(tzinfo=None)
    now = datetime.datetime.utcnow()
    if dt > now:
      diff = dt - now

    else:
      diff = now - dt
    
    periods = (
        (diff.days / 365, "年", "年"),
        (diff.days / 30, "月", "月"),
        (diff.days / 7, "周", "周"),
        (diff.days, "天", "天"),
        (diff.seconds / 3600, "小时", "小时"),
        (diff.seconds / 60, "分钟", "分钟"),
        (diff.seconds, "秒", "秒"),
    )

    for period, singular, plural in periods:
        
        if period:
            if future:
              msg = '%d %s' % (period, singular if period == 1 else plural)
              if dt < now:
                msg = "- "+msg

            else:
              msg = '%d %s 前' % (period, singular if period == 1 else plural)

            return msg

    return default


@register.filter
def push_index(arr):
  i = 0
  for ar in arr:
    ar.index = i
    i = i + 1
    if i%3 == 0:
      ar.row = True

  return arr


@register.filter
def gener_args(path, branch):
  return {
    "path"  : path,
    "branch" : branch 
  }


@register.filter
def last_commit(dic,repo):
  path = dic["path"].encode("utf-8")
  commits = repo.iter_commits(rev=dic['branch'], paths=path)
  commit = list(commits)[0]
  return commit


@register.filter
def last_commit_age(commit):
  date   = time.gmtime(commit.committed_date)
  date   = datetime.datetime.fromtimestamp(time.mktime(date))
  author = commit.author.name.encode("utf-8") 
  return u"[%s] %s"%(author,timesince(date))


@register.filter
def cover_commit_date(commit_date):
  date = time.gmtime(commit_date)
  date = datetime.datetime.fromtimestamp(time.mktime(date))
  return date 


@register.filter
def last_commit_message(commit):
  return commit.message


@register.filter
def filter_commits(date,commits):
  return commits[date]


#截取字符
@register.filter
def cut_str(str, len):
  return str[:int(len)]


#判断是否为tree
@register.filter
def is_tree(name, git_repo):
  branches = []
  tags     = []
  for h in git_repo.branches:
    branches.append(h.name)

  for h in git_repo.tags:
    tags.append(h.name)

  try:
    branches.index(name)
    return "branch: <strong>%s</strong>"%name
  except ValueError:
    try:
      tags.index(name)
      return "tag: <strong>%s</strong>"%name
    except ValueError:
      return "tree: <strong>%s</strong>"%name[:10]
 

#将diff内容转换成HTML格式  
@register.filter
def diff2html(diff):
  lexer = pygments.lexers.get_lexer_by_name("diff")
  def show_diff(seqm, a, b, init= False, delete = False):
    html   = '<table class="diff-code" cellPadding="0"><tbody>'
    c_num  = 1
    p_num  = 1
    for op, a1, a2, b1, b2 in seqm.get_opcodes():
        if op == 'equal':
            for item in a[a1:a2]:
                if delete == False:
                  html += '<tr><td class="num"><span>%s</span></td><td class="num"><span>%s</span></td><td><p class="pre-code">&nbsp;&nbsp;%s</p></td></tr>' % (str(p_num), str(c_num), item)
                  c_num = c_num + 1
                  p_num = p_num + 1

        elif op == 'replace':
            for item in a[a1:a2]:
                if init == False:
                  html += '<tr><td class="num"><span>%s</span></td><td class="num"><span></span></td><td><p class="del pre-code">-%s</p></td></tr>' % (str(p_num), item)
                  p_num = p_num + 1

            for item in b[b1:b2]:
                if delete == False:
                  html += '<tr><td class="num"><span></span></td><td class="num"><span>%s</span></td><td><p class="add pre-code">+%s</p></td></tr>' % (str(c_num), item)
                  c_num = c_num + 1

        elif op == 'insert':
            for item in b[b1:b2]:
                if delete == False:
                  html += '<tr><td class="num"><span></span></td><td class="num"><span>%s</span></td><td><p class="add pre-code">+%s</p></td></tr>' % (str(c_num), item)
                  c_num = c_num + 1

        elif op == 'delete':
            for item in a[a1:a2]:
                if init == False:
                  html += '<tr><td class="num"><span>%s</span></td><td class="num"><span></span></td><td><p class="del pre-code">-%s</p></td></tr>' % (str(p_num), item)
                  p_num = p_num + 1
        else:
            print "<<%s>>" % op

    html += "</tbody></table>"
    return html

  try:
    a_blob_data  = diff.a_blob.data_stream.read()
    delete = False
  except:
    a_blob_data  = ""
    delete = True

  try:
    b_blob_data  = diff.b_blob.data_stream.read()
    init = False
  except Exception, e:
    b_blob_data  = ""
    init = True

  a_blob_lines = a_blob_data.splitlines()

  b_blob_lines = b_blob_data.splitlines()

  a = a_blob_lines
  b = b_blob_lines
  sm= difflib.SequenceMatcher(None, b, a)
  
  html  = show_diff(sm, b,a, init = init, delete = delete)
  return html


@register.filter
def get_pull_length(repo):
  return PullRequest.objects.filter(repo = repo, stat="open").count()


@register.filter
def user_role(user, repo):
  repo_owner_profile = repo.owner.get_profile()
  is_owner  = False
  is_member = False
  if repo_owner_profile.is_team:
      ins = repo_owner_profile.owners.filter(username = user.username)
      mns = repo_owner_profile.members.filter(username = user.username)
      if ins.__len__():is_owner = True
      if mns.__len__():is_member = True
  else:
      if repo.owner == user:
          is_owner = True

  if is_owner:
    return "owner"

  if is_member:
    return "member"

  return None


@register.filter
def user_profile(user, field):
  profile = user.get_profile()
  return getattr(profile, field)

