from decimal import Decimal
from django.db.models import Count
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from bike_aggregator.models import BikeShop, BikeSearch
from bike_aggregator.utils import EMail, distance_filter, bikeshop_content_string
from .forms import BikeSearchForm, SignUpForm, ContactForm, NewsLetterSignUpForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
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
        #here we get the lat and long kwargs and make them work for us
        context = super(BikeSearchResults, self).get_context_data(**kwargs)
        bikesearch = {}
        try:
            bikesearch['latitude'] = Decimal(self.kwargs['latitude'])
            bikesearch['longitude'] = Decimal(self.kwargs['longitude'])
        except Exception as e:
            #some sort of error so we log it
            logger.error("Error changing Strings to Decimals: {},  {}".format(e.message, e.args))
        context['bikeshops'] = distance_filter(bikesearch, self.model.objects.all())
        context['message'] = "your results"
        context['bikesearch'] = bikesearch
        return context

class BikeSearchResultsMapView(ListView):
    model = BikeShop
    paginate_by = 10
    template_name = "map-view.html"

    def get_context_data(self, **kwargs):
        #here we get the lat and long kwargs and make them work for us
        context = super(BikeSearchResultsMapView, self).get_context_data(**kwargs)
        bikesearch = {}
        try:
            bikesearch['latitude'] = Decimal(self.kwargs['latitude'])
            bikesearch['longitude'] = Decimal(self.kwargs['longitude'])
        except Exception as e:
            #some sort of error so we log it
            logger.error("Error changing Strings to Decimals: {},  {}".format(e.message, e.args))
        context['bikeshops'] = bikeshop_content_string(distance_filter(bikesearch, self.model.objects.all()))
        context['message'] = "your results"
        try:
            bikesearch['latitude'] = float(self.kwargs['latitude'])
            bikesearch['longitude'] = float(self.kwargs['longitude'])
        except Exception as e:
            #some sort of error so we log it
            logger.error("Error changing Decimals to floats: {},  {}".format(e.message, e.args))
        context['bikesearch'] = bikesearch
        context['zoom'] = 13
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
        return super(BikeShopContact, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BikeShopContact, self).get_context_data(**kwargs)
        context['bikeshop'] = get_object_or_404(BikeShop, pk=self.kwargs['pk'])
        return context


class SignUp(FormView):
    template_name = 'sign-up.html'
    form_class = SignUpForm
    success_url = '/thanks/'

    def form_valid(self, form):
        form.save()
        return super(SignUp, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)
        context['message'] = "Sign your store up and start renting your bikes out to users of our website"
        context['button'] = "Sign Up"
        context['website_name'] = 'YouVelo.com'
        return context


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        return super(ContactView, self).form_valid(form)


class SorryNoBikesAvalibleView(TemplateView):
    template_name = "sorry-no-bikes-available.html"

    def get_context_data(self, **kwargs):
        context = super(SorryNoBikesAvalibleView, self).get_context_data(**kwargs)
        context['message'] = "Sorry we do not have any bikes  currently available in the area you are searching"
        context['button'] = "Home"
        context['website_name'] = 'YouVelo.com'
        return context


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
    form_class = NewsLetterSignUpForm
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
        searchers = self.model.objects.values('search_time').annotate(count=Count('search_time'))
        context['objects'] = [x for x in searchers if x['search_time']]
        return context

