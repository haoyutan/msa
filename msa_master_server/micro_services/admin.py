from django.contrib import admin

from .models import MicroService, MicroServiceConfiguration


class MicroServiceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MicroService._meta.fields]
    fields = ('name', 'url', 'is_external', 'package_source', 'package_version')
    ordering = ('id',)

admin.site.register(MicroService, MicroServiceAdmin)


class MicroServiceConfigurationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in
                    MicroServiceConfiguration._meta.fields]
    ordering = ('id',)

admin.site.register(MicroServiceConfiguration, MicroServiceConfigurationAdmin)


