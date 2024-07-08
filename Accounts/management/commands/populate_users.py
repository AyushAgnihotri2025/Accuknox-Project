import random
from django.core.management.base import BaseCommand
from faker import Faker

from Accounts.models import User


class Command(BaseCommand):
    help = 'Populate the database with fake user data'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        fake = Faker()

        # Entering Test Data
        email = 'testuser@mrayush.in'
        name = 'Ayush Test User'
        password = 'password123'  # You can generate a random password if needed

        User.objects.create_user(email=email, name=name, password=password)

        for _ in range(total):
            name = fake.name()
            email = f"{name.replace(' ', '.')}{fake.random_int(11111, 9999999)}@{fake.domain_name()}"
            password = 'password123'  # You can generate a random password if needed

            User.objects.create_user(email=email, name=name, password=password)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} users'))
