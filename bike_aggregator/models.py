from django.db import models

bike_types = (
    ('road_bike', 'road bike'),
    ('mountain_bike', 'mountain bike'),
    ('hybrid_bike', 'hybrid bike'),
    ('touring_bike', 'touring bike'),
    ('electric_bike', 'electric bike'),
)

class BikeSearch(models.Model):
    town_or_region = models.CharField(max_length=225)
    country = models.CharField(max_length=225)
    bike_type = models.CharField(max_length=225, choices=bike_types)
    no_of_bikes = models.IntegerField()
    email = models.EmailField(null=True, blank=True)

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
