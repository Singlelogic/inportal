from django.contrib import admin

from .models import Accumulator, DataCollectTerminal


class DataCollectTerminalAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'serial_number', 'mac_address', 'user',
                    'accumulator', 'remark')
    list_display_links = ('name', 'user', 'accumulator', 'remark')


class AccumulatorAdmin(admin.ModelAdmin):
    list_display = ('number', 'date_change', 'remark')


admin.site.register(DataCollectTerminal, DataCollectTerminalAdmin)
admin.site.register(Accumulator, AccumulatorAdmin)
