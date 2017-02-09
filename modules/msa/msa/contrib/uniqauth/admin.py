from django.contrib import admin

from .models import Account, AccessLog, PasswordHistory



class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'update', 'misc')
    ordering = ('-update',)


admin.site.register(Account, AccountAdmin)



class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('account', 't', 'ip', 'token')
    ordering = ('-t',)


admin.site.register(AccessLog, AccessLogAdmin)



class PasswordHistoryAdmin(admin.ModelAdmin):
    list_display = ('account', 't', 'ip', 'password')
    ordering = ('-t',)


admin.site.register(PasswordHistory, PasswordHistoryAdmin)
