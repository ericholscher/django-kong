# Create your views here.

from kong.models import TestResult, Test
from kong.utils import get_latest_results
from kong.models import Site, Type, Server
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import list_detail
import calendar

def get_timestamp(time):
    #return calendar.timegm(time.timetuple()) / 100
    #Need this for flot timestamps..
    return calendar.timegm(time.timetuple()) * 1000

def index(request):
    ret_val = {}
    flot_val = {}
    for site in Site.objects.all():
        results = get_latest_results(site)
        if ret_val.has_key(site.slug):
            ret_val[site.slug].extend(results)
        else:
            ret_val[site.slug] = results
        for result in results:
            results = list(TestResult.objects.filter(test=result.test, site=result.site)[:50])
            results.reverse()
            flot_val["%s-%s" % (result.site.slug, result.test.slug)] = [[get_timestamp(result.run_date), result.duration/1000] for result in results]

    return render_to_response('kong/index.html',
                       {'results': ret_val,
                        'flot_list': flot_val},
                       context_instance=RequestContext(request))

def test_object_for_site(request, test_slug, site_slug):
    test = Test.objects.get(slug=test_slug)
    site = Site.objects.get(slug=site_slug)
    tests = TestResult.objects.filter(test=test, site=site)[:50]
    duration_tests = list(tests)
    duration_tests.reverse()
    duration_list = [result.duration for result in duration_tests]
    flot_list = [[get_timestamp(result.run_date), result.duration/1000] for result in duration_tests]
    return render_to_response('kong/testresult_for_site.html',
                       {'results': tests,
                        'duration_list': duration_list,
                        'flot_list': flot_list
                        },
                       context_instance=RequestContext(request))
