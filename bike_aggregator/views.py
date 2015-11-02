from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from bike_aggregator.models import BikeShop
from django.views.generic.edit import FormMixin
from bike_aggregator.utils import EMail
from .forms import BikeRentalForm, SignUpForm, ContactForm
from django.shortcuts import get_object_or_404
import random
from django.db.models import Q


def distance_filter(search_object, distance, number_to_return):
    """
    lets try return all items that are within 10 miles
    :param queryset:
    :param distance:
    :param number_to_return:
    :return:
    """
    queryset = BikeShop.objects.all()
    queryset.filter(latitude__lte=(search_object.latitude+2))
    queryset.filter(latitude__gte=(search_object.latitude-2))
    queryset.filter(longitude__lte=(search_object.longitude+2))
    queryset.filter(longitude__gte=(search_object.longitude-2))

    #now we can hit the db
    for bike_shop in queryset:
        #h2=s2+c2

class BikeShopsView(FormMixin, ListView):
    model = BikeShop
    paginate_by = 10
    template_name = "bike-shop-list.html"
    form_class = BikeRentalForm
    success_url = "/bike-shops/"

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        self.form = self.form_class()

        if kwargs.get('search_instance'):
            bikesearch = kwargs['search_instance']
            self.object_list = self.get_queryset().filter(city=bikesearch.city)
            context = self.get_context_data(object_list=self.object_list)
            if self.object_list.count() > 0:
                context = self.get_context_data(object_list=self.object_list)
                context['website_name'] = 'YouVelo.com'
                context['message'] = "your results"
                context['button'] = "Search Again"
                context['button_action'] = "/"

            else:
                self.object_list = self.get_queryset().filter(country=bikesearch.country)
                context['message'] = "Looks like we cant find any bike shops in the area you are looking for"
                context['button'] = "Search Again"
                context['website_name'] = 'YouVelo.com'
                context['button_action'] = "/#one"
                context['form'] = self.form

        else:
            self.object_list = self.model.objects.none()
            context = self.get_context_data(object_list=self.object_list, form=self.form)
            context['website_name'] = 'YouVelo.com'
            context['message'] = "Search for bikes to rent all over the world"
            context['button'] = "Search"

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            kwargs['search_instance'] = form.save()
            return self.get(request, *args, **kwargs)
        else:
            return self.form_invalid(form)


class BikeShopContact(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = "/enquiry-email-sent/"

    def form_valid(self, form):
        context = {
            'bikeshop': get_object_or_404(BikeShop, pk=self.kwargs['pk']),
            'user': form.cleaned_data
        }
        email = EMail(to='colin.pringlewood@gmail.com', subject='Bike Hire Enquiry')
        email.text('emails/enquiry.txt', context)
        email.html('emails/enquiry.html', context)
        email.send()
        return super(BikeShopContact, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BikeShopContact, self).get_context_data(**kwargs)
        context['bikeshop'] = get_object_or_404(BikeShop, pk=self.kwargs['pk'])
        return context


def index(request):
    urls = ('test', 'control')
    return redirect(random.choice(urls), permanent=True)


class Control(FormView):
    template_name = 'bikes-to-rent.html'
    form_class = BikeRentalForm
    success_url = '/sorry-no-bikes-available/'

    def form_valid(self, form):
        form.save()
        return super(Control, self).form_valid(form)

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
        return super(Test, self).form_valid(form)

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

