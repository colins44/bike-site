from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from bike_aggregator.models import BikeShop, Prices
import random


prices = {
    'cruiser-bicycle': [10, 16],
    'touring-bicycle': [10, 16],
    'hybrid-bike': [10, 16],
    'road-bike': [25, 40],
    'mountain-bike': [22, 34],
    'kids-bikes': [10, 13],
    'tandem-bike': [15, 20],
    'electric-bicycle': [25, 35],
    'scooter': [35, 50],

}

class Command(BaseCommand):
    help = 'create random prices for all shops'


    def handle(self, *args, **options):
        for bikeshop in BikeShop.objects.all():
            for rental_equipment in bikeshop.rental_options.all():
                price_range = prices.__getitem__(rental_equipment.slug)
                try:
                    price = Prices.objects.get(bike_shop=bikeshop, rental_equipment=rental_equipment)
                except ObjectDoesNotExist:
                    price = Prices.objects.create(
                        bike_shop=bikeshop,
                        rental_equipment=rental_equipment,
                        price=random.randrange(min(price_range), max(price_range))
                    )
                else:
                    price.price = random.randrange(min(price_range), max(price_range))
                    price.save()

