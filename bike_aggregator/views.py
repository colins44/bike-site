import json
from django.http import HttpResponseRedirect
import requests
import itertools
from decimal import Decimal
import datetime
import requests
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.forms import model_to_dict
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.views.generic.edit import FormView
from bike_aggregator.models import BikeShop, BikeSearch, Stock, Event, RentalEquipment, Booking, StockItem
from bike_aggregator.utils import EMail, distance_filter, bikeshop_content_string, updator, get_fake_bikeshops
from .forms import BikeSearchForm, BikeShopForm, ContactForm, NewsLetterSignUpFrom, EnquiryEmailForm, StockForm,\
    ReservationRequestForm
from django.shortcuts import get_object_or_404


import logging
logger = logging.getLogger(__name__)


class Index(FormView):
    form_class = BikeSearchForm
    success_url = 'bike-shops/'
    template_name = 'home2.html'
    template_name = 'home2.html'

    def form_valid(self, form):
        super(Index, self).form_valid(form)
        if form.cleaned_data['latitude'] and form.cleaned_data['longitude']:
            instance = form.save()
            instance.latitude = float(instance.latitude)
            instance.longitude = float(instance.longitude)
            self.request.session.__setitem__('bikesearch', model_to_dict(instance))
            return redirect('bike-shop-search-results',
                        latitude=form.cleaned_data['latitude'],
                        longitude=form.cleaned_data['longitude'])
        else:
            try:
                base_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(form.cleaned_data.get('location'))
                req = requests.get(base_url)
                data = json.loads(req.content)
                location = data['results'][0]['geometry']['location']
                instance = form.save()
                instance.latitude = location['lat']
                instance.longitude = location['lng']
                self.request.session.__setitem__('bikesearch', model_to_dict(instance))
                return redirect('bike-shop-search-results',
                                latitude=location['lat'],
                                longitude=location['lng'])
            except Exception as e:
                logger.error("error getting lat and long, message:{}".format(e.message))
                return redirect('bike-shop-search-results',
                        latitude=form.cleaned_data['latitude'],
                        longitude=form.cleaned_data['longitude'])


class BikeSearchResults(ListView):
    model = BikeShop
    paginate_by = 10
    template_name = "bike-shop-list2.html"
    context_object_name = 'bikeshops'

    def get(self, request, *args, **kwargs):

        if request.session.get('visited', False):
            pass
        else:
            request.session['visited'] = True
            message = 'You can find bike shops that rent out the type of bikes you are looking for with the filter button'
            messages.add_message(request, messages.INFO, message)
        return super(BikeSearchResults, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BikeSearchResults, self).get_context_data(**kwargs)
        bikesearch = {}
        if self.kwargs.get('city'):
            context['bikeshops'] = BikeShop.objects.filter(city__iexact=self.kwargs['city'])[:1]
            if context['bikeshops']:
                bikesearch['latitude'] = context['bikeshops'][0].latitude
                bikesearch['longitude'] = context['bikeshops'][0].longitude
        else:
            try:
                bikesearch['latitude'] = Decimal(self.kwargs['latitude'])
                bikesearch['longitude'] = Decimal(self.kwargs['longitude'])
            except Exception as e:
                #some sort of error so we log it
                logger.error("Error changing Strings to Decimals: {},  {}".format(e.message, e.args))

        context['bikeshops'] = bikeshop_content_string(distance_filter(bikesearch, self.model.objects.all()))
        context['bikesearch'] = bikesearch

        if self.request.GET.get('filter'):
            try:
                rental_equipment = RentalEquipment.objects.get(slug=self.request.GET.get('filter'))
                message = 'Search results filtered on {}'.format(self.request.GET.get('filter'))
                messages.add_message(self.request, messages.INFO, message)
                context['bikeshops'] = bikeshop_content_string(
                    distance_filter(
                        bikesearch, self.model.objects.filter(rental_options__in=[rental_equipment.pk])))[:20]
            except ObjectDoesNotExist:
                context['bikeshops'] = bikeshop_content_string(distance_filter(bikesearch, self.model.objects.all()))[:20]

        if context['bikeshops'][0].distance_to_search > 7:
            context['bikeshops'] = bikeshop_content_string(get_fake_bikeshops(self.request.session['bikesearch']['latitude'],
                                                                              self.request.session['bikesearch']['longitude']))
        context['rental_options'] = RentalEquipment.objects.all()
        return context


class BikeShopView(FormView):
    model = BikeShop
    template_name = 'shop_detail_page.html'
    form_class = ReservationRequestForm

    def get(self, request, *args, **kwargs):
        if self.request.session.get('visited', False):
            pass
        else:
            self.request.session['visited'] = True
            print 'not visited, where is the message'
            message = 'Send a booking request to this shop by filling ' \
                      'out the Booking Request Form or send multipul booking ' \
                      'request by clicking "add to request list" button ' \
                      'and send your booking request to many stores at once'
            messages.add_message(self.request, messages.INFO, message)
        return super(BikeShopView, self).get(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BikeShopView, self).get_context_data(**kwargs)
        context['bikeshop'] = get_object_or_404(BikeShop, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        self.success_url = '/shop-profile/{}/'.format(self.kwargs['pk'])
        bikeshop = get_object_or_404(BikeShop, pk=self.kwargs['pk'])
        if not self.request.session.get('booking_message'):
            self.request.session['booking_message'] = True
            message = "Reservation Request sent to {}. " \
                      "For best results send a couple of Reservation Requests " \
                      "to other shops within the same area".format(bikeshop.shop_name)
        else:
            self.request.session['booking_message'] = True
            message = "Reservation Request sent to {}".format(bikeshop.shop_name)
        messages.add_message(self.request, messages.INFO, message)
        context = {}
        context['bikeshop'] = bikeshop
        context['form_data'] = form.cleaned_data
        email = EMail(to=bikeshop.email, subject='Bike Hire Enquiry')
        email.text('emails/reservations_request.txt', context)
        email.html('emails/reservations_request.html', context)
        email.send()
        Event.objects.create(
            name='Reservations Request email sent',
            data="Reservation Request sent from: {} to: {}".format(bikeshop.email, form.cleaned_data.get('email'))
        )
        return super(BikeShopView, self).form_valid(form)


class BikeShopContact(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = "/enquiry-email-sent/"

    def form_valid(self, form):
        context = {
            'bikeshop': get_object_or_404(BikeShop, pk=self.kwargs['pk']),
            'user': form.cleaned_data
        }
        email = EMail(to=context['bikeshop'].email, subject='Bike Hire Enquiry')
        email.text('emails/enquiry.txt', context)
        email.html('emails/enquiry.html', context)
        email.send()
        #now save the equiry email
        enquiry_form = EnquiryEmailForm(
            {
                'body': form.cleaned_data.get('message'),
                "bike_shop": context['bikeshop'].pk,
                "from_address": form.cleaned_data.get('email'),
             })
        if enquiry_form.is_valid():
            enquiry_form.save()
        else:
            logging.error("error saving enquiry form")
        return super(BikeShopContact, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BikeShopContact, self).get_context_data(**kwargs)
        context['bikeshop'] = get_object_or_404(BikeShop, pk=self.kwargs['pk'])
        return context


class BikeShopRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        bike_shop = model_to_dict(get_object_or_404(BikeShop, pk=self.kwargs['pk']), exclude=['latitude', 'longitude'])
        Event.objects.create(
            name="Customer redirected to bike shop website",
            data=json.dumps(bike_shop)
        )
        return bike_shop['website']

class SignUp(FormView):
    template_name = 'sign-up.html'
    form_class = BikeShopForm
    success_url = '/thanks/'

    def form_valid(self, form):
        form.save()
        return super(SignUp, self).form_valid(form)


class CrudMixin(object):

    def get_success_url(self):
        return reverse('stock-list')

    def get_queryset(self):
        return self.model.objects.filter(owned_by=self.request.user)


class StockListView(CrudMixin, ListView):
    model = Stock


class StockDetailView(CrudMixin, DetailView):
    model = Stock


class StockCreateView(CrudMixin, CreateView):
    model = Stock
    form_class = StockForm

    def form_valid(self, form):
        instance = form.save()
        instance.owned_by = self.request.user
        instance.last_change = timezone.now()
        instance.save()
        stock_item = model_to_dict(instance)
        stock_item['stock_id'] = instance.pk
        stock_item['owned_by'] = self.request.user
        stock_item.pop('id')
        stockitems = [StockItem(**stock_item) for x in xrange(form.cleaned_data['no_in_stock'])]
        StockItem.objects.bulk_create(stockitems)
        return HttpResponseRedirect('/stock/list/')


class StockDeleteView(CrudMixin, DeleteView):
    model = Stock


class StockUpdateView(CrudMixin, UpdateView):
    model = Stock
    form_class = StockForm

    def form_valid(self, form):
        instance = form.save()
        instance.last_change = timezone.now()
        instance.save()
        #check if there is a difference in the number of itmes
        updator(instance, form.cleaned_data['no_in_stock'], self.request.user)
        return HttpResponseRedirect('/stock/list/')


class BookingListView(CrudMixin, ListView):
    model = Booking


class BookingDetailView(CrudMixin, DetailView):
    model = Booking

class ShopCreateView(CrudMixin, CreateView):
    model = BikeShop
    form_class = BikeShopForm
    template_name = "bike_aggregator/stock_form.html"

    def form_valid(self, form):
        instance = form.save()
        instance.owned_by = self.request.user
        instance.last_change = timezone.now()
        instance.save()
        return HttpResponseRedirect('/profile/')


class ShopDetailView(CrudMixin, ListView):
    template_name = 'bike_aggregator/bikehops_list.html'
    model = BikeShop


class ShopUpdateView(CrudMixin, UpdateView):
    model = BikeShop
    form_class = BikeShopForm
    template_name = "bike_aggregator/stock_update_form.html"

    def form_valid(self, form):
        instance = form.save()
        instance.last_change = timezone.now()
        instance.save()
        return HttpResponseRedirect('/profile/')


class ShopDeleteView(CrudMixin, DeleteView):
    model = BikeShop
    template_name = "bike_aggregator/stock_confirm_delete.html"

    def get_success_url(self):
        return reverse('shop-detail')


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        return super(ContactView, self).form_valid(form)


class StoreSignUp(TemplateView):
    template_name = 'thanks.html'

    def get_context_data(self, **kwargs):
        context = super(StoreSignUp, self).get_context_data(**kwargs)
        context['message'] = "Thanks for sigining up, we will be in contact shortly"
        context['button'] = "Home"
        context['website_name'] = 'YouVelo.com'
        return context


class NewsLetterSignUp(FormView):
    form_class = NewsLetterSignUpFrom
    success_url = '/thanks/'
    template_name = 'find-out-more.html'

    def form_valid(self, form):
        form.save()
        return super(NewsLetterSignUp, self).form_valid(form)

class SearchPopularityChart(ListView):
    model = BikeSearch
    template_name = 'geo-chart.html'

    def get_context_data(self, **kwargs):
        context = super(SearchPopularityChart, self).get_context_data(**kwargs)
        bikesearches = self.model.objects.values('country').annotate(count=Count('country'))
        context['objects'] = [x for x in bikesearches if x['country']]
        return context

class BikeShopGeoChart(ListView):
    model = BikeShop
    template_name = 'geo-chart.html'

    def get_context_data(self, **kwargs):
        context = super(BikeShopGeoChart, self).get_context_data(**kwargs)
        bikeshops = self.model.objects.values('country').annotate(count=Count('country'))
        context['objects'] = [x for x in bikeshops if x['country']]
        return context

class SearchesOverTimeChart(ListView):
    model = BikeSearch
    template_name = 'line-chart.html'

    def get_context_data(self, **kwargs):
        context = super(SearchesOverTimeChart, self).get_context_data(**kwargs)
        searchers = BikeSearch.objects.filter(search_time__isnull=False)
        searchers = itertools.groupby(searchers, lambda x: x.search_time.date())
        data = []
        for x in searchers:
            we = {}
            we['date'] = x[0]
            we['count'] = len(list(x[1]))
            data.append(we)

        context['objects'] = data
        return context
