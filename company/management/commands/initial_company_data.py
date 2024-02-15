# from company.models import Company
# from django.core.management.base import BaseCommand
# from faker import Faker


# def create_fake_companies(num_products=5):
#     fake = Faker()

#     for _ in range(num_products):
#         # Create a fake product with random data
#         name = fake.unique.word()
#         phone = fake.word()
#         email = fake.email()
#         location = fake.word()
#         activation_code =fake.unique.random_int(min=100000, max=999999)
#         created_at = fake.date_time_between(start_date="-30d", end_date="now")


#         # Create a new Product instance and save it to the database
#         company = Company.objects.create(
#             name=name,
#             phone=phone,
#             email=email,
#             location=location,
#             activation_code = activation_code,
#             created_at = created_at
#         )
#         company.save()

#     print(f"{num_products} fake products created successfully.")


# class Command(BaseCommand):
#     help = 'Sets default companies'

#     def handle(self, *args, **options):
#         create_fake_companies(num_products=5)

