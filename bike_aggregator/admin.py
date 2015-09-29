from django.contrib import admin
from .models import BikeSearch, BikeShop

class BikeSearchAdmin(admin.ModelAdmin):
    list_display = ['location', 'bike_type', 'no_of_bikes']


admin.site.register(BikeShop)
admin.site.register(BikeSearch, BikeSearchAdmin)
