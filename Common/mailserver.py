# encoding: utf-8

from django.core.mail import send_mail

class MailServer:

    def active_mail(self, to_mail, active_url):
        title  = u"GitPower激活邮件"
        body   = u"请点击以下链接进行激活: %(active_url)s"%dict(active_url=active_url)
        
        send_mail(title, body, 'service@gitpower.com', [to_mail])