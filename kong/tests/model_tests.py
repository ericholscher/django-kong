from django.test import TestCase
from django.conf import settings
from django.core import mail
from django.core.management import call_command

from kong.models import Test, Site, TestResult
from kong.utils import execute_test, _send_error

class BasicTests(TestCase):

    fixtures = ['test_data.json']

    def setUp(self):
        self.test_slug = 'front-page'
        self.test = Test.objects.get(slug=self.test_slug)
        self.site = self.test.sites.all()[0]

    def test_results(self):
        self.assertEqual(str(self.site.latest_results()), '[<TestResult: Front Page for ljworld: www2.ljworld.com>]')

    def test_sites(self):
        self.assertEqual(str(self.test.all_sites), '[<Site: ljworld: www2.ljworld.com>]')

    def test_sending_errors(self):
        settings.KONG_MAIL_MANAGERS = True
        _send_error(self.site, self.test, 'Awesome stuffs')
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue('example.com' in mail.outbox[0].body)

    def test_execution(self):
        if getattr(settings, 'KONG_RUN_ONLINE_TESTS', False):
            result = execute_test(self.site, self.test)
            #If this fails because our sites are down, I'm sorry :D
            self.assertTrue(result)
            #TODO: Fix Django so you can check return values here
            #For now we can just manually inspect it.
            call_command('check_sites')
        else:
            print "WARNING: Skipping online tests. Set KONG_RUN_ONLINE_TESTS to True in your settings to run them"

class NotificationTests(TestCase):

    fixtures = ['test_data.json']

    def setUp(self):
        self.test = Test.objects.get(slug='front-page')
        self.site = self.test.sites.all()[0]

        settings.KONG_MAIL_ON_EVERY_FAILURE = False
        settings.KONG_MAIL_ON_RECOVERY = True
        settings.KONG_MAIL_ON_CONSECUTIVE_FAILURES = 1

    def test_mail_on_every_failure(self):

        result = TestResult.objects.create(
            site=self.site,
            test=self.test,
            succeeded=False,
            duration=1,
            content='test'
        )
        self.assertEqual(result.notification_needed, True)

        result = TestResult.objects.create(
            site=self.site,
            test=self.test,
            succeeded=False,
            duration=1,
            content='test'
        )
        self.assertEqual(result.notification_needed, False)

        settings.KONG_MAIL_ON_EVERY_FAILURE = True
        self.assertEqual(result.notification_needed, True)


    def test_mail_on_recovery(self):

        result = TestResult.objects.create(
            site=self.site,
            test=self.test,
            succeeded=False,
            duration=1,
            content='test'
        )
        result = TestResult.objects.create(
            site=self.site,
            test=self.test,
            succeeded=True,
            duration=1,
            content='test'
        )
        self.assertEqual(result.notification_needed, True)

        settings.KONG_MAIL_ON_RECOVERY = False
        self.assertEqual(result.notification_needed, False)


    def test_consecutive_failures(self):

        result = TestResult.objects.create(
            site=self.site,
            test=self.test,
            succeeded=False,
            duration=1,
            content='test'
        )
        self.assertEqual(result.notification_needed, True)

        settings.KONG_MAIL_ON_CONSECUTIVE_FAILURES = 2
        self.assertEqual(result.notification_needed, False)

        result = TestResult.objects.create(
            site=self.site,
            test=self.test,
            succeeded=False,
            duration=1,
            content='test'
        )
        self.assertEqual(result.notification_needed, True)
