# encoding: utf-8

import os
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.conf import settings    
from django.core.files.storage import Storage
from django.core.files.base import File
from Common.upyun import UpYun,md5,md5file
from django.utils.encoding import force_unicode

class YPStorage(Storage):

    def __init__(self, location = "/", base_url = None):

        if base_url is None:
            base_url = settings.IMAGE_HOST

        self.base_url = base_url
        self.upyun = UpYun(settings.STORE_BUCKET,settings.STORE_USER,settings.STORE_PASSWORD)

    def _open(self, name, mode = "rb"):

        return self.upyun.readFile(name)

    def _save(self, name, content):

        name = self._clean_name(name)
        content.open()
        if hasattr(content, 'chunks'):
            content_str = ''.join(chunk for chunk in content.chunks())
        else:
            content_str = content.read()
        self.upyun.writeFile(name, content_str)
        return name

    def exists(self, name):
        return False

    def size(self, name):
        name = self._clean_name(name)
        info = self.upyun.getFileInfo(name)
        return info["size"]

    def url(self, name):
        name = self._clean_name(name)
        return self.base_url + "/" + name

    def path(self, name):
        name = self._clean_name(name)
        return self.base_url + "/" + name

    def _clean_name(self, name):
        return name
