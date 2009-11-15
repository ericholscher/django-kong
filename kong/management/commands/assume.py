import sys, os
from optparse import OptionParser, make_option

from django.core.management.base import BaseCommand

from kong.models import Test
from kong.models import Site, Type, Server
from kong.utils import run_test, run_tests_for_type, run_tests_for_site, run_tests_for_box
from kong.models import HostedSite


BASH_COMMAND = '@'

def get_sites_for_slug(slug):
    all = []
    hosts = HostedSite.objects.all()
    for host in hosts:
        if host.slug == slug:
            all.append(host)
    return all

usage = "assume.py <shortname> [%s]<action>" % BASH_COMMAND
class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-l", action="store_true", dest="list",
                    help="Print all options"),
    )

    def complete(self):
        return [(h.slug, 0) for h in HostedSite.objects.all()]

    def handle(self, *args, **options):
        LIST = options.get('list')
        if LIST:
            hosts = HostedSite.objects.all()
            #Make unique
            snames = set([x.slug for x in hosts])
            for host in snames:
                print host
            sys.exit()

        if not len(args) == 2:
                sys.exit("Syntax is %s" % usage)
 
        shortname = args[0]
        command = args[1]
        
        hosts = get_sites_for_slug(shortname)
        
        if len(hosts) == 0:
            sys.exit('No hosts matching shortname')
        elif len(hosts) > 1:
            print "Which host file?"
            for num, host in enumerate(hosts):
                print "%s: %s" % (num, host.settings)
            host_num = int(raw_input(">"))
            host = hosts[host_num]
        else:
            host = hosts[0]
        
        if isinstance(host, HostedSite):
            conn_str = "root@%s" % host.on_servers.all()[0]
        else:
            conn_str = host.ssh_path
        
        settings = host.settings
        pypath = host.pythonpath
        
        if command.startswith(BASH_COMMAND):
            command = command.lstrip(BASH_COMMAND)
            conn_str = "ssh %s -t DJANGO_SETTINGS_MODULE=%s PYTHONPATH=%s %s" % (conn_str, settings, pypath, command)
        else:
                conn_str = "ssh %s -t DJANGO_SETTINGS_MODULE=%s PYTHONPATH=%s %s/django/bin/django-admin.py %s" % (conn_str, settings, pypath, pypath, command)
        
        print conn_str
        os.system(conn_str)

