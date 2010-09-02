import calendar
from collections import defaultdict
import itertools

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import list_detail

from kong.models import TestResult, Test
from kong.utils import execute_test
from kong.models import Site, Type

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

def flotify(result):
    results = list(TestResult.objects.filter(test=result.test, site=result.site)[:50])
    results.reverse()
    return [[get_timestamp(result.run_date), result.duration/1000] for result in results]


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
        results = site.latest_results()
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

def _render_to_result_list(request, sites, template_name='kong/index.html'):
    ret_val = defaultdict(list)
    flot_val = {}
    for site in sites:
        results = site.latest_results()
        ret_val[site.slug].extend(results)
        for result in results:
            flot_val["%s-%s" % (result.site.slug, result.test.slug)] = flotify(result)
    return render_to_response(template_name,
                       {'results': ret_val.items(),
                        'flot_list': flot_val},
                       context_instance=RequestContext(request))

def index(request):
    sites = Site.objects.all()
    return _render_to_result_list(request, sites)

def site_detail(request, site_slug):
    sites = Site.objects.filter(slug=site_slug)
    return _render_to_result_list(request, sites)

def test_detail(request, test_slug, pk):
    result = TestResult.objects.get(pk=pk)
    return render_to_response('kong/test_detail.html',
                       {'result': result},
                       context_instance=RequestContext(request))



def dashboard(request):
    ret_val = {}
    for site in Site.objects.all():
        results = site.latest_results()
        succ = True
        for result in results:
            if not result.succeeded:
                succ = False
                fail = result
        ret_val[site.slug] = succ
    return render_to_response('kong/dashboard.html',
                       {'results': ret_val},
                       context_instance=RequestContext(request))

def test_detail_for_site(request, site_slug, test_slug):
    test = Test.objects.get(slug=test_slug)
    site = Site.objects.get(slug=site_slug)
    result = TestResult.objects.filter(test=test, site=site)[0]
    flot_list = flotify(result)
    return render_to_response('kong/test_list_for_site.html',
                       {'result': result,
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

def failed(request):
    ret_val = {}
    flot_val = {}
    results = list(TestResult.objects.filter(succeeded=False)[:20])
    return render_to_response('kong/failed.html',
                       {'results': results,
                        'flot_list': flot_val},
                       context_instance=RequestContext(request))
