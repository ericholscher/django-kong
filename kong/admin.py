from django.contrib import admin
from kong.models import Test, TestResult, Site, Type

class TestResultAdmin(admin.ModelAdmin):
    search_fields = ('content', 'site__slug')
    list_filter = ('succeeded',)
    list_display = ('test', 'site', 'run_date', 'succeeded')

class SiteInline(admin.TabularInline):
    fields = ('slug', 'is_live', 'servername')
    list_filter = ('is_live',)
    extra = 0
    model = Site

class TestAdmin(admin.ModelAdmin):
    search_fields = ('site', 'test')
    prepopulated_fields = {"slug": ("name",)}
    save_as = True

class SiteAdmin(admin.ModelAdmin):
    search_fields = ('servername',)
    list_display = ('servername', 'slug', 'type')
    prepopulated_fields = {"slug": ("name",)}

class TypeAdmin(admin.ModelAdmin):
    search_fields = ('slug', 'name')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [
        SiteInline,
    ]

admin.site.register(Site, SiteAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(TestResult, TestResultAdmin)
