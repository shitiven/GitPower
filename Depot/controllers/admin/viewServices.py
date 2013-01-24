# -*- coding:utf-8 -*-

from Common import *

from Depot.models  import Repo
from Depot.decorators  import repo_access_required
from Service.models import DeployService


@repo_access_required("owner")
def repo_services_filter(request, username, repo_name):
    '''public to this project's services list'''

    repo     = request.repo
    context  = request.context

    services_show = []
    services = DeployService.objects.all()
    for service in services:
        username = service.service_to.split("/")[0]
        project  = service.service_to.split("/")[1]

        projects = Repo.objects.filter(owner__username__regex=username, name__regex=project)
        if repo in projects:
            if service not in repo.services.all():
                services_show.append(service)

    services_show = list(set(services_show))

    context.update({
        "services" : services_show
    })

    return render("repo/admin/services/filter.html", request, context = context)

@repo_access_required("owner")
def repo_services(request, username, repo_name):
    '''current git project services'''

    repo     = request.repo
    context  = request.context

    services = repo.services.all()

    context.update({
        "services" : services
    })

    return  render("repo/admin/services/service.html", request, context = context) 


@repo_access_required("owner")
def repo_service_add(request, username, repo_name):
    '''add service to project'''

    repo       = request.repo
    context    = request.context
    service_id = request.POST.get("service_id")

    service = get_object_or_404(DeployService, id=service_id)
    repo.services.add(service)

    messages.success(request, "服务添加成功")
    return HttpResponseRedirect(reverse("repo_services_filter", args=[username, repo.name]))


@repo_access_required("owner")
def repo_service_remove(request, username, repo_name):
    '''remove service from project'''

    repo    = request.repo
    context = request.context
    service_id = request.POST.get("service_id")

    service = get_object_or_404(DeployService, id=service_id)
    repo.services.remove(service)

    messages.success(request, "服务移除成功")
    return HttpResponseRedirect(reverse("repo_services", args=[username, repo.name]))

