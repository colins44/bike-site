from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

class StaticSiteMap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['ab-page-one', 'ab-page-two', 'contact', 'sign-up', 'sorry-no-bikes-available', 'thanks']

    def location(self, item):
        return reverse(item)
