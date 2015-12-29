from django.core.exceptions import ValidationError
from django.forms import ModelForm, formset_factory
from django.utils import timezone
from django.utils.datetime_safe import datetime
from bike_aggregator.models import BikeShop, BikeSearch, NewsLetterSubscibers, EnquiryEmail, Stock
from django import forms
from bike_aggregator.utils import EMail

bike_types = (
    ('scooter', 'scooter'),
    ('road_bike', 'road bike'),
    ('mountain_bike', 'mountain bike'),
    ('hybrid_bike', 'hybrid bike'),
    ('touring_bike', 'touring bike'),
    ('electric_bike', 'electric bike'),
)


class BikeShopForm(ModelForm):
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
        exclude = ('pk', 'owned_by')


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
        self.cleaned_data['search_time'] = timezone.now()
        return super(BikeSearchForm, self).save(commit=False)


class ContactForm(forms.Form):

    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class NewsLetterSignUpFrom(ModelForm):

    class Meta:
        model = NewsLetterSubscibers
        exclude = ('pk', 'subscribed',)


class EnquiryEmailForm(ModelForm):

    class Meta:
        model = EnquiryEmail
        exclude = ('pk',)

class StockForm(forms.ModelForm):
    no_in_stock = forms.IntegerField()

    class Meta:
        model = Stock
        exclude = ('owned_by',)


class BookingForm1(forms.Form):
    email = forms.EmailField(required=True)
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'), required=True)
    number_of_days = forms.IntegerField(required=True)
    bike_type = forms.ChoiceField(required=True,
                                  widget=forms.Select(),
                                  choices=((None, None),),
                                  label="Select the type of bike you would like to rent")

    def clean(self):
        if self.cleaned_data['start_date'] < datetime.now().date():
            raise ValidationError('Please choose a date in the future')
        else:
            super(BookingForm1, self).clean()


class BookingForm2(forms.Form):
    make = forms.ChoiceField(required=True,
                             widget=forms.Select(),
                             choices=((None, None),),
                             label='Select bike make')
    number = forms.IntegerField(label='Number of bikes you would like to rent')


class BookingForm3(forms.Form):
    size = forms.ChoiceField(required=True, widget=forms.Select(), choices=((None, None),))

BookingFormSet = formset_factory(BookingForm3, extra=2)