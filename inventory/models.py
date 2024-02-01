from django.template.defaultfilters import slugify
from django.utils import timezone
from uuid import uuid4
from django.db import models
from company.models import Company
from company.models import Store
from company.models import PosCenter
from company.models import Supplier
from company.mixins import Base

class ProductCategory(Base):
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('name', 'company')
    
class ProductVariant(Base):
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 
    class Meta:
        unique_together = ('name', 'company')

class ProductUnits(Base): # Units Of Measure
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('name', 'company')

class Product(Base):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    # Data    
    unique_no = models.CharField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    # description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(ProductCategory,on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(ProductVariant,on_delete=models.SET_NULL, null=True)
    units = models.ForeignKey(ProductUnits,on_delete=models.SET_NULL, null=True)
    # unit_price = models.DecimalField(max_digits=12, decimal_places=3)
    # available_qty = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    # reorder_min_qty = models.DecimalField(max_digits=12, decimal_places=3,default=0)
    # item_photo = models.ImageField(upload_to="products", null=True)
    # is_consummable = models.BooleanField(default=False)
    # is_for_sale = models.BooleanField(default=True)

    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="products_createdby")

    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ('name', 'company')

    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.name, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.name, self.uniqueId))

        super(Product, self).save(*args, **kwargs)

class StoreProduct(Base):
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    # Data
    description = models.TextField(blank=True, null=True)
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
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="store_products_createdby")

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.product.name} - {self.product.variant} - {self.product.category}"

    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.product.name, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.product.name, self.uniqueId))

        super(StoreProduct, self).save(*args, **kwargs)
    
class ReceivedStock(Base):
    SUPPLIER_TYPES = [('SUPPLIER', 'SUPPLIER'),('STORE', 'STORE'),]
    STATUS_TYPES = [('PENDING', 'PENDING'),('APPROVED', 'APPROVED'),('CANCELLED', 'CANCELLED'),]

    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data
    
    supplier_type = models.CharField(max_length=10,choices=SUPPLIER_TYPES,default="SUPPLIER")
    supplier_entity = models.ForeignKey(Supplier,on_delete=models.SET_NULL,null=True)
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
    store_product = models.ForeignKey(StoreProduct,on_delete=models.CASCADE)
    batch_no = models.CharField(max_length=255)
    qty_received = models.DecimalField(max_digits=12, decimal_places=3)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    total_cost = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    manufactured_date = models.DateField(null=True)
    expiry_date = models.DateField(null=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="received_stock_items_createdby")

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.store_product.product.name

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
            total = total + (item.store_product.unit_price * item.quantity)
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
    store_product = models.ForeignKey(StoreProduct,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    available_quantity = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    reason = models.CharField(max_length=225, choices=REASON_CHOICES, default='Low Stock')
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="stock_request_items_createdby")

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.store_product.product.name
    

class OutgoingConsumable(Base):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data
    store_product = models.ForeignKey(StoreProduct,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12,decimal_places=3)
    remarks = models.TextField(null=True,blank=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="outgoing_consumables_createdby")

    def __str__(self):
        return self.store_product.product.name
