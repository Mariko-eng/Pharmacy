from django.core.management.base import BaseCommand
from utils.defaults.init_app_groups import init_app_groups


class Command(BaseCommand):
    help = 'Sets default app groups and permissions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting default app groups and permissions...'))

        self.create_app_groups()

        self.stdout.write(self.style.SUCCESS('Default app groups and permissions set successfully.'))


    def create_app_groups(self, *args, **options):
        init_app_groups()