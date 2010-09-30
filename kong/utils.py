import datetime
import StringIO
import sys

from django.conf import settings
from django.core.mail import mail_managers, mail_admins
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

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
    #Avoid circular import
    from kong.models import TestResult
    twill_script = test.render(site)
    content = ''
    old_err = sys.stderr
    new_err = StringIO.StringIO()
    commands.ERR = new_err

    now = datetime.datetime.now()
    try:
        if getattr(settings, 'KONG_RESET_BROWSER', False):
            execute_string(twill_script, no_reset = False)
        else:
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

