import json
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.views.generic.edit import FormView
from bike_aggregator.models import BikeShop, BikeSearch, Stock, Event, RentalEquipment, Booking, StockItem, Prices
from bike_aggregator.utils import EMail, distance_filter, bikeshop_content_string, updator, get_fake_bikeshops, \
    get_location_data_from_google, title_maker
from .forms import BikeSearchForm, BikeShopForm, ContactForm, EnquiryEmailForm, StockForm,\
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

        instance = form.save()
        if not form.cleaned_data['latitude'] and not form.cleaned_data['longitude']:
            location = get_location_data_from_google(form.cleaned_data.get('location'))
            instance.latitude = location.get('latitude')
            instance.longitude = location.get('longitude')
            instance.city = location.get('city')
        instance.latitude = float(instance.latitude)
        instance.longitude = float(instance.longitude)
        instance.search_time = str(instance.search_time)
        self.request.session.__setitem__('bikesearch', model_to_dict(instance))
        return redirect('bike-shop-search-results',
                        latitude=instance.latitude,
                        longitude=instance.longitude)


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
            message = 'Hint: Use the filter button to find the types of bikes you want'
            messages.add_message(request, messages.INFO, message)
        return super(BikeSearchResults, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BikeSearchResults, self).get_context_data(**kwargs)
        context['bikesearch'] = self.request.session.get('bikesearch')

        if self.kwargs.get('city'):
            #if city is in url args return shops by city
            context['bikesearch'] = get_location_data_from_google(self.kwargs.get('city'))
            context['bikeshops'] = BikeShop.objects.filter(city__iexact=self.kwargs['city'])[:1]

        context['bikeshops'] = bikeshop_content_string(distance_filter(context['bikesearch'], self.model.objects.all()))

        if self.request.GET.get('filter'):
            #filter results depending on bike type
            try:
                rental_equipment = RentalEquipment.objects.get(slug=self.request.GET.get('filter'))
                context['bikeshops'] = bikeshop_content_string(
                    distance_filter(
                        context['bikesearch'], self.model.objects.filter(
                            rental_options__in=[rental_equipment.pk])))[:20]
            except ObjectDoesNotExist:
                context['bikeshops'] = bikeshop_content_string(distance_filter
                                                               (context['bikesearch'], self.model.objects.all()))[:20]

        if context['bikeshops'][0].distance_to_search > 7:
            context['bikeshops'] = bikeshop_content_string(get_fake_bikeshops(
                self.request.session['bikesearch']['latitude'],
                self.request.session['bikesearch']['longitude']))

        context['rental_options'] = RentalEquipment.objects.all()
        context['title'] = title_maker(self.request.session['bikesearch'].get('city', None),
                                       self.request.GET.get('filter', None))
        return context


def bikeshopdetail(request, pk):

    bikeshop = get_object_or_404(BikeShop, pk=pk)
    rental_equipment = []
    prices = Prices.objects.filter(bike_shop__pk=pk)
    for price in prices:
        rental_equipment.append("{} rental {} {} / day".format(price.rental_equipment.name,
                                                               price.currency,
                                                               price.price))
        # rental_equipment_data = model_to_dict(price)
        # rental_equipment_data['bike_type'] = price.rental_equipment.name
        # rental_equipment.append(rental_equipment_data)

    data = model_to_dict(bikeshop, exclude=['website', 'rental_options', 'fake', 'owned_by'])
    data['rental_equipment'] = rental_equipment

    return JsonResponse(data)


class BikeShopView(FormView):
    model = BikeShop
    template_name = 'shop_detail_page.html'
    form_class = ReservationRequestForm

    def get(self, request, *args, **kwargs):
        if self.request.session.get('visited', False):
            pass
        else:
            self.request.session['visited'] = True
            message = 'Send a booking request to this shop by filling ' \
                      'out the Booking Request Form or send multipul booking ' \
                      'request by clicking "add to request list" button ' \
                      'and send your booking request to many stores at once'
            messages.add_message(self.request, messages.INFO, message)
        return super(BikeShopView, self).get(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BikeShopView, self).get_context_data(**kwargs)
        context['bikeshop'] = get_object_or_404(BikeShop, pk=self.kwargs['pk'])
        context['prices'] = Prices.objects.filter(bike_shop__pk=self.kwargs['pk'])
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
            message = "Reservation Request sent to {} . For best results send a request to more than one store".format(bikeshop.shop_name)
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

