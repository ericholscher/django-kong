from django.db import models
from django.template import Template, Context
from django.db.models import permalink
from django.contrib.localflavor.us import models as USmodels
import datetime
import urlparse

#(HACK) http://code.djangoproject.com/ticket/897
class ManyToManyField_NoSyncdb(models.ManyToManyField):
    def __init__(self, *args, **kwargs):
        super(ManyToManyField_NoSyncdb, self).__init__(*args, **kwargs)
        self.creates_table = False

class Client(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(blank=True)
    phone = USmodels.PhoneNumberField(blank=True)
    email = models.EmailField(blank=True)
    contact = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return self.slug

class Site(models.Model):
    name = models.CharField(max_length=80, blank=True)
    slug = models.SlugField()
    type = models.ForeignKey('Type', related_name='sites')
    client = models.ForeignKey(Client, related_name='sites', blank=True, null=True)

    settings = models.CharField(max_length=80, default='settings')
    pythonpath = models.CharField(max_length=255,
                                  default="/home/code.django-1.0")
    #aliases = models.ForeignKey('Alias')
    is_live = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s: %s" % (self.slug, self.settings)

    @permalink
    def get_absolute_url(self):
        return ('kong_site_detail', [self.slug])

    @property
    def url(self):
        curr_site = self.hostedsite.servername
        if urlparse.urlsplit(curr_site).scheme == '': 
            curr_site = "http://%s" % curr_site
        return curr_site

    @property
    def tests(self):
        return Test.objects.filter(sites=self) | Test.objects.filter(types=self.type)


class HostedSite(Site):
    servername = models.CharField(max_length=100, default='example.com',
                                  help_text='This is the address of your actual site')
    on_servers = models.ManyToManyField('Server', null=True, blank=True, related_name="sites")
    maxclients = models.IntegerField(default=30, null=True, blank=True)
    wsgi_processes = models.IntegerField(default=5, null=True, blank=True)
    wsgi_max_requests = models.IntegerField(default=500, null=True, blank=True)
    serveradmin = models.CharField(max_length=100, null=True, blank=True)
    mediaserver = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.servername


class Server(models.Model):
    name = models.CharField(max_length=80, blank=True)
    slug = models.SlugField()
    #(HACK) http://code.djangoproject.com/ticket/897
    clients = ManyToManyField_NoSyncdb('HostedSite', db_table='kong_hostedsite_on_servers')
    hostname = models.CharField(max_length=100)
    internalip = models.IPAddressField(null=True, blank=True)
    externalip = models.IPAddressField(null=True, blank=True)

    def __unicode__(self):
        return self.hostname

    @permalink
    def get_absolute_url(self):
        return ('kong_server_detail', [self.slug])


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

###### Not Currently used

class Alias(models.Model):
    site = models.ForeignKey(HostedSite, related_name="aliases")
    url = models.CharField(max_length=100)

    def __unicode__(self):
        return self.url

class DeployTarget(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True)
    is_active = models.BooleanField()
    last_deployed = models.DateTimeField()
    servers = models.ManyToManyField(Server)

    def __unicode__(self):
        return self.name

