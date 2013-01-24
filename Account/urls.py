from django.conf.urls import patterns, include, url
import settings.views as settings
import profile.views as profile

urlpatterns = patterns('',
    url(r'index$',profile.index),
    url(r'filter$',profile.filter_user),
    url(r'login', profile.login_user),
    url(r'logout', profile.login_out),
    url(r'signup', profile.signup),
    url(r'validate_code', profile.user_to_active, name="validate_code"),
    url(r'user_active', profile.user_active, name="user_active"),

    url(r'settings/sshkey/(\d+)/delete$', settings.sshkey_delete),
    url(r'settings/sshkey$', settings.sshkey, name="settings_sshkey"),

    
    url(r'settings/team/([-_\.\w+]+)/remove_member$', settings.team_remove_member, name="team_remove_member"),
    url(r'settings/team/([-_\.\w+]+)/detele$', settings.team_delete, name="team_delete"),
    url(r'settings/team/([-_\.\w+]+)$', settings.team_members, name="team_members"),
    url(r'settings/team$', settings.team, name = "add_team"),    

    url(r'settings$', settings.index, name="settings_index"),

)
