# -*- coding:utf-8 -*-

from Common import User, models, reverse

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.conf import settings
from Service.models import DeployService

import Common.tasks.notify as notify
import datetime, os, git, time
import Account


REPOS_PATH   = settings.REPOS_PATH


class Repo(models.Model):
    name      = models.CharField(u'项目名称', max_length = 30)
    owner     = models.ForeignKey(User, verbose_name="拥有者")
    des       = models.CharField(u'描述', max_length = 200)
    add_time  = models.DateTimeField(default = datetime.datetime.now())
    is_public = models.BooleanField(default = True)
    services  = models.ManyToManyField(DeployService)
    issues_init = models.BooleanField(default = False)
    managers    = models.ManyToManyField(User, related_name="repo_managers", null=True,blank=True)
    developers  = models.ManyToManyField(User, related_name="repo_developers", null=True, blank=True)
    reporters   = models.ManyToManyField(User, related_name="repo_reporters",null=True, blank=True)
    subscribers = models.ManyToManyField(User, related_name="repo_subscribers", null=True, blank=True)
    touchreadme = False
    gitignore   = None
    is_edit     = False


    class Meta:
        unique_together = ("name", "owner",)


    @property
    def team_writers(self):
        writers = self.alldevelopers
        writers.extend(self.allowners)
        return list(set(writers))


    @property 
    def team_readers(self):
        readers = self.team_writers
        readers.extend(self.allreporters)
        return list(set(readers))


    @property
    def team_owners(self):
        return list(self.owner.get_profile().owners.all())


    @property 
    def team_developers(self):
        return list(self.owner.get_profile().members.all())


    @property 
    def team_reporters(self):
        return list(self.owner.get_profile().reporters.all())


    @property
    def is_team_owner(self):
        return self.owner.get_profile().is_team


    @property 
    def repo_owners(self):
        return list(self.managers.all())


    @property 
    def repo_developers(self):
        return list(self.developers.all())


    @property 
    def repo_reporters(self):
        return list(self.reporters.all())


    @property
    def alldevelopers(self):
        members = list(self.owner.get_profile().members.all())
        members.extend(self.repo_developers)
        if members is None:return []
        return list(set(members))


    @property 
    def allreporters(self):
        reporters = list(self.owner.get_profile().reporters.all())
        reporters.extend(self.repo_reporters)
        if reporters is None:return []
        return list(set(reporters))


    @property 
    def allowners(self):
        owners = list(self.owner.get_profile().owners.all())
        owners.extend(self.repo_owners)
        if self.owner.get_profile().is_team == False:
            owners.extend([self.owner])

        if owners is None:return []
        return list(set(owners))


    @property 
    def absolute_url(self):
        return settings.APP_URL + reverse("repo_index", args=[self.owner.username, self.name])


    def repo(self):
        '''return gitPython init project'''

        return git.Repo(self.repo_path())


    def repo_path(self):
        '''return git project working dir'''

        owner_name = self.owner.username
        repo_name  = self.name
        return "%s/%s/%s.git"%(REPOS_PATH, owner_name, repo_name)


    def create_split_conf(self):
        '''create gitolite.conf-compiled.pm, this is the gitolite rules'''
        return
        

    def create_repo(self):
        '''create the git project'''

        repo_path = self.repo_path()

        #the check and create folders for the project
        if os.path.exists(repo_path) is False:
            os.makedirs(repo_path)

        #initialize GitPython with a bare repository
        repo = git.Repo.init(repo_path, bare = True)

        #link the project's hooks to the default hooks
        os.popen('ln -s %s/common.py %s/hooks/common.py'%(settings.GIT_HOOKS_DIR, repo_path))
        os.popen('ln -s %s/post-update %s/hooks/post-update'%(settings.GIT_HOOKS_DIR, repo_path))
        os.popen('ln -s %s/update %s/hooks/update'%(settings.GIT_HOOKS_DIR, repo_path))

        #clone project to tmp folder
        cl_path = '/tmp/%s%s'%(self.name, time.time())
        cl_repo = repo.clone(cl_path)

        #create README.md and push to remote
        if self.touchreadme:

            os.popen("echo README >> %s/README.md"%cl_path)

            if self.gitignore is not None:
                try:
                    gitignore   = open("%s/gitignores/%s"%(settings.TEMPLATE_DIRS[0], self.gitignore))
                    gitigonre_f = open("%s/.gitignore"%cl_path,"w")
                    gitigonre_f.write(gitignore.read())
                    gitigonre_f.close()
                except:
                    pass

            cl_repo.git.execute(['git', 'add', '*'])
            cl_repo.git.execute(['git', 'commit', '--author=%s <%s>'%(self.owner.username, self.owner.email), '-v', '-a', '-m', 'init'])        
            cl_repo.git.execute(['git', 'push', 'origin', 'master'])

            os.popen('rm -rf %s'%cl_path)
            

    def rename(self, new_name, *args, **kwargs):
        '''rename the project'''

        source_path = self.repo_path()
        target_path = source_path.replace(self.name + ".git", new_name + ".git")

        #mv project folder to new folder
        os.popen("mv %s %s"%(source_path, target_path))

        #save the data
        self.name = new_name
        super(Repo, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        '''create project and save data to the database'''

        self.create_repo()
        sshkey = Account.models.SSHKey()

        super(Repo, self).save(*args, **kwargs)

        sshkey.create_access_conf(self)
        self.create_split_conf()

    def delete(self, *args, **kwargs):
        '''delete the project'''

        os.popen("rm -rf %s"%self.repo_path())

        super(Repo, self).delete(*args, **kwargs)


@receiver(m2m_changed, sender=Repo.managers.through)
def handler(sender, instance, action, reverse, model, pk_set, **kwargs):
    
    users = User.objects.filter(id__in = pk_set)

    if action == "post_add":
        for user in users:
            instance.subscribers.add(user)
            notify.repo_manager.delay(instance, [user.email])

    else:
        for user in users:
            instance.subscribers.remove(user)
            notify.repo_manager_remove.delay(instance, [user.email])

                

class BranchPermission(models.Model):
    repo   = models.ForeignKey(Repo, unique=True)
    branch = models.CharField(max_length=50)
    users  = models.ManyToManyField(User)   


    class Meta:
        unique_together = ("repo", "branch")


    def has_permission(self, user):
        print user

