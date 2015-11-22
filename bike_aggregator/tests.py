from decimal import Decimal
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from bike_aggregator.models import BikeShop, Stock
from bike_aggregator.utils import pythagoris, EMail, distance_filter, expand_search_area


class TestPythagorus(TestCase):

    def test_with_positive_numbers(self):
        distance = pythagoris(longs=(20,30), lats=(20,30))
        self.assertEqual(distance, 14.142136)

    def test_with_negative_numbers(self):
        distance = pythagoris(longs=(-20,-30), lats=(-20,-30))
        self.assertEqual(distance, 14.142136)

    def test_with_postive_and_negative_numbers(self):
        distance = pythagoris(longs=(5,-5), lats=(-5,5))
        self.assertEqual(distance, 14.142136)


class TestSendingEmail(TestCase):

    def test_email_sending_txt(self):
        email = EMail(to='contact@example.com', subject='test', fail_silently=False)
        ctx = {'username': 'Oz Katz'}
        email.text('emails/enquiry.txt', ctx)
        self.assertIsNone(email.send())

    def test_email_sending_txt(self):
        email = EMail(to='contact@example.com', subject='test', fail_silently=False)
        ctx = {'username': 'Oz Katz'}
        email.text('emails/enquiry.txt', ctx)
        self.assertIsNone(email.send())


class TestDistanceFilter(TestCase):


    def setUp(self):
        self.bike_shop_sicily = BikeShop.objects.create(
            location="sicily",
            latitude=37.0834,
            longitude=15.1537,
        )
        self.bike_shop_paris = BikeShop.objects.create(
            location="Paris",
            latitude=48.8567,
            longitude=2.3508,
        )
        self.bike_shop_amsterdam = BikeShop.objects.create(
            location="Amsterdam",
            latitude=52.3465,
            longitude=4.9177,
        )

        self.bike_search = {}

    def test_bike_search_paris(self):
        self.bike_search['latitude'] = Decimal(49.8567)
        self.bike_search['longitude'] = Decimal(2.5908)
        filtered_result = distance_filter(self.bike_search, BikeShop.objects.all(), distance=20)
        self.assertEqual(filtered_result[0].location, self.bike_shop_paris.location)
        self.assertEqual(filtered_result[2].location, self.bike_shop_sicily.location)

    def test_bike_search_amsterdam(self):
        self.bike_search['latitude'] = Decimal(52.3465)
        self.bike_search['longitude'] = Decimal(4.9177)
        filtered_result = distance_filter(self.bike_search, BikeShop.objects.all(), distance=20)
        self.assertEqual(filtered_result[0].location, self.bike_shop_amsterdam.location)
        self.assertEqual(filtered_result[2].location, self.bike_shop_sicily.location)

    def test_bike_search_rome(self):
        self.bike_search['latitude'] = Decimal(41.9000)
        self.bike_search['longitude'] = Decimal(12.5000)
        filtered_result = distance_filter(self.bike_search, BikeShop.objects.all(), distance=20)
        self.assertEqual(filtered_result[0].location, self.bike_shop_sicily.location)
        self.assertEqual(filtered_result[2].location, self.bike_shop_amsterdam.location)

    def test_expand_search_area(self):
        """
        Expand search area should only expand a certain amount then stop
        """
        self.bike_search['latitude'] = Decimal(52.3465)
        self.bike_search['longitude'] = Decimal(4.9177)
        returned_queryset = expand_search_area(self.bike_search, BikeShop.objects.all())
        self.assertEqual(len(returned_queryset), 1)


class TestAuthenticationNeeded(TestCase):


    def setUp(self):
        self.views = [
            ['stock-list', {}],
            ['stock-create', {}],
            ['stock-update', {'pk': 1}],
            ['stock-delete', {'pk': 1}]
        ]

    def test_call_view_denies_anonymous(self):

        for view in self.views:
            response = self.client.get(reverse(view[0], kwargs=view[1]), follow=True)
            self.assertRedirects(response, '/accounts/login/?next={}'.format(reverse(view[0], kwargs=view[1])))


class TestStockCrud(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='testing',
            email='email@example.com',
            password='testing'
        )

        self.user2 = User.objects.create_user(
            username='user2',
            email='email@example2.com',
            password='testing1'
        )

        self.data = {
            'type': 'type',
            'no_in_stock': 2,
            'make': 'make',
            'year': 2002

        }
        self.stock = Stock.objects.create(
            type='road_bike',
            owned_by=self.user,
            no_in_stock=1,
        )
        self.client.login(username=self.user.username, password='testing')

    def test_create(self):
        '''
        Create an item of stock and then check the list view to see it
        '''
        resp = self.client.post('/stock/create/', data=self.data)
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get(reverse('stock-list'))
        self.assertEquals(len(resp.context['object_list']), 2)

    def test_update_stock(self):
        self.data['type'] = 'new_type'
        resp = self.client.post('/stock/update/{}/'.format(self.stock.pk), data=self.data)
        self.assertRedirects(resp, reverse('stock-list'))
        self.stock.type = 'new_type'

    def test_other_user_cannot_update(self):
        self.client.logout()
        self.client.login(username=self.user2.username, password='testing1')
        self.data['type'] ='old_name'
        resp = self.client.post('/stock/update/{}/'.format(self.stock.pk), data={'type': 'old_name'})
        self.assertEquals(resp.status_code, 404)
        self.stock.type = 'road_bike'

    def test_other_user_sees_nothing(self):
        self.client.logout()
        self.client.login(username=self.user2.username, password='testing1')
        response = self.client.get(reverse('stock-list'))
        self.assertEquals(len(response.context['object_list']), 0)

    def test_delete_stock_diffrent_user(self):
        self.client.logout()
        self.client.login(username=self.user2.username, password='testing1')
        response = self.client.post('/stock/delete/{}/'.format(self.stock.pk))
        self.assertEquals(response.status_code, 404)
        self.assertEquals(Stock.objects.count(), 1)

    def test_delete_stock(self):
        self.client.login(username=self.user.username, password='testing')
        response = self.client.post('/stock/delete/{}/'.format(self.stock.pk))
        self.assertRedirects(response, reverse('stock-list'))
        self.assertEquals(Stock.objects.count(), 0)

class TestShopCrud(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='testing',
            email='email@example.com',
            password='testing'
        )

        self.user2 = User.objects.create_user(
            username='user2',
            email='email@example2.com',
            password='testing1'
        )

        self.data = {
            'shop_name': 'testing',
            'location': 'locations',
            'email': 'email@example.com',
            'telephone': '+12313213213123'
        }
        self.client.login(username=self.user.username, password='testing')

        self.bikeshop = BikeShop.objects.create(
            shop_name='the shop',
            email='shop@email.com',
            location='harare',
            phone_number=+123123123123,
            owned_by=self.user2,
        )

    def test_get_empty_profile(self):
        resp = self.client.get('/profile/')
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['object_list']), 0)

    def test_get_profile_when_not_logged_in(self):
        self.client.logout()
        resp = self.client.get('/profile/')
        self.assertRedirects(resp, '/accounts/login/?next={}'.format('/profile/'))

    def test_create_profile(self):
        self.client.login(username=self.user.username, password='testing')
        resp = self.client.post(reverse('shop-create'), data=self.data)
        self.assertEquals(resp.status_code, 302)
        resp = self.client.get('/profile/')
        self.assertEquals(len(resp.context['object_list']), 1)

        #now update your profile
        self.data['email'] = 'new@email.com'
        self.client.post(reverse('shop-update', kwargs={'pk': 2}), data=self.data)
        resp = self.client.get('/profile/')
        self.assertEquals(len(resp.context['object_list']), 1)
        self.assertEquals(resp.context['object_list'][0].email, 'new@email.com')

    def test_delete_shop(self):
        self.client.login(username=self.user2.username, password='testing1')
        resp = self.client.get(reverse('shop-detail'))
        self.assertEquals(len(resp.context['object_list']), 1)
        self.client.post('/profile/delete/{}/'.format(self.bikeshop.pk))
        self.assertEquals(BikeShop.objects.filter(owned_by=self.user2).count(), 0)





