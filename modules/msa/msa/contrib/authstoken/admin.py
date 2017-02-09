from django.contrib import admin

from .models import SUser, SToken



class SUserAdmin(admin.ModelAdmin):
    list_display = ('sid', 'is_active', 'description', 'created', 'updated')
    ordering = ('-updated',)


admin.site.register(SUser, SUserAdmin)



class STokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'suser', 'host', 'created')
    fields = ('suser', 'host')
    ordering = ('-created',)


admin.site.register(SToken, STokenAdmin)
