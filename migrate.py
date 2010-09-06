from django.db import connection

cursor = connection.cursor()
cursor.execute('alter table kong_site add column "servername" varchar(100)')
cursor.execute('alter table kong_site drop column client_id')
cursor.execute('alter table kong_site drop column settings')
cursor.execute('alter table kong_site drop column pythonpath')
cursor.execute('select site_ptr_id, servername from kong_hostedsite')
rows = cursor.fetchall()
names = dict([(row[0], row[1]) for row in rows])

from kong.models import Site
for site in Site.objects.all():
    site.servername = names[site.pk]
    site.save()

"""
cursor.execute('delete table kong_alias')
cursor.execute('delete table kong_client')
cursor.execute('delete table kong_deploytarget')
cursor.execute('delete table kong_deploytarget_servers')
cursor.execute('delete table kong_hostedsite')
cursor.execute('delete table kong_hostedsite_on_servers')
cursor.execute('delete table kong_server')
cursor.execute('delete table kong_test_sites')
"""
