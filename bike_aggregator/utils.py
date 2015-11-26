from decimal import Decimal
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.forms import model_to_dict
from django.template import Template, Context
from django.template.loader import render_to_string
import math
from bike_aggregator.models import BikeShop, StockItem


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
    def __init__(self, to, subject, fail_silently=False):
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
            from_addr = getattr(settings, 'EMAIL_ENQUIRY_ADDRESS')
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
    distance = round(math.sqrt(distance_squared), 6)
    return distance

def expand_search_area(bike_search, queryset, distance=Decimal(0.025), amount_of_results=10):
    """Expand the search area until the amount of results are reached.
        Default search area expands at a radius rate of 2.5 km each time"""

    while distance < 0.1 and queryset.count() < amount_of_results:
        queryset = queryset.filter(latitude__lte=(bike_search['latitude']+distance))
        queryset = queryset.filter(latitude__gte=(bike_search['latitude']-distance))
        queryset = queryset.filter(longitude__lte=(bike_search['longitude']+distance))
        queryset = queryset.filter(longitude__gte=(bike_search['longitude']-distance))
        distance = distance+distance

    return queryset

def distance_filter(bike_search, bike_shop_queryset, distance=Decimal(0.025), amount_of_results=10):
    """
    default is to return items within a 20km radius of the search point
    """
    conversion = float(0.009)
    queryset = expand_search_area(bike_search, bike_shop_queryset, distance=distance)

    #now we can hit the db
    bike_shops = []
    for bike_shop in queryset:
        if bike_shop.latitude and bike_shop.longitude:
            distance = pythagoris((bike_search['latitude'], bike_shop.latitude),
                                  (bike_search['longitude'], bike_shop.longitude))
            #change the distance from radians back to Km
            bike_shop.distance_to_search = round(distance/conversion, 2)
            bike_shops.append(bike_shop)
    return sorted(bike_shops, key=lambda x: x.distance_to_search)


def bikeshop_content_string(bikeshops):
    """Build the content string for the bike shop markers on the google map"""

    template = Template("<a href=/contact-bikeshop/{{ bikeshop.pk }}/>Contact {{ bikeshop.shop_name }}</a>")

    for bikeshop in bikeshops:
        model_dict = {
            "shop_name": bikeshop.shop_name,
            "pk": str(bikeshop.pk)
        }
        context = Context({"bikeshop":model_dict})
        bikeshop.content_string = template.render(context)


    return bikeshops

def Updator(stock, number_in_stock):
    """
    this function takes all
    :param stock: A stock object
    :return:
    """

    stock = model_to_dict(stock)
    stock['stock_id'] = stock.pop('id')
    stock_items = StockItem.objects.filter(owned_by=stock['owned_by'], stock_id=stock['stock_id'])
    stock_items.update(**stock)

    #now check number in stock and how that corresponds to the actual number
    if len(stock_items) < number_in_stock:
        #create more stock if the bike shop is adding it
        StockItem.objects.bulk_create(
            StockItem(**stock) for x in xrange(number_in_stock - stock_items.count())
        )

    if number_in_stock < len(stock_items):
        stock_to_delete_ids = StockItem.objects.filter(
            owned_by=stock['owned_by'], stock_id=stock['stock_id'])[:stock_items.count()-number_in_stock].values_list("id", flat=True)
        StockItem.objects.filter(id__in=(stock_to_delete_ids)).delete()