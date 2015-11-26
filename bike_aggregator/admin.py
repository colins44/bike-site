from django.contrib import admin
from .models import BikeSearch, BikeShop, RentalEquipment, NewsLetterSubscibers, EnquiryEmail, Stock, Event


class BikeSearchAdmin(admin.ModelAdmin):
    list_display = ['location',]


admin.site.register(BikeShop)
admin.site.register(RentalEquipment)
admin.site.register(NewsLetterSubscibers)
admin.site.register(BikeSearch, BikeSearchAdmin)
admin.site.register(EnquiryEmail)
admin.site.register(Stock)
admin.site.register(Event)