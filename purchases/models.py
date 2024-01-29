from django.db import models
from django.utils import timezone
from company.models import Company, Supplier
from company.models import Store
from company.mixins import Base
from inventory.models import StoreProduct

class PurchaseOrderRequest(Base):
    SUPPLIER_TYPES = [('SUPPLIER', 'SUPPLIER'),('STORE', 'STORE'),]
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
    supplier_entity = models.ForeignKey(Supplier,on_delete=models.SET_NULL,null=True)
    supplier_store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True, related_name="purchase_order_requests")
    order_date = models.DateField(default=timezone.now)
    delivery_date = models.DateField(null=True) # Expected  Delivery Date
    order_notes = models.TextField(null=True,blank=True)
    payment_terms = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="purchase_orders_createdby")

class PurchaseOrderRequestItem(Base):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data
    order_request = models.ForeignKey(PurchaseOrderRequest, on_delete=models.CASCADE)
    store_product = models.ForeignKey(StoreProduct,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    total_cost = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="purchase_order_items_createdby")

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"