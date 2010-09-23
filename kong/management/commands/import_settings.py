from django.core.management.base import BaseCommand
from kong.models import HostedSite, Site, Type, Server

class Command(BaseCommand):
    "A basic command to create a site from your current DJANGO_SETTINGS_MODULE"

    def handle(self, *args, **options):
        from django.conf import settings
        HostedSite.objects.create(
            name = name,
            slug = slugify(name),
           
        )
