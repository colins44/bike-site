import json
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.forms import model_to_dict
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.views.generic.edit import FormView
import itertools
from bike_aggregator.models import BikeShop, BikeSearch, Stock, Event, RentalEquipment
from bike_aggregator.utils import EMail, distance_filter, bikeshop_content_string
from .forms import BikeSearchForm, BikeShopForm, ContactForm, NewsLetterSignUpFrom, EnquiryEmailForm, StockForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from formtools.wizard.views import SessionWizardView
import logging
logger = logging.getLogger(__name__)


class Index(FormView):
    form_class = BikeSearchForm
    success_url = 'bike-shops/'
    template_name = 'home.html'

    def form_valid(self, form):
        super(Index, self).form_valid(form)
        form.save()
        #here we redirect to the actuall list view with the kwargs
        return redirect('bike-shop-search-results',
                        latitude=form.cleaned_data['latitude'],
                        longitude=form.cleaned_data['longitude'])


class BikeSearchResults(ListView):
    model = BikeShop
    paginate_by = 10
    template_name = "bike-shop-list.html"

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
        context['message'] = "your results"
        if self.request.GET.get('filter'):
            try:
                rental_equipment = RentalEquipment.objects.get(slug=self.request.GET.get('filter'))
                context['bikeshops'] = bikeshop_content_string(
                    distance_filter(
                        bikesearch, self.model.objects.filter(rental_options__in=[rental_equipment.pk])))[:20]
            except ObjectDoesNotExist:
                context['bikeshops'] = bikeshop_content_string(distance_filter(bikesearch, self.model.objects.all()))[:20]
        context['rental_options'] = RentalEquipment.objects.all()
        return context


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
        return HttpResponseRedirect('/stock/list/')


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


class BikeShopView(DetailView):
    model = BikeShop
    template_name = 'bike_aggregator/bikeshop_list.html'


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


class EnquiryEmailSent(TemplateView):
    template_name = 'thanks.html'

    def get_context_data(self, **kwargs):
        context = super(EnquiryEmailSent, self).get_context_data(**kwargs)
        context['message'] = "Thanks, we have contacted the bike store and hope to hear from them soon"
        context['button'] = "Search Again"
        context['website_name'] = 'YouVelo.com'
        context['button_action'] = "/"
        return context


def map(request):
    array_to_js = {
        "type": "FeatureCollection",
        "features": [],
    }
    for bikeshop in BikeShop.objects.all():
        if bikeshop.latitude and bikeshop.longitude:
            array_to_js["features"].append(
                { "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [float(bikeshop.longitude), float(bikeshop.latitude)]},
            "properties": {"name": bikeshop.shop_name}
             },
            )
    return JsonResponse(array_to_js, safe=False)

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


class ContactWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        return render_to_response('done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })

    def get_form_initial(self, step):
        import ipdb; ipdb.set_trace()
        return self.initial_dict.get(step, {})

    def get_context_data(self, form, **kwargs):
        context = super(ContactWizard, self).get_context_data(form=form, **kwargs)
        import ipdb; ipdb.set_trace()
        if self.steps.current == 'my_step_name':
            context.update({'another_var': True})
        return context
