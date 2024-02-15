from uuid import uuid4
from django.db import models
from django.utils import timezone
from company.models import Company, SupplierEntity
from company.models import Store
from company.mixins import Base
from inventory.models import StockItem
from utils.permissions.purchases import *

class PurchaseOrder(Base):
    SUPPLIER_TYPES = [('SUPPLIER', 'SUPPLIER'),('STORE', 'STORE'),]

    PAYMENT_PERIODS = [
        ('Instant', 'Instant'),
        ('After 7 days', 'After 7 days'),
        ('After 14 days', 'After 14 days'),
        ('After 30 days', 'After 30 days'),
        ('After 60 days', 'After 60 days'),]
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DECLINED', 'Declined'),
    )

    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data
    supplier_type = models.CharField(max_length=10,choices=SUPPLIER_TYPES,default="SUPPLIER")
    supplier_entity = models.ForeignKey(SupplierEntity,on_delete=models.SET_NULL,null=True)
    supplier_store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True, related_name="purchase_order_requests")
    order_date = models.DateField(default=timezone.now)
    delivery_date = models.DateField(null=True) # Expected  Delivery Date
    order_notes = models.TextField(null=True,blank=True)
    payment_period = models.CharField(max_length=25, choices=PAYMENT_PERIODS, default='Instant')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="purchase_orders_createdby")

    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = purchase_order_permissions
        ordering = ("-created_at",)
    
    @property
    def order_unique_id(self):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.save()
            
        return self.uniqueId

    @property
    def items_count(self):
        return self.purchaseorderitem_set.count()
    
    @property
    def total_cost(self):
        total = 0
        items = self.purchaseorderitem_set.all()
        for item in items:
            total = total + item.total_cost
        return total
    
    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        super(PurchaseOrder, self).save(*args, **kwargs)

class PurchaseOrderItem(Base):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data
    order_request = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    stock_item = models.ForeignKey(StockItem,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    total_cost = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="purchase_order_items_createdby")

    class Meta:
        default_permissions = [] # Defaults to ('add', 'change', 'delete', 'view'), setting this to an empty list if your app doesn’t require any of the default permissions.
        permissions = purchase_order_item_permissions
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"