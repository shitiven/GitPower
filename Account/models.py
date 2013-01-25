# -*- coding:utf-8 -*-

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete,pre_save
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from Common import ValidationError, regular

import Pull, Depot
import GitPower.settings as settings
import datetime, os, re, time, hashlib, urllib
import Common.gitolite as gitolite


def renderAuthorized(objects):
    '''create authorized_keys file'''
    return     

    sshfile = open("%s/.ssh/authorized_keys"%os.getenv("HOME"), "w")
    sshfile.write("# gitolite start\n")
    for sshkey in objects:
        userfile = '%s_%s'%(sshkey.user.username, sshkey.title)
        sshfile.write('command="%s/bin/gitolite-shell %s",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty %s\n'%(os.getenv("HOME"), userfile, sshkey.content))
    sshfile.write("# gitolite end")
    sshfile.close()


class InviteCode(models.Model):
    '''Invite Code'''

    def render_code():
        return hashlib.md5("incode_code_%s"%str(time.time())).hexdigest()[:10]

    code = models.CharField(u'邀请码', max_length=30, default=render_code, unique=True)
    used = models.BooleanField(u'已使用')
    user = models.ForeignKey(User,blank=True,null=True)


class UserProfile(models.Model):
    '''User Profile'''

    def avatar_filename(instance, filename):
        t,s = os.path.split(filename)
        return hashlib.md5("avatar_%s"%str(time.time()) + s).hexdigest()


    def render_code():
        return hashlib.md5("active_%s"%str(time.time())).hexdigest()


    user     = models.ForeignKey(User, unique=True, verbose_name = u'用户的额外信息', related_name = "profile")
    is_team  = models.BooleanField(default = False)
    owners   = models.ManyToManyField(User, verbose_name=u'管理员', related_name="owners")
    members  = models.ManyToManyField(User, verbose_name=u'开发者', related_name="members")
    reporters = models.ManyToManyField(User, verbose_name=u'报告者', related_name="reporters")
    teams    = models.ManyToManyField(User, verbose_name=u'所属Team', related_name = "team")

    nickname  = models.CharField(u'昵称', max_length=20, unique=True, null=True, blank=True)
    website   = models.URLField(u'网站', null=True, blank=True)
    company   = models.CharField(u'公司', max_length=100, null=True, blank=True)
    city      = models.CharField(u'城市', max_length=100, null=True, blank=True)
    avatar    = models.FileField(upload_to=avatar_filename, blank = True, null = True)

    active_code = models.CharField(u'激活码', max_length=100, default=render_code)


    def gavatar(self, params):
        avatar_url = "http://www.gravatar.com/avatar/"
        avatar_url = avatar_url + hashlib.md5(self.user.email.lower()).hexdigest() + "?"
        return avatar_url + urllib.urlencode(params)


    @property
    def date_joined(self):
        return str(self.user.date_joined.date())


    @property
    def display_name(self):
        if self.is_team or not self.nickname:
            return self.user.username

        return self.nickname


    @property
    def avatar_small(self):
        if not self.avatar:
            return self.gavatar({'s' : '24'})

        return self.avatar + "!24x24"


    @property
    def avatar_normal(self):
        if not self.avatar:
            return self.gavatar({'s' : '45'})

        return self.avatar + "!45x45"


    @property
    def avatar_large(self):
        if not self.avatar:
            return self.gavatar({'s' : '210'})

        return self.avatar + "!210x210"


    @property
    def repos(self):
        '''get user's all project'''
        
        repos = []
        teams = UserProfile.objects.filter(owners__in = [self.user])
        for team in teams:
            repos.extend(Depot.Repo.objects.filter(owner = team.user))

        repos.extend(Depot.Repo.objects.filter(owner = self.user))

        return repos


def rewrite_access(owner):
    return
    repos = Depot.Repo.objects.filter(owner = owner)
    sshkey = SSHKey()
    for repo in repos:
        sshkey.create_access_conf(repo)


@receiver(m2m_changed, sender = UserProfile.owners.through)
def userprofile_owners_change(sender, instance, action, reverse, model, pk_set, **kwargs):
    rewrite_access(instance.user)


@receiver(m2m_changed, sender = UserProfile.members.through)
def userprofile_members_change(sender, instance, action, reverse, model, pk_set, **kwargs):
    rewrite_access(instance.user)


@receiver(post_save, sender=User)
def UserSaved(sender, **kwargs):
    '''create user's profile when user object is saved '''

    saved_user = kwargs["instance"]
    try:
        UserProfile.objects.get(user = saved_user)
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user = saved_user)


@receiver(post_delete, sender=User)
def UserDeleted(sender, **kwargs):
    '''delete the user folder when user is deleted'''

    deleted_user =  kwargs["instance"]
    os.popen('rm -rf %s/%s'%(settings.REPOS_PATH, deleted_user.username))


class SSHKey(models.Model):
    '''sshkey'''

    title    = models.CharField(u'名称', max_length = 30)
    content  = models.TextField(u'key')
    user     = models.ForeignKey(User, verbose_name = '所属用户')
    mac      = models.CharField(u'mac address',max_length=100, blank=True, null=True)
    add_time = models.DateTimeField(default = datetime.datetime.now())


    class Meta:
        unique_together = ("title", "user", )


    def repo_path(self, repo):
        return "%s/%s/%s.git"%(settings.REPOS_PATH, repo.owner.username, repo.name)


    def render_cgl(self):
        '''when sshkey changed recreated access file'''
        return
        user_profile = self.user.get_profile()
        users = [self.user]

        #if the user is team account then filter all members
        users.extend(user_profile.teams.all())
        repos = Depot.Repo.objects.filter(owner__in = users)
        
        for repo in repos:
            self.create_access_conf(repo)


    def get_project_rules(self, repo):
        '''return the project's members rules'''

        #get this project's members
        members = repo.team_writers
        #generate this project rules
        rules = []
        i = 0
        if repo.is_public:
            rules = ["'@all'=>[[1,'R','refs/.*']]"]
            i = 1

        for member in members:  
            sshkeys   = SSHKey.objects.filter(user = member)
            j = 1
            for sshkey in sshkeys:
                rule = "'%s_%s'=>[[%s,'RW+','refs/.*']]"%(sshkey.user.username, sshkey.title, str(i+j))
                rules.append(rule)
                j = j + 1

            i = i + 1

        return rules


    def create_access_conf(self, repo):
        '''create project's access file'''

        rules = self.get_project_rules(repo)
        gitolite.create_access_conf(repo, rules)   


    def delete(self, *args, **kwargs):
        '''delete sshkey and delete the pub file'''

        sshkeys = SSHKey.objects.all().exclude(user = self.user, title = self.title)
        renderAuthorized(sshkeys)

        super(SSHKey, self).delete(*args, **kwargs)
        #when sshkey change recreate access file
        
        self.render_cgl()


    def save(self, *args, **kwargs):
        '''sshkey model saved'''

        #create pub file
        filename = "%s_%s.pub"%(self.user.username, self.title)
        keypath  = "%s/keydir/%s"%(settings.GITLOTE_PATH, filename)
	self.content  = re.match("(^ssh-(?:dss|rsa) [A-Za-z0-9+\/]+)",self.content).group()	

        super(SSHKey, self).save(*args, **kwargs)
        renderAuthorized(SSHKey.objects.all())

        #when sshkey change recreate access file
        self.render_cgl()
