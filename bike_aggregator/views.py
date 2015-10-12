from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from bike_aggregator.models import BikeShop
from .forms import BikeRentalForm, SignUpForm, ContactForm
import random


class BikesShops(ListView):
    model = BikeShop
    paginate_by = 10
    template_name = "bike-shop-list.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=BikeShop.objects.all())
        return super(BikesShops, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BikesShops, self).get_context_data(**kwargs)
        context['publisher'] = self.object
        return context

    def get_queryset(self):
        return self.objects.all()


def index(request):
    urls = ('test', 'control')
    return redirect(random.choice(urls), permanent=True)


class Control(FormView):
    template_name = 'bikes-to-rent.html'
    form_class = BikeRentalForm
    success_url = '/sorry-no-bikes-available/'

    def form_valid(self, form):
        form.save()
        super(Control, self).form_valid(form)
        testing_dict = {'name':'colin', 'age':31}
        redirect_url = "/bike-shops/?{}={}".format((testing_dict.keys()), (testing_dict.values()))
        print redirect_url
        return HttpResponseRedirect(reverse(BikesShops))

    def get_context_data(self, **kwargs):
        context = super(Control, self).get_context_data(**kwargs)
        context['message'] = "Search for bikes to rent all over the world"
        context['button'] = "Search"
        context['website_name'] = 'YouVelo.com'
        context['submit_url'] = '/bikes-to-rent/'
        return context

class Test(FormView):
    template_name = 'bicycles-to-rent.html'
    form_class = BikeRentalForm
    success_url = '/sorry-no-bikes-available/'

    def form_valid(self, form):
        form.save()
        super(Test, self).form_valid(form)
        testing_dict = {'name':'colin', 'age':31}
        redirect_url = "/bike-shops/?{}={}".format((testing_dict.keys()), (testing_dict.values()))
        print redirect_url
        return HttpResponseRedirect(reverse(BikesShops))

    def get_context_data(self, **kwargs):
        context = super(Test, self).get_context_data(**kwargs)
        context['message'] = "Search for bikes to rent all over the world"
        context['button'] = "Search"
        context['website_name'] = 'YouVelo.com'
        context['submit_url'] = '/bicycles-to-rent/'
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
        form.send_email()
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

