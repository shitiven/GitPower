# encoding: utf-8
from celery.task import task
from django.core.mail import EmailMessage
from django.conf import settings
from Common import *

base_template = '''
<html>
<body style="margin:0;padding:0;background:#ccc;">
<div style="padding:40px 0;">
    <div style="width:600px;margin:0 auto;">
        <div style="line-height:50px;background-color:#333;color:#ddd;font-size:18px;padding:0 15px;">%(title)s</div>
        <div style="padding:25px 15px;background:#ffffff">
            {{body}}
        </div>
    </div>
</div>
</body>
</html>
'''

action_template = '''
<p style="font-size14px; font-weight:bold; color:#666">%(action)s</p>
'''

comment_template = '''
<p style="border:1px solid #ddd;background:#efefef;padding:10px;color:#333">%(comment)s</p>
'''

only_action_template  = base_template.replace("{{body}}", action_template)
with_comment_template = base_template.replace("{{body}}", action_template+comment_template)


def notify(subject=None, title=None, action=None, comment=None, to_mails=[]):
    mail_data = dict(
        title   = title,
        action  = action,
        comment = comment
    )

    body = only_action_template%mail_data
    if comment:
        body = with_comment_template%mail_data

    for to_mail in to_mails:    
        msg  = EmailMessage(subject, body, "service@gitpower.com", [to_mail])
        msg.content_subtype = "html"
        msg.send()


@task(ignore_result=True)
def account_active(to_mail, active_url):
    subject = u'GitPower激活邮件'
    title   = u'账户激活'
    action  = u'请点击以下链接进行激活: <a href="%(active_url)s" target="_blank">%(active_url)s</a>'%dict(active_url=active_url) 
    to_mails = [to_mail]

    notify(subject=subject, title=title, action=action, to_mails=[to_mail])


@task(ignore_result=True)
def issue_comment(comment):
    '''issue有新评论通知'''

    issue   = comment.issue
    repo    = issue.repo

    subject = u'note for issue #%s'%issue.id
    title   = u'%s'%repo.name
    action  = u'%(author)s left new comment for Issue #%(id)s <a href="%(url)s" target="_blank">%(title)s</a>'%dict(
            id      = issue.id,
            author  = comment.submitter,
            title   = issue.title,
            url     = issue.absolute_url
        )

    notify(subject=subject, title=title, action=action, comment=comment.content, to_mails=comment.subscribers) 


@task(ignore_result=True)
def issue_state_change(comment, state):
    '''issue状态变更通知'''
    issue   = comment.issue
    repo    = issue.repo

    subject = u'note for issue state change'
    title   = u'%s'%repo.name
    action  = u'%(author)s %(state)s the Issue #%(id)s <a href="%(url)s" target="_blank">%(title)s</a>'%dict(
            id      = issue.id,
            author  = comment.submitter,
            url     = issue.absolute_url,
            title   = issue.title,
            state   = state
        )

    notify(subject=subject, title=title, action=action, to_mails=comment.subscribers) 


@task(ignore_result=True)
def issue_assign(issue):
    repo    = issue.repo
    subject = u'note for issue assign to you'
    title   = u'%s'%repo.name
    action  = u'You are assigned the Issue #%(id)s <a href="%(url)s" target="_blank">%(title)s</a>'%dict(
            id    = issue.id,
            url   = issue.absolute_url,
            title = issue.title
        )
    notify(subject=subject, title=title, action=action, to_mails=[issue.assigner.email])


@task(ignore_result=True)
def issue_update(issue):
    repo    = issue.repo
    subject = u'note for issue update'
    title   = u'%s'%repo.name
    action  = u'updated the Issue #%(id)s <a href="%(url)s" target="_blank">%(title)s</a>'%dict(
            id    = issue.id,
            url   = issue.absolute_url,
            title = issue.title
        )
    notify(subject=subject, title=title, action=action, to_mails=issue.subscribers_mail)


@task(ignore_result=True)
def repo_manager(repo, to_mails):
    subject = u'note for be repo manager'
    title   = u'%s'%repo.name
    action  = u'you has be the \'<a href="%(url)s" target="_blank">%(repo)s</a>\' project manager'%dict(
            repo = repo.name,
            url  = repo.absolute_url
        )
    notify(subject=subject, title=title, action=action, to_mails=to_mails)


@task(ignore_result=True)
def repo_manager_remove(repo, to_mails):
    subject = u'note for remove repo manager'
    title   = u'%s'%repo.name
    action  = u'you has remove the \'<a href="%(url)s" target="_blank">%(repo)s</a>\' project manager'%dict(
            repo = repo.name,
            url  = repo.absolute_url
        )
    notify(subject=subject, title=title, action=action, to_mails=to_mails)

