from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),
     (r'^admin/', include(admin.site.urls)),

     url(r'^$', direct_to_template, {'template': 'index.html'}, name='kong_home'),
     url(r'^index/$', 'kong.views.index', name='kong_index'),

     url(r'^sites/(?P<site_slug>.*?)/', 'kong.views.site_object', name='kong_site_detail'),
     url(r'^sites/', 'kong.views.site_list', name='kong_site_list'),

     url(r'^tests/(?P<id>\d+)/', 'kong.views.testresult_detail', name='kong_testresult_detail'),
     url(r'^tests/(?P<test_slug>.*?)/(?P<site_slug>.*?)/', 'kong.views.test_object_for_site', name='kong_testresult_for_site'),
     url(r'^tests/(?P<test_slug>.*?)/', 'kong.views.test_object', name='kong_test_list'),
     url(r'^tests/', 'kong.views.test_list', name='kong_testresult_list'),


     url(r'^types/(?P<type_slug>.*?)/', 'kong.views.type_object', name='kong_type_detail'),
     url(r'^types/', 'kong.views.type_list', name='kong_type_list'),

     url(r'^servers/(?P<server_slug>.*?)/', 'kong.views.server_object', name='kong_server_detail'),
     url(r'^servers/', 'kong.views.server_list', name='kong_server_list'),

)
