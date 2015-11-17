from django.forms import ModelForm
from django.utils import timezone
from bike_aggregator.models import BikeShop, BikeSearch, NewsLetterSubscibers, EnquiryEmail
from django import forms

bike_types = (
    ('scooter', 'scooter'),
    ('road_bike', 'road bike'),
    ('mountain_bike', 'mountain bike'),
    ('hybrid_bike', 'hybrid bike'),
    ('touring_bike', 'touring bike'),
    ('electric_bike', 'electric bike'),
)


class SignUpForm(ModelForm):
    street_number = forms.CharField(max_length=225, required=False, widget=forms.HiddenInput())
    street = forms.CharField(max_length=225, required=False, widget=forms.HiddenInput())
    post_code = forms.CharField(max_length=225, required=False, widget=forms.HiddenInput())
    city = forms.CharField(max_length=225, required=False, widget=forms.HiddenInput())
    country = forms.CharField(max_length=225, required=False, widget=forms.HiddenInput())
    state = forms.CharField(max_length=225, required=False, widget=forms.HiddenInput())
    latitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    longitude = forms.FloatField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = BikeShop
        exclude = ('pk',)

    def save(self, commit=True):
        super(SignUpForm, self).save(commit)


class BikeSearchForm(ModelForm):
    street_number = forms.CharField(max_length=225, required=False, widget=forms.HiddenInput())
    street = forms.CharField(max_length=225, required=False, widget=forms.HiddenInput())
    post_code = forms.CharField(max_length=225, required=False, widget=forms.HiddenInput())
    city = forms.CharField(max_length=225, required=False, widget=forms.HiddenInput())
    country = forms.CharField(max_length=225, required=False, widget=forms.HiddenInput())
    state = forms.CharField(max_length=225, required=False, widget=forms.HiddenInput())
    latitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    longitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    search_time = forms.DateTimeField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = BikeSearch
        exclude = ('pk',)

    def save(self, commit=True):
        search = super(BikeSearchForm, self).save(commit=False)
        search.search_time = timezone.now()
        search.save()


class ContactForm(forms.Form):

    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class NewsLetterSignUpForm(ModelForm):

    class Meta:
        model = NewsLetterSubscibers
        exclude = ('pk', 'subscribed',)


class EnquiryEmailForm(ModelForm):

    class Meta:
        model = EnquiryEmail
        exclude = ('pk',)



