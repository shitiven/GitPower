# -*- coding:utf-8 -*-

from django.shortcuts  import render_to_response, redirect, get_object_or_404
from django.http       import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib    import messages
from django.core.urlresolvers   import reverse
from django.contrib.auth.models import User
from django.utils.encoding      import force_unicode
from django.contrib.auth.decorators import login_required
from django.db import models
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext, loader
from django.core.exceptions import ValidationError

import inspect, os, sys, re, json

#the form regular
regular = {
    "reponame" : re.compile('^[a-zA-Z]+[-_\.a-zA-Z0-9]+$'),
    "username" : re.compile('^[a-zA-Z]+[-_\.a-zA-Z0-9]+$')
}

def form_message(request, form):
    '''insert form error into messages'''
    
    for field in form.fields:
        for error in form[field].errors:
            field_label = force_unicode(form[field].label,"utf-8")
            field_error = force_unicode(error,"utf-8")

            field_message = "<strong>%s:</strong> %s"%(field_label, field_error)
            field_message = force_unicode(field_message, "utf-8")

            messages.error(request, field_message)
    
    messages.error(request, form.errors.get("__all__"))


def render(template, request, context = {}):
    
    return render_to_response(template, context_instance  = RequestContext(request, context))

def render_json(dct, code=200):
    if isinstance(dct, dict):
        dct = json.dumps(dct)

    return HttpResponse(dct, 'application/json ;charset=utf-8', code)

def render_to_403(*args, **kwargs):    

    if not isinstance(args,list):        
        args = []        
        args.append('403.html')             

    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}         
    response = HttpResponseForbidden(loader.render_to_string(*args, **kwargs), **httpresponse_kwargs)  


__all__ = [ name for name, obj in locals().items()
            if not (name.startswith('_')) ]