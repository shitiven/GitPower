from django.conf.urls import patterns, include, url
from Pull.views import check_merge_ajax

urlpatterns = patterns('',

	url(r'^check_merge_ajax$', check_merge_ajax),
)
