from django.db import models
from django.contrib.auth.models import Group
from .mixins import Base
from user.constants.permissions.company import *
from utils.shared.slugify import unique_slugify


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
    status = models.CharField(max_length=225, choices=STATUS_TYPES, default="PENDING")
    activation_code = models.CharField(max_length = 225, null=True, blank=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)

    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = company_application_permissions


class Company(Base):
    application = models.ForeignKey(CompanyApplication,null=True,on_delete=models.SET_NULL)
    name = models.CharField(max_length=225)
    phone = models.CharField(max_length=225)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=225, null=True, blank=True)
    logo = models.ImageField(upload_to="company/logo", null=True)
    slug = models.SlugField(blank=True, null=True)
    activation_code = models.CharField(max_length = 225, null=True, blank=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)

    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = company_permissions

    def __str__(self):
        return self.name
    
    def save(self, **kwargs): #  Override the save method
        slug_str = "%s" % (self.name) 
        unique_slugify(self, slug_str) 
        super(Company, self).save(**kwargs)
    
class CompanyLevelGroup(Base): # Company level groups
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length = 225, blank=True, null=True)
    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = company_group_level_permissions

class Store(Base):
    STORE_TYPES = [('RETAIL', 'RETAIL'),('WHOLESALE', 'WHOLESALE'),]
    STATUS_TYPES = [('OPEN', 'OPEN'),('CLOSED', 'CLOSED'),]

    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    store_type = models.CharField(max_length=225,choices=STORE_TYPES)
    status_type = models.CharField(max_length=225,choices=STATUS_TYPES)
    name = models.CharField(max_length = 225)
    phone = models.CharField(max_length = 225)
    email = models.EmailField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    location_district = models.CharField(max_length = 225, blank=True, null=True)
    location_village = models.CharField(max_length = 225, blank=True, null=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)

    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = store_permissions

    def __str__(self):
        return self.name

    def save(self, **kwargs): #  Override the save method
        slug_str = "%s %s" % (self.company.name, self.name) 
        unique_slugify(self, slug_str) 
        super(Store, self).save(**kwargs)


class StoreLevelGroup(Base): # Company level groups
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length = 225, blank=True, null=True)

    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = store_group_level_permissions


class PosCenter(Base):
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    name = models.CharField(max_length = 225)
    slug = models.SlugField(blank=True, null=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL)

    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = pos_center_permissions

    def __str__(self):
        return f"{self.name} - {self.store.name}"

    def save(self, **kwargs): #  Override the save method
        slug_str = "%s %s" % (self.store.name, self.name) 
        unique_slugify(self, slug_str) 
        super(Store, self).save(**kwargs)

class SupplierEntity(Base):
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    phone = models.CharField(max_length=225)
    email = models.EmailField(null=True, blank=True)
    location = models.CharField(max_length=225, null=True, blank=True)
    updated_by = models.CharField(max_length=225, null=True, blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="suppliers_createdby")

    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = supplier_entity_permissions

    def __str__(self):
        return self.name
    
class Client(Base):
    store = models.ForeignKey(Store,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=225)
    phone = models.CharField(max_length=225,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="posusers")

    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = client_permissions

    def __str__(self):
        return self.name






