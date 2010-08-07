from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),
     (r'^admin/', include(admin.site.urls)),
     url(r'^$', 'kong.views.index', name='kong_index'),
     url(r'index/$', 'kong.views.index', name='kong_index'),
     url(r'^test/(?P<test_slug>.*?)/(?P<num_total>\d+)/(?P<div_by>\d+)/',
         'kong.views.graph_test', name='kong_test'),
     url(r'failed/$', 'kong.views.failed', name='kong_failed'),
     url(r'dashboard/$', 'kong.views.dashboard', name='kong_dashboard'),
     url(r'^tests/(?P<test_slug>.*?)/(?P<site_slug>.*?)/run/', 'kong.views.run_test_on_site', name='kong_run_test_on_site'),
     url(r'^tests/(?P<test_slug>.*?)/(?P<site_slug>.*?)/', 'kong.views.test_object_for_site', name='kong_testresult_for_site'),
     url(r'^sites/(?P<site>.*?)/', 'kong.views.site_object', name='kong_site_detail'),
     url(r'^sites/', 'kong.views.site_list', name='kong_site_list'),


)
