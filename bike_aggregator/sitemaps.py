from django.contrib.sitemaps import Sitemap
from bike_aggregator.models import BikeShop


class StaticSiteMap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        #get a list of city names with no duplicates
        cities = BikeShop.objects.all().values_list('city', flat=True).distinct()
        city_urls = []
        for city in cities:
            try:
                city_urls.append("/bike-shop-search-results/{}/".format(city.lower()))
            except:
                pass
        city_urls.append("/about/")
        city_urls.append("/sign-up/")
        city_urls.append("/contact/")
        city_urls.append("")
        city_urls.append("/find-out-more/")
        city_urls.append("/sign-up/")
        return city_urls

    def location(self, item):
        return item
