from django.forms import model_to_dict
from django.test import TestCase
from bike_aggregator.models import BikeSearch, BikeShop
from .forms import BikeRentalForm, SignUpForm


class TestForms(TestCase):

    def test_get_home_page(self):
        resp = self.client.get('/bikes-to-rent/')
        self.assertEqual(resp.status_code, 200)

    def test_bike_search_form(self):
        bike_rental_form_data = {
            'location': 'paris',
            'bike_type': 'road_bike',
            'no_of_bikes': 10,
            'email':'email@example.com'
        }
        form = BikeRentalForm(data=bike_rental_form_data)
        self.assertTrue(form.is_valid())

    def test_bike_shop_form(self):
        signup_form_data = {
            'town_or_region': 'paris',
            'country': 'France',
            'shop_name': 'road_bike',
            'website': 'https://google.com',
            'email': 'admin@example.com'
        }
        form = SignUpForm(data=signup_form_data)
        self.assertTrue(form.is_valid())

    def test_post_to_home_page(self):
        bike_rental_form_data = {
            'location': 'harare',
            'bike_type': 'road_bike',
            'no_of_bikes': 10,
            'email': 'admin@example.com'
        }
        resp = self.client.post(
            path='/bicycles-to-rent/',
            data=bike_rental_form_data
        )
        self.assertEqual(resp.status_code, 302)
        bike_search = BikeSearch.objects.get(location=bike_rental_form_data['location'])
        bike_search = model_to_dict(bike_search)
        self.assertDictContainsSubset(bike_rental_form_data, bike_search)
        self.assertEqual(BikeSearch.objects.all().count(), 1)


    def test_post_to_signup_page(self):
        signup_form_data={
            'town_or_region': 'paris',
            'country': 'France',
            'shop_name': 'road_bike',
            'website': 'https://google.com',
            'email':'email@example.com'
        }
        resp = self.client.post(
            path='/sign-up/',
            data=signup_form_data
        )
        self.assertEqual(resp.status_code, 302)
        bike_shop = BikeShop.objects.get(website=signup_form_data['website'])
        bike_shop = model_to_dict(bike_shop)
        self.assertDictContainsSubset(signup_form_data, bike_shop)
        self.assertEqual(BikeShop.objects.all().count(), 1)


# Create your tests here.
