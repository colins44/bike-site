from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, ProcessFormView
from .forms import BikeRentalForm, SignUpForm, ContactForm


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
        context['website_name'] = 'bike aggregator'
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
        context['message'] = "Sign your store up"
        context['button'] = "Sign Up"
        context['website_name'] = 'Bike Aggregator'
        return context

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        print 'asdasdsadasd'
        return super(ContactView, self).form_valid(form)

class SorryNoBikesAvalibleView(TemplateView):
    template_name = "sorry-no-bikes-available.html"

    def get_context_data(self, **kwargs):
        context = super(SorryNoBikesAvalibleView, self).get_context_data(**kwargs)
        context['message'] = "Sorry we do not have any bikes  currently available in the area you are searching"
        context['button'] = "Home"
        context['website_name'] = 'Bike Aggregator'
        return context

class StoreSignUp(TemplateView):
    template_name = 'thanks.html'

    def get_context_data(self, **kwargs):
        context = super(StoreSignUp, self).get_context_data(**kwargs)
        context['message'] = "Thanks for sigining up, we will be in contact shortly"
        context['button'] = "Home"
        context['website_name'] = 'Bike Aggregator'
        return context


# def handler404(request):
#     response = render_to_response('404.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 404
#     return response
#
#
# def handler500(request):
#     response = render_to_response('500.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 500
#     return response
