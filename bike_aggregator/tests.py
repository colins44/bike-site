from django.forms import model_to_dict
from django.test import TestCase
from bike_aggregator.models import BikeSearch, BikeShop, RentalEquipment
from .forms import BikeRentalForm, SignUpForm, ContactForm


class TestForms(TestCase):

    def test_get_home_page(self):
        resp = self.client.get('/bikes-to-rent/')
        self.assertEqual(resp.status_code, 200)

    def test_bike_search_form(self):
        bike_rental_form_data = {
            'location': 'paris',
            'bike_type': 'road_bike',
            'no_of_bikes': 10,
            'email': 'email@example.com'
        }
        form = BikeRentalForm(data=bike_rental_form_data)
        self.assertTrue(form.is_valid())

    def test_bike_shop_form(self):
        bike = RentalEquipment.objects.create(name='bike')
        signup_form_data = {
            'location': 'paris',
            'country': 'France',
            'city': 'Paris',
            'latitude': -123.1234,
            'longitude': 123.1234,
            'post_code': 'w1 3ce',
            'state': 'North Korea',
            'street': 'charring cross',
            'street_number': '77A',
            'shop_name': 'road_bike',
            'website': 'https://google.com',
            'email': 'admin@example.com',
            'rental_options': [bike.pk,]
        }
        form = SignUpForm(data=signup_form_data)
        self.assertTrue(form.is_valid())
        form.save()

        bikeshop = BikeShop.objects.get(email=signup_form_data['email'])
        self.assertEquals(signup_form_data['latitude'], float(bikeshop.latitude))
        self.assertEquals(signup_form_data['longitude'], float(bikeshop.longitude))
        bikeshop = model_to_dict(bikeshop)
        bikeshop.pop('longitude')
        bikeshop.pop('latitude')
        signup_form_data.pop('latitude')
        signup_form_data.pop('longitude')
        self.assertDictContainsSubset(signup_form_data, bikeshop)

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
        bike = RentalEquipment.objects.create(name='bike')
        signup_form_data = {
            'location': 'harare',
            'country': 'zimbabwe',
            'city': 'harare',
            'latitude': -180.1234,
            'longitude': 180.1234,
            'post_code': 'w1 3ce',
            'state': 'North Korea',
            'street': 'charring cross',
            'street_number': '77A',
            'shop_name': 'road_bike',
            'website': 'https://google.com/?news=bbc',
            'email': 'admin@example.com',
            'rental_options': [bike.pk,]
        }
        resp = self.client.post(
            path='/sign-up/',
            data=signup_form_data
        )
        self.assertEqual(resp.status_code, 302)
        bike_shop = BikeShop.objects.get(website=signup_form_data['website'])
        bike_shop = model_to_dict(bike_shop)
        bike_shop.pop('longitude')
        bike_shop.pop('latitude')
        signup_form_data.pop('latitude')
        signup_form_data.pop('longitude')
        self.assertDictContainsSubset(signup_form_data, bike_shop)
        self.assertEqual(BikeShop.objects.all().count(), 1)

    def test_sending_equiry_email(self):
        self.assertTrue(ContactForm.send_mail('testing', ['admin@email.com', {}]))


# Create your tests here.
