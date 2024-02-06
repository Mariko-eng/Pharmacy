from django.db import models
from .mixins import Base

class CompanyApplication(Base):
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


class Company(Base):
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

class Store(Base):
    STORE_TYPES = [('RETAIL', 'RETAIL'),('WHOLESALE', 'WHOLESALE'),]
    STATUS_TYPES = [('OPEN', 'OPEN'),('CLOSED', 'CLOSED'),]

    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    store_type = models.CharField(max_length=255,choices=STORE_TYPES)
    status_type = models.CharField(max_length=255,choices=STATUS_TYPES)
    name = models.CharField(max_length = 225)
    phone = models.CharField(max_length = 225)
    email = models.EmailField(blank=True, null=True)
    location_district = models.CharField(max_length = 225, blank=True, null=True)
    location_village = models.CharField(max_length = 225, blank=True, null=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class PosCenter(Base):
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    name = models.CharField(max_length = 225)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} - {self.store.name}"


class SupplierEntity(Base):
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=225)
    email = models.EmailField(null=True, blank=True)
    location = models.CharField(max_length=225, null=True, blank=True)
    updated_by = models.CharField(max_length=225, null=True, blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="suppliers_createdby")

    def __str__(self):
        return self.name
    
class Client(Base):
    store = models.ForeignKey(Store,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="posusers")

    def __str__(self):
        return self.name






