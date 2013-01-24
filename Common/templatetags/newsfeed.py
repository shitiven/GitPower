# encoding: utf-8
from django import template
from Common.templatetags.custom import timesince
from django.utils.encoding import force_unicode

register = template.Library()

news_temp = {}
news_temp["pull_merged"] = '''
<a href="/{{actioner}}">{{actioner}}</a> merged commit 
<a href="{{commit_url}}">{{commit}}</a> into {{to_head}} from {{from_head}} <cite>{{time_ago}}</cite>
'''

news_temp["pull_closed"] = '''
<a href="/{{actioner}}">{{actioner}}</a> 关闭了该合并请求 <cite>{{time_ago}}</cite>
'''
@register.filter
def news_template(feed):
  global news_temp
  timeago = force_unicode(timesince(feed.create_date),"utf-8")
  tmp = news_temp[feed.news_type]
  tmp = force_unicode(tmp, "utf-8")

  tmp = tmp.replace('{{actioner}}', feed.actioner.username)
  tmp = tmp.replace('{{commit}}', feed.pull.merged_commit_hexsha[:10])
  tmp = tmp.replace('{{to_head}}', feed.pull.to_head)
  tmp = tmp.replace('{{from_head}}', feed.pull.from_head)
  tmp = tmp.replace('{{time_ago}}', timeago)

  return tmp