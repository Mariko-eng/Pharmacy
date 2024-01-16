from django.db import models
from .mixins import CommonFieldsMixin

class CompanyApplication(CommonFieldsMixin):
    STATUS_TYPES = [('PENDING', 'PENDING'), 
                    ('APPROVED', 'APPROVED'),
                    ('CREATED', 'CREATED'),
                    ('DECLINED', 'DECLINED'),
                    ('CANCELLED', 'CANCELLED'),]

    name = models.CharField(max_length = 225)
    phone = models.CharField(max_length = 225)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length = 225, null=True, blank=True)
    logo = models.ImageField(upload_to="company/logo", null=True)
    status = models.CharField(max_length=255, choices=STATUS_TYPES, default="PENDING")
    activation_code = models.CharField(max_length = 225, null=True, blank=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)


class Company(CommonFieldsMixin):
    application = models.ForeignKey(CompanyApplication,null=True,on_delete=models.SET_NULL)
    name = models.CharField(max_length=225)
    phone = models.CharField(max_length=225)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=225, null=True, blank=True)
    logo = models.ImageField(upload_to="company/logo", null=True)
    activation_code = models.CharField(max_length = 225, null=True, blank=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Store(models.Model):
    STORE_TYPES = [('RETAIL', 'RETAIL'),('WHOLESALE', 'WHOLESALE'),]
    STATUS_TYPES = [('OPEN', 'OPEN'),('CLOSED', 'CLOSED'),]

    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    name = models.CharField(max_length = 225)
    phone = models.CharField(max_length = 225)
    email = models.EmailField(blank=True, null=True)
    store_type = models.CharField(max_length=255,choices=STORE_TYPES)
    status = models.CharField(max_length=255,choices=STATUS_TYPES)
    location_district = models.CharField(max_length = 225, blank=True, null=True)
    location_village = models.CharField(max_length = 225, blank=True, null=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class PosCenter(CommonFieldsMixin):
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    name = models.CharField(max_length = 225)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)


class Supplier(CommonFieldsMixin):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=225)
    email = models.EmailField(null=True, blank=True)
    location = models.CharField(max_length=225, null=True, blank=True)
    updated_by = models.CharField(max_length=225, null=True, blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="suppliers_createdby")

    def __str__(self):
        return self.name
    
# class Provider(CommonFieldsMixin):
#     PROVIDER_TYPES = [('SUPPLIER', 'SUPPLIER'),('STORE', 'STORE'),]
    
#     company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
#     provider_type = models.CharField(max_length=10,choices=PROVIDER_TYPES,default="SUPPLIER")
#     supplier_entity = models.ForeignKey(SupplierEntity,on_delete=models.SET_NULL,null=True)
#     supplier_store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
#     updated_by = models.CharField(max_length=225,null=True,blank=True)
#     created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="providers_createdby")


class Customer(CommonFieldsMixin):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="posusers")

    def __str__(self):
        return self.name






