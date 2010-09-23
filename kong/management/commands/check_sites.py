from django.core.management.base import BaseCommand
from kong.models import Test
from kong.models import Site, Type
from optparse import OptionParser, make_option



class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("-t", "--test", dest="test"),
        make_option("-s", "--site", dest="site"),
        make_option("-T", "--type", dest="type"),
        make_option("-l", "--list", dest="list",
                    action="store_true", default=False),
    )

    def handle(self, *args, **options):
        TEST = options.get('test')
        SITE = options.get('site')
        TYPE = options.get('type')
        LIST = options.get('list')
        passed =  True

        if TEST:
            print "Running test: %s" % TEST
            test = Test.objects.get(slug=TEST)
            passed = test.run_tests()
        elif TYPE:
            print "Running tests for type : %s" % TYPE
            type = Type.objects.get(slug=TYPE)
            passed = type.run_tests()
        elif SITE:
            print "Running tests for site : %s" % SITE
            site = Site.objects.get(slug=SITE)
            passed = site.run_tests()
        elif LIST:
            print "All Sites:"
            for site in Site.objects.all():
                print site.slug
            print "All Tests:"
            for test in Test.objects.all():
                print test.slug
        else:
            print "Running tests for all sites"
            for site in Site.objects.all():
                passed = site.run_tests()

        #This is mainly for Nagios reporting.
        if passed:
            return 0
        else:
            return 2
