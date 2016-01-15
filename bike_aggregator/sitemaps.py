from django.contrib.sitemaps import Sitemap
from bike_aggregator.models import BikeShop
from django.template.defaultfilters import slugify


class StaticSiteMap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        #get a list of city names with no duplicates
        cities = BikeShop.objects.all().values_list('city', flat=True).distinct()
        city_urls = []
        for city in cities:
            try:
                city_urls.append("/bike-shop-search-results/{}/".format(slugify(city)))
                city_urls.append("/bike-shop-search-results/{}/?filter=scooter".format(slugify(city)))
                city_urls.append("/bike-shop-search-results/{}/?filter=electric-bicycle".format(slugify(city)))
                city_urls.append("/bike-shop-search-results/{}/?filter=cruiser-bicycle".format(slugify(city)))
            except:
                pass
        city_urls.append("/contact/")
        city_urls.append("/find-out-more/")
        city_urls.append("/")
        return city_urls

    def location(self, item):
        return item
