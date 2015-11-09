from django.db import models
from django.core.validators import RegexValidator

bike_types = (
    ('road_bike', 'road bike'),
    ('mountain_bike', 'mountain bike'),
    ('touring_bicycle', 'touring bicycle'),
    ('electric_bicycle', 'electric bicycle'),
    ('cruiser_bike', 'cruiser bicycle'),
    ('scooter', 'scooter'),
)

class BikeSearch(models.Model):
    location = models.CharField(max_length=225)
    street_number = models.CharField(max_length=225, blank=True, null=True)
    street = models.CharField(max_length=225, blank=True, null=True)
    post_code = models.CharField(max_length=225, blank=True, null=True)
    state = models.CharField(max_length=225, null=True, blank=True)
    city = models.CharField(max_length=225, null=True, blank=True)
    country = models.CharField(max_length=225, null=True, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    search_time = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.pk


class RentalEquipment(models.Model):
    name = models.CharField(max_length=225)

    def __unicode__(self):
        return self.name

class BikeShop(models.Model):
    shop_name = models.CharField(max_length=225)
    location = models.CharField(max_length=225)
    street_number = models.CharField(max_length=225, blank=True, null=True)
    street = models.CharField(max_length=225, blank=True, null=True)
    post_code = models.CharField(max_length=225, blank=True, null=True)
    state = models.CharField(max_length=225, null=True, blank=True)
    city = models.CharField(max_length=225, null=True, blank=True)
    country = models.CharField(max_length=225, null=True, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    website = models.URLField(null=True, blank=True)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15)
    rental_options = models.ManyToManyField(RentalEquipment)

    def __unicode__(self):
        return self.shop_name

