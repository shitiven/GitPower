# encoding: utf-8
from celery.task import task
from django.core.mail import EmailMessage

base_template = '''
<html>
<body style="margin:0;padding:0;background:#ccc;">
<div style="padding:40px 0;">
    <div style="width:600px;margin:0 auto;">
        <div style="line-height:50px;background-color:#333;color:#ddd;font-size:18px;">测试标题</div>
        <div style="padding:25px 15px;">
            {{body}}
        </div>
    </div>
</div>
</body>
</html>
'''

action_template = '''
<p style="font-size14px; font-weight:bold; color:#666">{{title}}</p>
'''

comment_template = '''
<p style="border:1px solid #ddd;background:#efefef;padding:10px;color:#333">{{comment}}</p>
'''

only_action_template  = base_template.replace("{{body}}", action_template)
with_comment_template = base_template.replace("{{body}}", action_template+comment_template)


@task(ignore_result=True)
def notify():
    msg = EmailMessage("测试", with_comment_template, "service@gitpower.com", ["z-cool@126.com","xuning@taobao.com","fackweb@gmail.com"])
    msg.content_subtype = "html"
    msg.send()


'''    def active_mail(self, to_mail, active_url):
        title  = u"GitPower激活邮件"
        body   = u"请点击以下链接进行激活: %(active_url)s"%dict(active_url=active_url)
        
        send_mail(title, body, 'service@gitpower.com', [to_mail])'''