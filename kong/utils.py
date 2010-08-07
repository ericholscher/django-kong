import datetime
import StringIO
import sys

from django.conf import settings
from django.core.mail import mail_managers, mail_admins
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from kong.models import Test, TestResult
from twill.parse import execute_string
from twill.errors import TwillAssertionError


def get_latest_results(site):
    """
    This function returns a list of the latest testresult for each test
    defined for a site.
    """
    ret_val = []
    tests = Test.objects.filter(sites=site) | Test.objects.filter(types=site.type)
    for test in tests:
        try:
            result = test.test_results.filter(site=site)[0]
            ret_val.append(result)
        except IndexError:
            #No result for test
            pass
    return ret_val

def execute_test(site, test):
    import twill.commands as commands
    SITE = Site.objects.get_current()
    now = datetime.datetime.now()
    print "trying %s on %s" % (test, site)
    twill_script = test.render(site)
    content = ''
    old_io = sys.stdout
    old_err = sys.stderr
    new_io = StringIO.StringIO()
    #sys.stdout = new_io
    commands.ERR = new_io
    try:
        execute_string(twill_script)
        succeeded = True
        content = new_io.getvalue().strip()
    except Exception, e:
        succeeded = False
        content = new_io.getvalue().strip() + "\n\nException:\n\n" + str(e)
        message = render_to_string('kong/failed_email.txt', {'site': site,
                                                             'test': test,
                                                             'error': content,
                                                             'url': SITE.domain})
        if hasattr(settings, 'KONG_MAIL_MANAGERS'):
            mail_managers('Kong Test Failed: %s (%s)' % (test, site), message)
        if hasattr(settings, 'KONG_MAIL_ADMINS'):
            mail_admins('Kong Test Failed: %s (%s)' % (test, site), message)

    sys.stdout = old_io
    commands.ERR = old_err
    end = datetime.datetime.now()
    duration = end - now
    duration = duration.microseconds

    TestResult.objects.create(site=site,
                              test=test,
                              succeeded=succeeded,
                              duration=duration,
                              content=content)
    return succeeded

def run_tests_for_type(type):
    all_passed = True
    for site in type.all_sites():
        for test in site.tests.all():
            passed = execute_test(site, test)
            all_passed = passed and all_passed

        for test in type.tests.all():
            try:
                passed = execute_test(site, test)
                all_passed = passed and all_passed
            except Exception, e:
                print e
                print "Moving on"
    return all_passed

def run_test_for_type(type, test):
    all_passed = True
    for site in type.all_sites():
        passed = execute_test(site, test)
        all_passed = passed and all_passed
    return all_passed

def run_tests_for_site(site):
    print "Running all tests for site: %s" % site
    all_passed = True
    for test in site.tests.all():
        passed = execute_test(site, test)
        all_passed = passed and all_passed
    return all_passed

def run_test_for_site(site, test):
    return execute_test(site, test)

def run_tests_for_box(box):
    all_passed = True
    for site in box.sites.all():
        passed = run_tests_for_site(site)
        all_passed = passed and all_passed

    return all_passed

def run_test(test):
    print "Running all tests for %s" % test
    sites = test.sites.all()
    types = test.types.all()
    all_passed = True

    #Run test for the sites it points to
    for site in sites:
        passed = execute_test(site, test)
        all_passed = passed and all_passed

    #Run tests for the types of sites it points to
    for type in types:
        passed  = run_test_for_type(type, test)
        all_passed = passed and all_passed

    return all_passed
