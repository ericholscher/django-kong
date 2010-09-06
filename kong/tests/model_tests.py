from django.test import TestCase
from django.conf import settings
from django.core import mail

from kong.models import Test, Site, TestResult
from kong.utils import execute_test, _send_error

class SanitizeTest(TestCase):

    fixtures = ['test_data.json']

    def setUp(self):

        self.test = Test.objects.get(slug='front-page')
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
        if getattr(settings, 'RUN_ONLINE_TESTS', False):
            result = execute_test(self.site, self.test)
            #If this fails because our sites are down, I'm sorry :D
            self.assertTrue(result)
        else:
            print "WARNING: Skipping online tests. Set RUN_ONLINE_TESTS to True in your settings to run them"
