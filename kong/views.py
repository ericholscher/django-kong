# Create your views here.

from kong.models import TestResult, Test
from kong.utils import get_latest_results
from kong.models import Site, Type, Server
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import list_detail

def index(request):
    ret_val = {}
    for site in Site.objects.all():
        results = get_latest_results(site)
        if ret_val.has_key(site.slug):
            ret_val[site.slug].extend(results)
        else:
            ret_val[site.slug] = results

    return render_to_response('kong/index.html',
                       {'results': ret_val},
                       context_instance=RequestContext(request))

def test_object_for_site(request, test_slug, site_slug):
    test = Test.objects.get(slug=test_slug)
    site = Site.objects.get(slug=site_slug)
    tests = TestResult.objects.filter(test=test, site=site)[:15]
    return render_to_response('kong/testresult_for_site.html',
                       {'results': tests },
                       context_instance=RequestContext(request))
