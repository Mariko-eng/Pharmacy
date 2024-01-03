from django.db import models
from .mixins import CommonFieldsMixin

class CompanyApplication(CommonFieldsMixin):
    STATUS_TYPES = [('PENDING', 'PENDING'), ('APPROVED', 'APPROVED'),('DECLINED', 'DECLINED'),]

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
    name = models.CharField(max_length = 225)
    phone = models.CharField(max_length = 225)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length = 225, null=True, blank=True)
    logo = models.ImageField(upload_to="company/logo", null=True)
    activation_code = models.CharField(max_length = 225, null=True, blank=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)


class Store(CommonFieldsMixin):
    STORE_TYPES = [('RETAIL', 'RETAIL'),('WHOLESALE', 'WHOLESALE'),]
    STATUS_TYPES = [('OPEN', 'OPEN'),('CLOSED', 'CLOSED'),]

    name = models.CharField(max_length = 225)
    location = models.CharField(max_length = 225)
    phone = models.CharField(max_length = 225)
    store_type = models.CharField(max_length=255,choices=STORE_TYPES)
    status_type = models.CharField(max_length=255,choices=STATUS_TYPES)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)

    
class PosCenter(CommonFieldsMixin):
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    name = models.CharField(max_length = 225)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)


class SupplierEntity(CommonFieldsMixin):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="suppliers_createdby")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Provider(CommonFieldsMixin):
    PROVIDER_TYPES = (('SUPPLIER', 'Supplier'),('BRANCH', 'Branch'),)
    
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    provider_type = models.CharField(max_length=10,choices=PROVIDER_TYPES,default="Supplier")
    supplier_entity = models.ForeignKey(SupplierEntity,on_delete=models.SET_NULL,null=True)
    supplier_store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="providers_createdby")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

class Customer(CommonFieldsMixin):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="posusers")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name






