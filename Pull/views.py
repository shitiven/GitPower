# encoding: utf-8

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from Depot.models import Repo
from Pull.models import PullRequest
from forms import PullForm
from NewsFeed.models import NewsFeed
from Common.templatetags.custom import user_role
import time, git, json, os, datetime

def render(dct, code=200):
    if isinstance(dct, dict):
        dct = json.dumps(dct)
    return HttpResponse(dct, 'application/json ;charset=utf-8', code)

def pull_item(request, owner_username, repo_name, pull_id):
    repo  = get_object_or_404(Repo, owner__username = owner_username, name = repo_name)
    pull  = get_object_or_404(PullRequest, id = pull_id)
    newsfeed = NewsFeed.objects.filter(pull = pull).order_by("-create_date")
    template_context = {
        "repo" : repo,
        "branch" : 'master',
        "current_block" : "pull",
        "pull" :pull,
        "newsfeed" : newsfeed
    }
    template_context.update(request.context)
    return render_to_response("pull/pull.html", context_instance  = RequestContext(request,template_context))
 

def get_pulls(repo, requester = None, current_user = None):
    open_pulls    = PullRequest.objects.filter(repo = repo, stat="open").order_by("-create_date")
    closed_pulls  = PullRequest.objects.filter(repo = repo, stat="closed").order_by("-create_date")
    if requester:
        open_pulls = open_pulls.filter(requester = requester).order_by("-create_date")
        closed_pulls = closed_pulls.filter(requester = requester).order_by("-create_date")

    current_user_pulls_length = 0
    if current_user:
        current_user_pulls_length = PullRequest.objects.filter(repo = repo, requester = current_user).count()

    return {
        "open_pulls" : open_pulls,
        "closed_pulls" : closed_pulls,
        "pulls_length"  : open_pulls.__len__()  + closed_pulls.__len__(),
        "current_user_pulls_length" : current_user_pulls_length
    }


def pulls(request, owner_username, repo_name):
    repo  = get_object_or_404(Repo, owner__username = owner_username, name = repo_name)
    template_context = {
        "repo" : repo,
        "branch" : "master",
        "current_block" : "pull",
        "current_left_menu" : "all"
    }
    current_user = None
    if request.user.is_authenticated():
        current_user = request.user

    template_context.update(get_pulls(repo, current_user = current_user))
    template_context.update(request.context)

    return render_to_response("pull/pulls.html", context_instance  = RequestContext(request,template_context))

@login_required
def your_pulls(request, owner_username, repo_name, requester):
    repo  = get_object_or_404(Repo, owner__username = owner_username, name = repo_name)

    requester = get_object_or_404(User, username = requester)

    template_context = {
        "repo" : repo,
        "branch" : "master",
        "current_block" : "pull",
        "current_left_menu" : "yours"
    }
    current_user = None
    if request.user.is_authenticated():
        current_user = request.user

    template_context.update(get_pulls(repo, requester = requester, current_user = current_user))
    template_context.update(request.context)

    return render_to_response("pull/pulls.html", context_instance  = RequestContext(request,template_context)) 


@login_required
def pull_new(request, username, repo_name):

    repo = get_object_or_404(Repo, owner__username = username, name = repo_name)

    if user_role(request.user, repo) not in ["memeber", "owner"]:
        return render_to_response("pull/deny.html", context_instance = RequestContext(request, {
                "repo" : repo,
                "git_repo" : repo.repo(),
                "branch" : "master"
            }))

    if request.method == "POST":
        form = PullForm(request.POST)
        if form.is_valid():
            pull = form.save(request.user, repo)

            return render({
                "status" : "ok",
                "pull_id" : pull.id
            })
        else:
            return render({
                "status" : "fail",
                "form_errors" : form.errors
            })

    template_context = {
        "repo" : repo,
        "git_repo" : repo.repo(),
        "branch" : "master"
    }

    template_context.update(request.context)

    return render_to_response("pull/request.html", context_instance  = RequestContext(request,template_context))


@login_required
def check_merge_ajax(request):
    merge_action = request.POST.get('merge_action', None)
    repo_id    = request.POST.get('repo_id')
    from_head  = request.POST.get('from_head').replace(" ","").replace("\n","")
    to_head    = request.POST.get('to_head').replace(" ","").replace("\n","")
    pull_id    = request.POST.get('pull_id')

    repo = get_object_or_404(Repo, id = repo_id)
    git_repo = repo.repo()
    tmp_dir  = '/tmp/%s%s'%(repo.name,str(time.time()))
    cl  = git_repo.clone(tmp_dir)
    if to_head == 'master':
        cl.git.execute(['git','checkout','master'])
    else:
        cl.git.execute(['git','checkout','-b',to_head,'origin/%s'%to_head])

    merge_result = None
    try:
        if merge_action:
            try:
                pull_url   = "/%s/%s/pull/%s"%(repo.owner.username, repo.name, pull_id) 
                commit_msg = 'Merge pull request <a href="%s">#%s</a> from %s'%(pull_url, pull_id, from_head)
                result = cl.git.execute(['git','merge','--commit','origin/%s'%from_head])
                result = cl.git.execute(['git','commit','--amend','--author="%s <%s>"'%(request.user.username, request.user.email), '-a', '-m', commit_msg])
                result = cl.git.execute(['git','push','origin',to_head])
                pull = PullRequest.objects.get(id = pull_id)
                pull.stat = "closed"
                pull.save()

                merged_feed = NewsFeed()
                merged_feed.actioner = request.user
                merged_feed.pull = pull
                merged_feed.repo = repo
                merged_feed.pull_merged()

                closed_feed = NewsFeed()
                closed_feed.actioner = request.user
                closed_feed.pull = pull
                closed_feed.repo = repo
                closed_feed.pull_closed()

                return render({
                    "status" : "ok"
                })
            except Exception, e:
                print "-->", str(e)
                return render({
                    "status" : "fail",
                    "error_msg"    : str(e)
                })
        else:
            result = cl.git.execute(['git','merge','origin/%s'%from_head])

        can_auto_merge = True

    except Exception,e:
        print str(e)
        result = str(e)
        can_auto_merge = False

    should_merge = True
    error_msg = ""
    if result.replace(' ','').lower() == 'alreadyup-to-date.':
        should_merge = False
        error_msg    = u'''<span class="label label-inverse">%s</span> 
                            is already up-to-date with 
                            <span class="label label-inverse">%s</span>, 
                            请选择其他分支'''%(to_head, from_head)

    os.popen('rm -rf %s'%tmp_dir)

    from_head   = git_repo.heads[from_head]
    from_commit = from_head.commit.hexsha

    return render({
        "status" : "ok",
        "can_auto_merge" : can_auto_merge,
        "should_merge" : should_merge,
        "commit" : from_commit,
        "error_msg" : error_msg
    })
