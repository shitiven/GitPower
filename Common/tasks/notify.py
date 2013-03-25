# encoding: utf-8
from celery.task import task
from django.core.mail import EmailMessage

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
def notify_active(to_mail, active_url):
    subject = u'GitPower激活邮件'
    title   = u'账户激活'
    action  = u'请点击以下链接进行激活: <a href="%(active_url)s">%(active_url)s</a>'%dict(active_url=active_url) 
    to_mails = [to_mail]

    notify(subject=subject, title=title, action=action, to_mails=[to_mail])

