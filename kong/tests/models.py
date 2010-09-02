from django.test import TestCase
from django.conf import settings

from kong.models import Test, Site, TestResult
from kong.utils import execute_test

class SanitizeTest(TestCase):

    fixtures = ['test_data.json']

    def setUp(self):

        self.test = Test.objects.get(slug='front-page')
        self.site = self.test.sites.all()[0]

    def test_results(self):
        self.assertEqual(str(self.site.latest_results()), '[<TestResult: Front Page for ljworld: www2.ljworld.com>]')

    def test_execution(self):
        result = execute_test(self.site, self.test)
        self.assertTrue(result)

    def test_results(self):
        self.assertEqual(str(self.test.all_sites), '[<Site: ljworld: www2.ljworld.com>]')
