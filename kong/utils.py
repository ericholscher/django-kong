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

def _send_error(kong_site, test, content):
    real_site = Site.objects.get_current()
    message = render_to_string('kong/failed_email.txt', {'kong_site': kong_site,
                                                         'test': test,
                                                         'error': content,
                                                         'real_site': real_site})
    if getattr(settings, 'KONG_MAIL_MANAGERS', False):
        mail_managers('Kong Test Failed: %s (%s)' % (test, kong_site), message)
    if getattr(settings, 'KONG_MAIL_ADMINS', False):
        mail_admins('Kong Test Failed: %s (%s)' % (test, kong_site), message)

def _send_recovery(kong_site, test, content):
    real_site = Site.objects.get_current()
    message = render_to_string(
        'kong/recovered_email.txt', {
            'kong_site': kong_site, 
            'test': test, 
            'content': content, 
            'real_site': real_site
        }
    )
    if getattr(settings, 'KONG_MAIL_MANAGERS', False):
        mail_managers('Kong Test Recovered: %s (%s)' % (test, kong_site), message)
    if getattr(settings, 'KONG_MAIL_ADMINS', False):
        mail_admins('Kong Test Recovered: %s (%s)' % (test, kong_site), message)

def execute_test(site, test):
    import twill.commands as commands
    twill_script = test.render(site)
    content = ''
    old_err = sys.stderr
    new_err = StringIO.StringIO()
    commands.ERR = new_err

    now = datetime.datetime.now()
    try:
        execute_string(twill_script)
        succeeded = True
        content = new_err.getvalue().strip()
    except Exception, e:
        succeeded = False
        content = new_err.getvalue().strip() + "\n\nException:\n\n" + str(e)        

    end = datetime.datetime.now()
    duration = end - now
    duration = duration.microseconds
    commands.ERR = old_err
    result = TestResult.objects.create(site=site,
                                       test=test,
                                       succeeded=succeeded,
                                       duration=duration,
                                       content=content)
    
    if result.notification_needed and result.failed:
        _send_error(site, test, content)
    if result.notification_needed and result.succeeded:
        _send_recovery(site, test, content)
    
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
