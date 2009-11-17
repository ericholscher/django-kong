from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),
     (r'^admin/', include(admin.site.urls)),
     url(r'^$', 'kong.views.index', name='kong_index'),
     url(r'index/$', 'kong.views.index', name='kong_index'),
     url(r'^tests/(?P<test_slug>.*?)/(?P<site_slug>.*?)/', 'kong.views.test_object_for_site', name='kong_testresult_for_site'),
)
