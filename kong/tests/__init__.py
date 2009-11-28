from django.test.testcases import TestCase
from django.template import Context, Template
from django.contrib.auth.models import User
from django.conf import settings
import logging, os, sys, re

from kong.models import Test, Site
from kong.utils import run_test

class TwillTests(TestCase):
    """
    Test the twill execution model
    """

    def test_basic_twill_script(self):
        """
        Test that the twill script is being run.
        Mock out the results so that network access
        isn't required.
        """

        from twill.browser import TwillBrowser

        #Mock out the test we want to run.
        html_func = lambda url: "Awesome HTML Output"
        TwillBrowser.get_html = html_func
        code_func = lambda url: 200
        TwillBrowser.get_code = code_func
        url_func = lambda url: 'http://example.com'
        TwillBrowser.get_url = url_func

        test = Test.objects.create(
            body="go awesome.com/\r\ncode 200\r\nfind Awesome",
            name="My Awesome Test",
            slug="my-awesome-test",
        )
        passed = run_test(test)
        self.assertEqual(passed, True)
