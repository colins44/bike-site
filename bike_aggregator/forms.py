from django.forms import ModelForm
from bike_aggregator.models import BikeShop, BikeSearch
from django import forms
from django.core.mail import send_mail

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


class BikeRentalForm(ModelForm):
    location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Where do you want to go?'}),
        label="Location:"
    )
    class Meta:
        model = BikeSearch
        exclude = ('pk',)


class ContactForm(forms.Form):

    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()

    def send_email(self):
        send_mail('Contact from the bike site', self.cleaned_data['message'], self.cleaned_data['email'],
            ['colin.pringlewood@gmail.com'], fail_silently=False)


