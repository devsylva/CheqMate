from django.core.management.base import BaseCommand
from faker import Faker
from  apps.cart.models import Product
import random 


class Command(BaseCommand):

    # this script creates dummy pruducts in the database
    def handle(self, *args, **kwargs):
        
        #Initialize Faker
        fake = Faker()

        # Define some sample categories (modify as needed)
        categories = ['Electronics', 'Clothing', 'Groceries', 'Books', 'Furniture', 'Toys']

        # Create dummy products
        for _ in range(100):  # Change the range number to control the number of products
            product = Product.objects.create(
                name=fake.word().capitalize() + ' ' + fake.word().capitalize(),  # Fake product name
                description=fake.sentence(),  # Fake description
                barcode=fake.binary(length=16),  # Fake barcode
                price=round(random.uniform(5.00, 1000.00), 2),  # Random price between 5 and 1000
            )
            product.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the Product model with dummy data.'))