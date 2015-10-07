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

moto_bike_types = (
    ('scooter', 'scooter'),
    ('sports_bike', 'sports bike'),
    ('sports_touring', 'sports touring'),
    ('touring_bike', 'touring bike'),
    ('offroad', 'offroad'),
)


class SignUpForm(ModelForm):

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

class BikeRentalFormOne(forms.Form):
    location = forms.CharField(required=True, max_length=255, help_text='Where do you want to go?', label="Location:")
    no_of_bikes = forms.IntegerField(required=True, min_value=0, label='Number of bikes:')
    bike_type = forms.ChoiceField(choices=bike_types, required=True)

    def save(self):
        data = self.cleaned_data
        bs = BikeSearch.objects.create(
            location=data.get('location'),
            no_of_bikes=data.get('no_of_bikes'),
            bike_type=data.get('bike_type'),
            email='admin@example.com',
            phone_number='+447470142526'
        )
        print bs

class MotoBikeHireForm(forms.Form):
    location = forms.CharField(required=True, max_length=255, help_text='Where do you want to go?', label="Location:")
    no_of_bikes = forms.IntegerField(required=True, min_value=0, label='Number of bikes:')
    bike_type = forms.ChoiceField(choices=moto_bike_types, required=True)

    def save(self):
        data = self.cleaned_data
        bs = BikeSearch.objects.create(
            location=data.get('location'),
            no_of_bikes=data.get('no_of_bikes'),
            bike_type=data.get('bike_type'),
            email='admin@example.com',
            phone_number='+447470142526'
        )
        print bs
