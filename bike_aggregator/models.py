from django.db import models
from django.core.validators import RegexValidator

bike_types = (
    ('road_bike', 'road bike'),
    ('mountain_bike', 'mountain bike'),
    ('hybrid_bike', 'hybrid bike'),
    ('touring_bike', 'touring bike'),
    ('electric_bike', 'electric bike'),
)

class BikeSearch(models.Model):
    location = models.CharField(max_length=225)
    bike_type = models.CharField(max_length=225, choices=bike_types)
    no_of_bikes = models.IntegerField()
    email = models.EmailField(null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15)

    def __unicode__(self):
        return u'%s' % self.pk

class BikeShop(models.Model):
    town_or_region = models.CharField(max_length=225)
    country = models.CharField(max_length=225)
    shop_name = models.CharField(max_length=225)
    website = models.URLField(null=True, blank=True)
    email = models.EmailField()

    def __unicode__(self):
        return self.shop_name
# Create your models here.
