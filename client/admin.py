from django.contrib import admin

from .models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('client',)
    list_display_links = ('client',)


admin.site.register(Client, ClientAdmin)
