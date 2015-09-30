from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import BikeRentalForm, SignUpForm, ContactForm, BikeRentalFormOne, MotoBikeHireForm
import random

def index(request):
    urls = ('ab-page-one', 'ab-page-two')
    return redirect(random.choice(urls), permanent=True)


class Index(FormView):
    template_name = 'index.html'
    form_class = BikeRentalForm
    success_url = '/sorry-no-bikes-available/'

    def form_valid(self, form):
        form.save()
        return super(Index, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['message'] = "Search for bikes to rent all over the world"
        context['button'] = "Search"
        context['website_name'] = 'YouVelo.com'
        context['submit_url'] = '/bikes-to-rent/'
        return context

class BikeHire(FormView):
    template_name = 'index.html'
    form_class = BikeRentalFormOne
    success_url = '/sorry-no-bikes-available/'

    def form_valid(self, form):
        form.save()
        return super(BikeHire, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BikeHire, self).get_context_data(**kwargs)
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

