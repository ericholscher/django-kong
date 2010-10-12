from django.conf import settings
from django.db import models
from django.template import Template, Context
from django.db.models import permalink
from django.contrib.localflavor.us import models as USmodels

from kong.utils import execute_test

import datetime
import urlparse


class Site(models.Model):
    name = models.CharField(max_length=80, blank=True)
    slug = models.SlugField()
    type = models.ForeignKey('Type', related_name='sites',
                             null=True, blank=True)
    servername = models.CharField(max_length=100, default='example.com',
                                  help_text='This is the address of your actual site')
    is_live = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s: %s" % (self.slug, self.servername)

    @permalink
    def get_absolute_url(self):
        return ('kong_site_detail', [self.slug])

    @property
    def url(self):
        curr_site = self.servername
        if urlparse.urlsplit(curr_site).scheme == '':
            curr_site = "http://%s" % curr_site
        return curr_site

    @property
    def all_tests(self):
        if self.type:
            return Test.objects.filter(sites=self) | Test.objects.filter(types=self.type)
        else:
            return Test.objects.filter(sites=self)

    def latest_results(self):
        """
        This returns a list of the latest testresult for each test
        defined for a site.
        """
        ret_val = []
        for test in self.all_tests.all():
            try:
                latest_result = test.test_results.filter(site=self)[0]
                ret_val.append(latest_result)
            except IndexError:
                #No result for test
                pass
        return ret_val

    def run_tests(self):
        all_passed = True
        for test in self.all_tests.all():
            passed = execute_test(self, test)
            all_passed = passed and all_passed
        return all_passed


class Type(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(blank=True)

    def __unicode__(self):
        return self.name

    def all_sites(self):
        return self.sites.all()

    def run_tests(self):
        all_passed = True
        for site in self.all_sites():
            passed = site.run_tests()
            all_passed = passed and all_passed
        return all_passed


class Test(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True)
    sites = models.ManyToManyField(Site, blank=True, null=True, related_name='tests')
    types = models.ManyToManyField(Type, blank=True, null=True, related_name='tests')
    body = models.TextField()

    def __unicode__(self):
        return self.name

    def render(self, site):
        return Template(self.body).render(Context({'site': site, 'test': self})).encode('utf8')

    @permalink
    def get_absolute_url(self):
        return ('kong_testresults_detail', [self.slug])

    @property
    def all_sites(self):
        return self.sites.all() | Site.objects.filter(type__in=self.types.all())

    def run_tests(self):
        all_passed = True
        for site in self.all_sites.all():
            passed = execute_test(site, self)
            all_passed = passed and all_passed
        return all_passed


class TestResult(models.Model):
    test = models.ForeignKey(Test, related_name='test_results')
    site = models.ForeignKey(Site, related_name='test_results')
    run_date = models.DateTimeField(default=datetime.datetime.now, db_index=True)
    duration = models.IntegerField(null=True)
    succeeded = models.BooleanField()
    content = models.TextField()

    class Meta:
        ordering = ('-run_date',)

    def __unicode__(self):
        return "%s for %s" % (self.test, self.site)

    @permalink
    def get_absolute_url(self):
        return ('kong_testresults_detail', [self.slug])

    def get_previous_results(self, num_results=1):
        """
        Returns X number of earlier test results for the same combination of test and site
        """
        return TestResult.objects.filter(
            test=self.test,
            site=self.site,
            pk__lt=self.pk)[:num_results]

    @property
    def failed(self):
        return not self.succeeded

    @property
    def notification_needed(self):
        """
        Checks whether result needs to be mailed to admins.
        The procedure is as follows
        (taking into account min number of consecutive failures):
        1. Find out whether current test failed
        2. Find out whether previous test failed
        3. If MAIL_ON_EVERY_FAILURE is set to False don't send new notification
           if previous test also failed
        4. If test succeeds and MAIL_ON_RECOVERY is set,
           send recovery notification if previous test failed
        """

        MAIL_ON_EVERY_FAILURE = getattr(settings, 'KONG_MAIL_ON_EVERY_FAILURE', False)
        MAIL_ON_RECOVERY = getattr(settings, 'KONG_MAIL_ON_RECOVERY', True)
        CONSECUTIVE_FAILURES = getattr(settings, 'KONG_MAIL_ON_CONSECUTIVE_FAILURES', 1)

        results = self.get_previous_results(CONSECUTIVE_FAILURES)
        results = [self.succeeded] + [result.succeeded for result in results]

        result_list = results[:CONSECUTIVE_FAILURES]

        if True in result_list or len(result_list) < CONSECUTIVE_FAILURES:
            result_failed = False
        elif len:
            result_failed = True

        prev_results = results[1:]
        if True in prev_results or len(prev_results) < CONSECUTIVE_FAILURES:
            prev_result_failed = False
        else:
            prev_result_failed = True

        if result_failed:
            if not MAIL_ON_EVERY_FAILURE and prev_result_failed:
                return False
            return True
        else:
            if MAIL_ON_RECOVERY:
                if prev_result_failed:
                    return True
        return False
