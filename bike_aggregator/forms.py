from django.forms import ModelForm
from bike_aggregator.models import BikeShop, BikeSearch
from django import forms
from django.core.mail import send_mail


class SignUpForm(ModelForm):

    class Meta:
        model = BikeShop
        exclude = ('pk',)

        
    def save(self, commit=True):
        super(SignUpForm, self).save(commit)

class BikeRentalForm(ModelForm):

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


