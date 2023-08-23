from django.contrib import admin

from .models import PowerSupply, SerialCollector, FPGA

admin.site.register(PowerSupply)
admin.site.register(SerialCollector)
admin.site.register(FPGA)
