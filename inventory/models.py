from uuid import uuid4
from django.db import models
from company.models import Company
from company.models import Store
from company.models import SupplierEntity
from company.mixins import Base
from django.template.defaultfilters import slugify
from utils.permissions.inventory import *

class Category(Base):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 
    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = category_permissions
        unique_together = ('name', 'store')
    
class Variant(Base):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 
    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = variant_permissions
        unique_together = ('name', 'store')

class Units(Base): # Units Of Measure
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = units_permissions
        unique_together = ('name', 'store')

class StockItem(Base):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    # Data    
    unique_no = models.CharField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(Variant,on_delete=models.SET_NULL, null=True)
    units = models.ForeignKey(Units,on_delete=models.SET_NULL, null=True)
    item_photo = models.ImageField(upload_to="products", null=True)    
    unit_price = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    reorder_min_qty = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    available_qty = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    actual_qty = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    is_for_sale = models.BooleanField(default=True)
    is_consummable = models.BooleanField(default=False)
    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="stock_items_createdby")

    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = stock_item_permissions
        ordering = ("-created_at",)

    def __str__(self):
        if self.variant is None:
            return f"{self.name} - {self.units}"
        return f"{self.name} - {self.variant} - {self.units}"

    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.name, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.name, self.uniqueId))

        super(StockItem, self).save(*args, **kwargs)

class ReceivedStock(Base):
    SUPPLIER_TYPES = [('SUPPLIER', 'SUPPLIER'),('STORE', 'STORE'),]
    STATUS_TYPES = [('PENDING', 'PENDING'),('APPROVED', 'APPROVED'),('CANCELLED', 'CANCELLED'),]

    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data
    
    supplier_type = models.CharField(max_length=10,choices=SUPPLIER_TYPES,default="SUPPLIER")
    supplier_entity = models.ForeignKey(SupplierEntity,on_delete=models.SET_NULL,null=True)
    supplier_store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True, related_name="received_stock")
    delivered_by_name = models.CharField(max_length=255)
    delivered_by_phone = models.CharField(max_length=255)
    received_date = models.DateField(null=True)
    delivery_notes = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=10,choices=STATUS_TYPES, default="PENDING")
    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User", null=True, on_delete=models.SET_NULL, related_name="received_stocks_createdby")
    
    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = received_stock_permissions
        ordering = ("-created_at",)

    @property
    def recv_stock_unique_id(self):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.save()
            
        return self.uniqueId

    @property 
    def items_count(self):
        return self.receivedstockitem_set.count()
 
    @property
    def total_cost(self):
        total = 0
        items = self.receivedstockitem_set.all()
        for item in items:
            total = total + item.total_cost
        return total


    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        super(ReceivedStock, self).save(*args, **kwargs)

    @property
    def provider_details(self):
        if self.supplier_type == "SUPPLIER":
            return self.supplier_entity
        elif self.supplier_type == "STORE":
            return self.supplier_store
        else:
            return "Nan"
 
 
class ReceivedStockItem(Base):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data
    received_stock = models.ForeignKey(ReceivedStock,on_delete=models.CASCADE)
    stock_item = models.ForeignKey(StockItem,on_delete=models.CASCADE)
    batch_no = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    total_cost = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    manufactured_date = models.DateField(null=True)
    expiry_date = models.DateField(null=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="received_stock_items_createdby")

    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = received_stock_item_permissions
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.batch_no} - {self.stock_item.name}"

class StockRequest(Base):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DECLINED', 'Declined'),
    ]
 
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data
    request_date = models.DateField(null=True)
    delivery_date = models.DateField(null=True) # Expected  Delivery Date
    request_notes = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=225, choices=STATUS_CHOICES, default='PENDING')
    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="stock_requests_createdby")

    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = stock_request_permissions
        ordering = ("-created_at",)

    @property
    def stock_req_unique_id(self):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.save()        
        return self.uniqueId

    def __str__(self):
        return f"{self.request_date} - {self.status}"
    
    @property
    def items_count(self):
        return self.stockrequestitem_set.count()
    
    @property
    def total_cost(self):
        total = 0
        items = self.stockrequestitem_set.all()
        for item in items:
            total = total + (item.stock_item.unit_price * item.quantity)
        return total
    
    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        super(StockRequest, self).save(*args, **kwargs)

class StockRequestItem(Base):
    REASON_CHOICES = (
        ('Low Stock', 'Low Stock'),
        ('New Product', 'New Product'),
        ('Other', 'Other'),
    ) 
        
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data
    stock_request = models.ForeignKey(StockRequest, on_delete=models.CASCADE)
    stock_item = models.ForeignKey(StockItem,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    available_quantity = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    reason = models.CharField(max_length=225, choices=REASON_CHOICES, default='Low Stock')
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="stock_request_items_createdby")

    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = stock_request_item_permissions
        ordering = ("-created_at",)

    def __str__(self):
        return self.stock_item.product.name
    

# class OutgoingConsumable(Base):
#     #Owner
#     company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
#     store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
#     # Data
#     stock_item = models.ForeignKey(StockItem,on_delete=models.CASCADE)
#     quantity = models.DecimalField(max_digits=12,decimal_places=3)
#     remarks = models.TextField(null=True,blank=True)
#     updated_by = models.CharField(max_length=225,null=True,blank=True)
#     created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="outgoing_consumables_createdby")

#     def __str__(self):
#         return self.stock_item.name
