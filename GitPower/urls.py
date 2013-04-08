from django.conf.urls import patterns, include, url
from GitPower.views import *
from Depot.views import repo_index
from Depot.views import repo_tree
from Depot.views import repo_commits
from Depot.views import repo_commit
from Depot.views import repo_tree_ajax
from Depot import (
    repo_admin, 
    repo_admin_members,
    repo_admin_members_remove,
    repo_admin_competence,
    repo_rename, 
    repo_delete,
    repo_services,
    repo_service_add,
    repo_service_remove,
    repo_services_filter,
    branch_permission,
    branch_permission_remove
)

from Issues import (
    issue,
    issues,
    issue_comment,
    issue_edit,
    issue_create,
    issue_state_toggle,
    issue_assign_milestone,
    issue_assign_assigner,
    issues_created_by,
    issue_labels_update,
    milestones,
    create_milestone,
    delete_milestone,
    edit_milestone,
    create_label,
    edit_labels
)

from Pull.views import pull_new, pulls, pull_item, your_pulls
import Account.profile.views as profile
import GitPower.settings as settings


urlpatterns = patterns('', )

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

urlpatterns += patterns('',

    url(r'^$', index, name = "index"),
    url(r'^accounts/', include('Account.urls')),
    url(r'^repo/', include('Depot.urls')),
    url(r'^pull/', include('Pull.urls')),
    url(r'^service/', include('Service.urls')),

    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/tree/ajax$', repo_tree_ajax, name = "repo_tree_ajax"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/tree/([-_\.\w+]+)/(.*)$', repo_tree, name = "repo_tree"),

    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/commits/([-_\.\w+]+)/(.*)$', repo_commits, name = "repo_commits"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/commit/(\w+)/(.*)$', repo_commit, name = "repo_commit"),

    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/pull/new$', pull_new, name = "pull_new"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/pulls$', pulls, name = "pulls"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/pulls/(\w+)$', your_pulls, name = "your_pulls"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/pull/(\d+)$', pull_item, name = "pull"),

    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/admin/branch/permission/remove$', branch_permission_remove, name = "repo_branch_permission_remove"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/admin/branch/permission$', branch_permission, name = "repo_branch_permission"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/admin/members/remove$', repo_admin_members_remove, name = "repo_admin_members_remove"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/admin/members$', repo_admin_members, name = "repo_admin_members"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/admin/rename$', repo_rename, name = "repo_rename"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/admin/delete$', repo_delete, name = "repo_delete"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/admin/services$', repo_services, name = "repo_services"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/admin/services/filter$', repo_services_filter, name = "repo_services_filter"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/admin/services/add$', repo_service_add, name = "repo_service_add"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/admin/services/remove$', repo_service_remove, name = "repo_service_remove"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/admin/competence$', repo_admin_competence, name = "repo_admin_competence"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/admin$', repo_admin, name = "repo_admin"),

    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/issues/label/edit$', edit_labels, name = "edit_labels"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/issues/label/create$', create_label, name = "create_label"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/issues/milestones/(\d+)/edit$', edit_milestone, name = "edit_milestone"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/issues/milestones/delete$', delete_milestone, name = "delete_milestone"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/issues/milestones/new$', create_milestone, name = "create_milestone"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/issues/milestones$', milestones, name = "milestones"),

    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/issues/(\d+)/edit$', issue_edit, name = "issue_edit"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/issues/create$', issue_create, name = "issue_create"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/issues/state/toggle$', issue_state_toggle, name = "issue_state_toggle"),

    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/issues/(\d+)/labels/update$', issue_labels_update, name = "issue_labels_update"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/issues/(\d+)/assigner/assign/(\d+)$', issue_assign_assigner, name = "issue_assign_assigner"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/issues/(\d+)/milestone/assign/(\d+)$', issue_assign_milestone, name = "issue_assign_milestone"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/issues/(\d+)/comment$', issue_comment, name = "issue_comment"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/issues/(\d+)$', issue, name = "issue"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/issues/issues_created_by/(\w+)$', issues_created_by, name = "issues_created_by"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/issues$', issues, name = "issues"),
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)/notify$', notify, name="notify"),
    
    url(r'^(\w+)/([-_\.a-zA-Z0-9]+)$', repo_index, name = "repo_index"),
    url(r'^(\w+)$', profile.index, name="profile_index"),

)
