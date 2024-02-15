# from company.models import Company, Store
# from django.core.management.base import BaseCommand
# from faker import Faker


# def get_company_ids():
#     # Get all categories from the Category model
#     companies = Company.objects.all()

#     # Extract a list of category IDs
#     company_ids = [company.id for company in companies]

#     return company_ids

# class Provider(fake.providers.BaseProvider):
#     def get_store_statuses(self):
#         return [status[0] for status in Store.STATUS_TYPES]
    
#     def get_store_types(self):
#         return [store_type[0] for store_type in Store.STORE_TYPES]


# def create_fake_stores(num=5):
#     fake = Faker()
#     fake.add_provider(Provider)

#     for _ in range(num):
#         # Create a fake product with random data
#         company = fake.random_element(elements=get_company_ids())
#         store_status = fake.random_element(elements=fake.get_store_statuses())
#         store_type = fake.random_element(elements=fake.get_store_types())
#         name = fake.unique.word()
#         phone = fake.word()
#         email = fake.email()
#         location_district = fake.word()
#         location_village = fake.word()
#         created_at = fake.date_time_between(start_date="-30d", end_date="now")


#         # Create a new Product instance and save it to the database
#         store = Store.objects.create(
#             company = company,
#             store_type = store_type,
#             status = store_status,
#             name=name,
#             phone=phone,
#             email=email,
#             location_district=location_district,
#             location_village = location_village,
#             created_at = created_at
#         )
#         store.save()

#     print(f"{num} fake products created successfully.")


# class Command(BaseCommand):
#     help = 'Sets default companies'

#     def handle(self, *args, **options):
#         create_fake_stores(num=7)

