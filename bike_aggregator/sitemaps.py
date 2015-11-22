from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from bike_aggregator.models import BikeShop


class StaticSiteMap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return BikeShop.objects.all()

    def location(self, item):
        return item.get_absolute_url()
