# -*- coding:utf-8 -*-

from Common import User
from Common import models

import GitPower.settings as settings
import datetime

class DeployService(models.Model):
    '''deploy service'''

    call_url    = models.URLField()
    deploy_key  = models.TextField()
    add_time    = models.DateTimeField(default = datetime.datetime.now()) 
    needwrite   = models.BooleanField(default = False)
    method      = models.CharField(max_length = 20)
    name        = models.CharField(max_length = 30, unique = True)
    service_to  = models.CharField(max_length = 100)
    des         = models.TextField()
    creater     = models.ForeignKey(User)