from django.contrib import admin
from .models import BikeSearch, BikeShop, RentalEquipment


class BikeSearchAdmin(admin.ModelAdmin):
    list_display = ['location',]


admin.site.register(BikeShop)
admin.site.register(RentalEquipment)
admin.site.register(BikeSearch, BikeSearchAdmin)
