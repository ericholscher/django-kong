from django.db import models
from django.template import Template, Context
from django.db.models import permalink
from django.contrib.localflavor.us import models as USmodels
import datetime
import urlparse

class Site(models.Model):
    name = models.CharField(max_length=80, blank=True)
    slug = models.SlugField()
    type = models.ForeignKey('Type', related_name='sites', null=True, blank=True)
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
    def tests(self):
        return Test.objects.filter(sites=self) | Test.objects.filter(types=self.type)

    def latest_results(self):
        """
        This returns a list of the latest testresult for each test
        defined for a site.
        """
        ret_val = []
        for test in self.tests:
            try:
                latest_result = test.test_results.filter(site=self)[0]
                ret_val.append(latest_result)
            except IndexError:
                #No result for test
                pass
        return ret_val


class Type(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(blank=True)

    def __unicode__(self):
        return self.name

    def all_sites(self):
        return self.sites.all()

class Test(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True)
    sites = models.ManyToManyField(Site, blank=True, null=True, related_name='tests')
    types = models.ManyToManyField(Type, blank=True, null=True, related_name='tests')
    body = models.TextField()

    def __unicode__(self):
        return self.name

    def render(self, site):
        return Template(self.body).render(Context({'site': site, 'test': self})).encode()

    @permalink
    def get_absolute_url(self):
        return ('kong_testresults_detail', [self.slug])


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
