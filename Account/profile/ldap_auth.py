# encoding: utf-8

from Common import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

import ldap, json, re


def ldap_user(username, password):
    
    scope     = ldap.SCOPE_SUBTREE
    ret       = ['mail', 'sN', 'sAMAccountName', 'displayname']

    def filter_ladp(username, password, base):

        filter    = "(&(objectclass=person) (sAMAccountName=%s))" % username 
        try:
            host = re.search("\s*\w+=(\w+)\s*,\s*\w+=(\w+)\s*,\s*\w+=(\w+)",base).groups()
            host = ".".join(host)
            l = ldap.open(host)

            l.protocol_version = ldap.VERSION3
            l.simple_bind_s('%s@%s' % (username, host), password)

            result_id = l.search(base, scope, filter, ret)
            result_type, result_data = l.result(result_id, 0)
            return result_data

        except Exception as e:
            return None 

    ldap_user = username
    username  = username.replace('-', '').replace('.', '')

    result_data = None
    for base in settings.LDAP_BASE:
        result_data  = filter_ladp(username, password, base)
        if result_data:break

    try:
        if(len(result_data) !=1 ):return None

        try:
            mail = result_data[0][1]['mail'][0]
        except:
            mail = "none@mail.com"

        try:
            user = User.objects.get(username__exact=username)
            user.set_password(password)
            if mail:user.mail = mail
            user.save()

        except User.DoesNotExist:

            user = User.objects.create_user(username, mail, password)
            user.is_active = True
            user.save()

        try:
            profile = user.get_profile()
            if not profile.nickname:
                profile.nickname = result_data[0][1]['displayName'][0]
                profile.save()

        except Exception,e:
            pass

        return authenticate(username=username, password=password)

    except Exception as e:
        print str(e)
        return None 
