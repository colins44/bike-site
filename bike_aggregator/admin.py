from django.contrib import admin
from .models import BikeSearch, BikeShop, RentalEquipment, NewsLetterSubscibers, EnquiryEmail, Stock, Event, Booking \



class BikeSearchAdmin(admin.ModelAdmin):
    list_display = ['location', 'country', 'search_time']


class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_time']
    list_filter = ['name', 'event_time']


admin.site.register(BikeShop)
admin.site.register(RentalEquipment)
admin.site.register(NewsLetterSubscibers)
admin.site.register(BikeSearch, BikeSearchAdmin)
admin.site.register(EnquiryEmail)
admin.site.register(Stock)
admin.site.register(Event, EventAdmin)
admin.site.register(Booking)