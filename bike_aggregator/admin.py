from django.contrib import admin
from .models import BikeSearch, BikeShop, RentalEquipment


class BikeSearchAdmin(admin.ModelAdmin):
    list_display = ['location', 'bike_type', 'no_of_bikes']


admin.site.register(BikeShop)
admin.site.register(RentalEquipment)
admin.site.register(BikeSearch, BikeSearchAdmin)
