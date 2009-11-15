from django.contrib import admin
from kong.models import Test, TestResult, Client, HostedSite, Server, DeployTarget, Type

class TestResultAdmin(admin.ModelAdmin):
    search_fields = ('content', 'site__slug')
    list_filter = ('succeeded',)
    list_display = ('test', 'site', 'run_date', 'succeeded')

class HostedSiteInline(admin.TabularInline):
    fields = ('slug', 'settings', 'is_live', 'on_servers', 'servername')
    model = HostedSite

class DeployTargetAdmin(admin.ModelAdmin):
    pass

class ClientAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        HostedSiteInline,
    ]

class SiteAdmin(admin.ModelAdmin):
    list_filter = ('is_live',)

class TestAdmin(admin.ModelAdmin):
    search_fields = ('site', 'test')
    prepopulated_fields = {"slug": ("name",)}
    save_as = True

class HostedSiteAdmin(SiteAdmin):
    search_fields = ('servername',)
    list_display = ('servername', 'slug', 'type', 'client')
    prepopulated_fields = {"slug": ("name",)}

class ServerAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class TypeAdmin(admin.ModelAdmin):
    search_fields = ('slug', 'name')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        HostedSiteInline,
    ]

admin.site.register(Client, ClientAdmin)
admin.site.register(HostedSite, HostedSiteAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(DeployTarget, DeployTargetAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(TestResult, TestResultAdmin)
