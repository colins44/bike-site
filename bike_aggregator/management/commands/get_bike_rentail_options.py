from django.core.management.base import BaseCommand
from bike_aggregator.models import BikeShop, RentalEquipment
import json


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'


    def handle(self, *args, **options):
        with open('bike_aggregator/db.json') as data_file:
            data = json.load(data_file)

        for x in data:
            if x['model'] == 'bike_aggregator.bikeshop':
                bike_shop = BikeShop.objects.get(pk=x['pk'])
                bike_shop.rental_options.add(*x['fields']['rental_options'])
