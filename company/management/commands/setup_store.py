from django.core.management.base import BaseCommand
from company.models import Store
from utils.defaults.init_store_groups import init_store_groups

class Command(BaseCommand):
    help = 'Sets default store groups and permissions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting default store groups and permissions...'))

        self.create_store_groups()

        self.stdout.write(self.style.SUCCESS('Default store groups and permissions set successfully.'))


    def create_store_groups(self, *args, **options):
        stores = Store.objects.all()

        for store in stores:
            init_store_groups(store_id=store.pk)