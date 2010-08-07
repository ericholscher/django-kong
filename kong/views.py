# Create your views here.

from kong.models import TestResult, Test
from kong.utils import get_latest_results, execute_test
from kong.models import Site, Type, Server
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import list_detail
import calendar
import itertools

def split_seq(iterable, size):
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))


def get_timestamp(time):
    #return calendar.timegm(time.timetuple()) / 100
    #Need this for flot timestamps..
    return calendar.timegm(time.timetuple()) * 1000

def graph_test(request, test_slug, num_total=5000, div_by=50):
    ret_val = {}
    flot_val = {}
    num_split = int(num_total)/int(div_by)
    test = Test.objects.get(slug=test_slug)
    sites = set(list(test.sites.all()))
    types = test.types.all()
    for type in types:
        for site in type.sites.all():
            sites.add(site)
    for site in sites:
        flot_val[site.slug] = []
        results = get_latest_results(site)
        if ret_val.has_key(site.slug):
            ret_val[site.slug].extend(results)
        else:
            ret_val[site.slug] = results
        tests = TestResult.objects.filter(test=test, site=site)[:num_total]
        duration_tests = list(tests)
        duration_tests.reverse()
        for result_list in split_seq(duration_tests, num_split):
            time = sum([result.duration/1000 for result in result_list])/len(result_list)
            flot_val[site.slug].append([get_timestamp(result_list[0].run_date), time])
    return render_to_response('kong/graph_test.html',
                              {'sites': list(sites),
                               'flot_list': flot_val,
                                'test': test,
                              },
                              context_instance=RequestContext(request))

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

def dashboard(request):
    ret_val = {}
    flot_val = {}
    for site in Site.objects.all():
        results = get_latest_results(site)
        succ = True
        for result in results:
            if not result.succeeded:
                succ = False
                fail = result
        ret_val[site.slug] = succ
    return render_to_response('kong/dashboard.html',
                       {'results': ret_val},
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

def run_test_on_site(request, test_slug, site_slug):
    test = Test.objects.get(slug=test_slug)
    site = Site.objects.get(slug=site_slug)
    execute_test(site, test)
    return test_object_for_site(request, test_slug, site_slug)


def site_list(request):
    qs = Site.objects.all()
    return list_detail.object_list(request, qs)

def site_object(request, site):
    ret_val = {}
    sites = Site.objects.filter(slug=site)
    for site in sites:
        results = get_latest_results(site)
        if ret_val.has_key(site.slug):
            ret_val[site.slug].extend(results)
        else:
            ret_val[site.slug] = results

    return render_to_response('kong/index.html',
                       {'results': ret_val},
                       context_instance=RequestContext(request))

def failed(request):
    ret_val = {}
    flot_val = {}
    results = list(TestResult.objects.filter(succeeded=False)[:20])
    return render_to_response('kong/failed.html',
                       {'results': results,
                        'flot_list': flot_val},
                       context_instance=RequestContext(request))
