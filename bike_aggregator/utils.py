from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import math
from bike_aggregator.models import BikeShop


class EMail(object):
    """
    A wrapper around Django's EmailMultiAlternatives
    that renders txt and html templates.
    Example Usage:
    >>> email = Email(to='oz@example.com', subject='A great non-spammy email!')
    >>> ctx = {'username': 'Oz Katz'}
    >>> email.text('templates/email.txt', ctx)
    >>> email.html('templates/email.html', ctx)  # Optional
    >>> email.send()
    >>>
    """
    def __init__(self, to, subject, fail_silently=True):
        self.to = to
        self.subject = subject
        self.fail_sliently = fail_silently
        self._html = None
        self._text = None

    def _render(self, template, context):
        return render_to_string(template, context)

    def html(self, template, context):
        self._html = self._render(template, context)

    def text(self, template, context):
        self._text = self._render(template, context)

    def send(self, from_addr=None):
        if isinstance(self.to, basestring):
            self.to = [self.to]
        if not from_addr:
            from_addr = getattr(settings, 'EMAIL_FROM_ADDR')
        msg = EmailMultiAlternatives(
            self.subject,
            self._text,
            from_addr,
            self.to
        )
        if self._html:
            msg.attach_alternative(self._html, 'text/html')
        msg.send(self.fail_sliently)


def pythagoris(longs, lats):
    """
    this should take two itoradors sort them then subtract them
    :param tuple:
    :param tuple:
    :return: distance in straight line
    """
    #first sort high to low
    lats = sorted(lats, reverse=True)
    longs = sorted(longs, reverse=True)

    #now subtract high from low
    cos = lats[0]-lats[1]
    sin = longs[0]-longs[1]
    distance_squared = math.pow(cos, 2)+math.pow(sin, 2)
    distance = round(math.sqrt(distance_squared), 2)
    return distance

def distance_filter(bike_search, bike_shop_queryset, distance=5, number_to_return=10):
    """
    lets try return all items that are within 10 miles
    :param queryset:
    :param distance:
    :param number_to_return:
    :return:
    """
    queryset = bike_shop_queryset
    queryset.filter(latitude__lte=(bike_search.latitude+distance))
    queryset.filter(latitude__gte=(bike_search.latitude-distance))
    queryset.filter(longitude__lte=(bike_search.longitude+distance))
    queryset.filter(longitude__gte=(bike_search.longitude-distance))

    #now we can hit the db
    for bike_shop in queryset:
        distance = pythagoris((bike_search.latitude, bike_shop.latitude),
                              (bike_search.longitude, bike_shop.longitude))
        bike_shop.distance_to_search = distance

    return sorted(queryset, key=lambda x: x.distance_to_search)