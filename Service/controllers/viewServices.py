# -*- coding:utf-8 -*-


from Common import *
from Service.models  import DeployService
from Service.decorators import service_creater_required
from forms  import ServiceForm
from django.contrib.auth.decorators import login_required


@service_creater_required
def service_edit(request, service_id):
    '''edit service'''

    service = request.service

    if request.method == "POST":

        request.POST = request.POST.copy()
        request.POST.update({
            "creater" : request.user.id
        })

        form = ServiceForm(request.POST, instance=service, initial={"creater":request.user})
        
        if form.is_valid():
            form.save()

            messages.success(request, "服务修改成功")
            return HttpResponseRedirect(reverse("service_admin")) 
        else:
            form_message(request, form)

    else:
        form = ServiceForm(instance=service)

    context = {
        "form" : form,
        "action" : "edit",
        "service" : service
    }

    return  render("service/form.html", request, context = context)

def service_create(request):
    '''create service'''

    if request.method == "POST":

        request.POST = request.POST.copy()
        request.POST.update({
            "creater" : request.user.id
        })
        
        form = ServiceForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "服务创建成功")
            return HttpResponseRedirect(reverse("service_admin"))

        else:
            form_message(request, form)

    else:

        form = ServiceForm()

    context = {
        "form" : form,
        "action" : "create"
    }

    return  render("service/form.html", request, context = context)

    
@service_creater_required
def service_delete(request, service_id):
    '''delete service'''

    service_id = request.POST.get("service_id")
    service = get_object_or_404(DeployService, id = service_id)
    service.delete()

    messages.success(request, "服务删除成功")

    return HttpResponseRedirect(reverse("service_admin"))

@login_required
def service_admin(request):
    '''admin services'''

    creater  = request.user

    services = DeployService.objects.filter(creater = creater)
    context = {
        "services" : services
    }

    return render("service/admin.html", request, context = context)
