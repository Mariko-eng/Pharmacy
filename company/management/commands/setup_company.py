from django.core.management.base import BaseCommand
from company.models import Company
from utils.defaults.init_company_groups import init_company_groups

class Command(BaseCommand):
    help = 'Sets default company groups and permissions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting default company groups and permissions...'))

        self.create_company_groups()

        self.stdout.write(self.style.SUCCESS('Default company groups and permissions set successfully.'))


    def create_company_groups(self, *args, **options):
        companies = Company.objects.all()

        for company in companies:
            init_company_groups(company_id=company.pk)
