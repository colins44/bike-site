from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
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
    owned_by = models.OneToOneField(User, blank=True, null=True)
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
    rental_options = models.ManyToManyField(RentalEquipment, blank=True)
    website = models.URLField(null=True, blank=True)
    email = models.EmailField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15)

    def __unicode__(self):
        return self.shop_name

    def get_absolute_url(self):
        return reverse('shop-profile', args=[self.pk])


class NewsLetterSubscibers(models.Model):
    name = models.CharField(max_length=225, null=True, blank=True)
    email_address = models.EmailField()
    subscribed = models.BooleanField(default=True)

    def __unicode__(self):
        return self.email_address


class EnquiryEmail(models.Model):
    from_address = models.EmailField(null=True, blank=True)
    bike_shop = models.ForeignKey(BikeShop, blank=True)
    body = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "enquiry email from {} to bikeshop: {}".format(self.from_address, self.bike_shop.email)


year_choices = (
    (2000, 2000),
    (2001, 2001),
    (2002, 2002),
    (2003, 2003),
    (2004, 2004),
    (2005, 2005),
    (2006, 2006),
    (2007, 2007),
    (2008, 2008),
    (2009, 2009),
    (2010, 2010),
    (2011, 2011),
    (2012, 2012),
    (2013, 2013),
    (2014, 2014),
    (2015, 2015),
    (2016, 2016),
)


class Stock(models.Model):
    type = models.CharField(max_length=225, null=True, blank=True)
    make = models.CharField(max_length=225)
    year = models.IntegerField(blank=True, null=True, choices=year_choices)
    size = models.CharField(max_length=225, null=True, blank=True)
    no_in_stock = models.IntegerField()
    owned_by = models.ForeignKey(User, blank=True, null=True)
    last_change = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('stock-detail', args=[self.pk])


class Event(models.Model):
    name = models.CharField(max_length=225, blank=True, null=True)
    data = models.TextField(null=True, blank=True)
    event_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Event: {} at {}".format(self.name, self.event_time)

