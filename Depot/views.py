# encoding: utf-8

from django.contrib.auth.models import User
from django.utils.encoding import force_unicode
from forms import RepoForm
from Account.models import SSHKey
from django.template.base import VariableDoesNotExist
from models import Repo, DeployService
from Common.gitolite import human_filesize, pygmentize
from Common import *
import GitPower.settings as settings
import os, markdown, json, time, difflib, git


def repo_index(request, username, repo_name):

    repo = get_object_or_404(Repo, owner__username = username, name = repo_name)

    template_context = get_repo_tree(repo, "master", "")
    readme = get_readme(repo,"master")
    if readme is not None:
        template_context.update({
            "readme" : readme
        })

    is_owner = False
    owner_profile = repo.owner.get_profile()

    if request.user.is_authenticated():
        
        if owner_profile.is_team:
            ins = owner_profile.owners.filter(username = request.user.username)
            if ins.__len__():is_owner = True
        else:
            if repo.owner == request.user:
                is_owner = True

    if template_context is not None:
        template_context.update({
            "repo" : repo,
            "is_owner" : is_owner
        })
    else:
        template_context = {
            "repo" : repo,
            "is_owner" : is_owner,
            "is_repo_index" : True,
            "branch" : "master"
        }

    if repo.repo().heads.__len__() < 1:
        template_context.update({
            "blank_repo" : True
        })

    template_context.update({
        "current_page"  : "files",
        "current_block" : "code"
    })

    template_context.update(request.context)
    
    return render_to_response("repo/index.html", context_instance  = RequestContext(request,template_context))


def get_commits(repo, branch, path = None, skip = 0):
    if path is None:
        commits = repo.iter_commits(branch, max_count = 50, skip = skip)
    else:
        commits = repo.iter_commits(rev=branch, paths=path, skip = skip, max_count = 50)

    result = {}
    date_filter = []
    for commit in commits:
        c_date = time.strftime("%Y-%m-%d", time.gmtime(commit.committed_date))
        try:    
            result[c_date].append(commit)
        except:
            date_filter.append(c_date)
            result[c_date] = [commit]

    return {"result":result, "date_filter" : date_filter}


def repo_commits(request, username, repo_name, branch, path):
    repo = get_object_or_404(Repo, owner__username = username, name = repo_name)
    commits = get_commits(repo.repo(), branch, path= path)
    template_context = {
        "repo" : repo,
        "commits" : commits["result"],
        "date_fitler" : commits['date_filter'],
        "git_repo" : repo.repo(),
        "branch" : branch,
        "current_page" : "commits",
        "current_path" : path,
        "current_block" : "code"
    }
    template_context.update(request.context)
    return render_to_response("repo/commits.html", context_instance = RequestContext(request, template_context))


def repo_commit(request, username, repo_name, commit_hexsha, path):

    repo     = get_object_or_404(Repo, owner__username = username, name = repo_name)
    git_repo = repo.repo() 
    commit   = git_repo.commit(commit_hexsha)
    try:
        diffes = commit.parents[0].diff(commit, path, create_patch=True)
    except:
        diffes = commit.diff()

    print diffes[0].diff

    template_context = {
        "repo" : repo,
        "git_repo" : git_repo,
        "current_page" : "commits",
        "branch" : "master",
        "hidden_branches" : True,
        "commit" : commit,
        "current_path" : path,
        "diffes" : diffes,
        "current_block" : "code"
    }

    template_context.update(request.context)

    return render_to_response("repo/commit.html", context_instance = RequestContext(request, template_context))


def fliter_project(request):

    keyword = request.GET.get("keyword")
    if keyword.replace(" ","").__len__() < 1:
        return HttpResponse(json.dumps({"result":[]})) 
    
    if request.user.is_authenticated():
        profile = request.user.get_profile()
        repos    = Repo.objects.filter(name__icontains = keyword, is_public=True)[:20]


    result = {"result":[]}
    for repo in repos:
        result["result"].append({
            "name" : repo.name,
            "des"  : repo.des,
            "owner" : repo.owner.username
        })

    return HttpResponse(json.dumps(result))


@login_required
@csrf_protect
def add_repo(request):

    def gitignores():
        path  = "%s/gitignores/"%settings.TEMPLATE_DIRS[0]

        files = []
        for ps, ds, fs in os.walk(path):
            for f in fs:
                n, x = os.path.splitext(f)
                if x==".gitignore":
                    p = {
                        "name" : f.replace(".gitignore",""),
                        "path" : os.path.join(ps, f).replace(path,""),
                        "value": f.replace(".gitignore","").lower()
                    }
                    files.append(p)

        return files


    sshkeys_len = SSHKey.objects.filter(user = request.user).count()
    if sshkeys_len < 1:
        return render_to_response("error.html", context_instance  = RequestContext(request,{
                "error" : '在创建项目前，请先添加你的 SSH key，<a href="/accounts/settings/sshkey">点击这里</a> 添加。'
        }))

    if request.method == "POST":

        form = RepoForm(request.POST)
        if form.is_valid():
            repo = form.save(commit=False)
            repo.touchreadme = request.POST.get("touchreadme", False)
            repo.gitignore   = request.POST.get("gitignores", None)
            repo.create_repo()
            return HttpResponseRedirect("/%s/%s"%(repo.owner.username, repo.name))

        else:
            form_message(request, form)

    else:
        form = RepoForm()

    owner_teams = []
    profile = request.user.get_profile()
    teams = profile.teams

    for team in teams.all():
        team_profile = team.get_profile()
        for team_owner in team_profile.owners.all():
            if request.user.username == team_owner.username:
                owner_teams.append(team)

    context = {
                "page" : "repo",
                "form"  : form,
                "owner_teams" : owner_teams,
                "gitignores" : gitignores()
    }

    return render('repo/add.html', request, context=context)


def repo_list(request):
    repos = Repo.objects.all().order_by("-add_time")[:10]
    if request.user.is_authenticated():
        sshkeys_len = SSHKey.objects.filter(user = request.user).count()
    else:
        sshkeys_len = 1

    return render_to_response("repo/list.html", context_instance  = RequestContext(request,{
                "page" : "repo",
                "repos"  : repos,
                "sshkeys_len" : sshkeys_len
    }))


def get_readme(repo, branch):
    try:
        tree = repo.repo().tree(branch)
    except:
        return None

    try:
        readme = tree/"README.md"
        readme = readme.data_stream.read()
        readme = force_unicode(readme, 'UTF8')
        return markdown.markdown(readme)
    except Exception,e:
        print str(e)
        return None


def get_repo_tree(repo, branch, path):
    git_repo = None

    try:
        git_repo = repo.repo()
        tree = git_repo.tree(branch)

    except Exception:
        return None

    for element in path.split('/'):
        if len(element):
            tree = tree/element

    submodules = git.Submodule.list_items(git_repo, branch)

    if hasattr(tree, 'mime_type'):
        is_blob = True
    else:
        is_blob = False

    paths = path.split("/")
    paths_str = ['<a href="/%s/%s">%s</a>'%(repo.owner.username, repo.name, repo.name)]
    for p in paths:
        c_p = paths.index(p) + 1
        if c_p < paths.__len__():
            p_c = path.replace(paths[c_p],"")
        else:
            p_c = path
        if c_p  == paths.__len__():
            paths_str.append(p)
        else:
            p_c = "/" + repo.owner.username + "/"  + repo.name + "/tree/" + branch + "/" + "/".join(paths[0:c_p])
            paths_str.append('<a href="%s">%s</a>'%(p_c, p))
    
    try:
        paths.remove("")
    except:
        pass

    template_context = {
        "branch" : branch,
        "path" : ' / '.join(paths_str),
        "prev_path" : "/".join(path.split("/")[0:-1]),
        "tree" : tree,
        "tree_deep" : paths.__len__(),
        "is_blob" : is_blob,
        "master_pull" : True,
        "git_repo" : git_repo,
        "last_commit" : git_repo.commit(branch),
        "current_path" : path,
        "submodules" : submodules,
        "commits" : get_commits(git_repo, branch, path=path)
     }

    if is_blob:
        f,t = os.path.splitext(path)
        md_data = False
        data = tree.data_stream.read()
        if(t.lower() == ".md"): md_data = markdown.markdown(force_unicode(data, 'UTF8'), ['codehilite'])
        template_context.update({
            'data': data,
            'md_data'  : md_data,
            'data_size'  : float(tree.data_stream.size)/1000,
            "data_lines" : data.splitlines().__len__(),
            'file_type'  : t
        })

    return template_context


def repo_tree(request, username, repo_name, branch, path):
    repo = get_object_or_404(Repo, owner__username = username, name = repo_name)
    is_owner = False
    owner_profile = repo.owner.get_profile()

    if request.user.is_authenticated():
        
        if owner_profile.is_team:
            ins = owner_profile.owners.filter(username = request.user.username)
            if ins.__len__():is_owner = True
        else:
            if repo.owner == request.user:
                is_owner = True

    template_context = get_repo_tree(repo, branch, path)

    if template_context is None:
        return HttpResponseRedirect(reverse("repo_index", args = [username, repo_name]))

    template_context.update({
        "repo" : repo,
        "is_owner" : is_owner,
        "current_page" : "files"
    })


    template_context.update({
        "current_block" : "code"
    })

    template_context.update(request.context)

    return render_to_response("repo/index.html", context_instance  = RequestContext(request,template_context))


def repo_tree_ajax(request, username, repo_name):
    repo    = request.repo
    branch  = request.GET.get('branch')
    path    = request.GET.get('path')

    template_context = get_repo_tree(repo, branch, path)

    if template_context is not None:

        template_context.update({
            "repo" : repo
        })

    else:    
        template_context.update({
            "repo" : repo
        })

    return render_to_response("repo/tree.html", context_instance  = RequestContext(request,template_context))