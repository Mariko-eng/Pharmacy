from django.db import models
from user.models import Company
from user.models import CompanyBranch
from user.models import Provider
from inventory.models import Product
from user.mixins import CommonFieldsMixin

class PurchaseOrderRequest(CommonFieldsMixin):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DECLINED', 'Declined'),
    )

    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    branch = models.ForeignKey(CompanyBranch,on_delete=models.SET_NULL,null=True)
    # Data
    provider = models.ForeignKey(Provider,on_delete=models.SET_NULL,null=True)
    order_date = models.DateField(null=True)
    expected_delivery_date = models.DateField(null=True)
    attached_file = models.FileField(upload_to="files")
    order_notes = models.TextField(null=True,blank=True)
    payment_terms = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="purchase_orders_createdby")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

class PurchaseOrderRequestItem(CommonFieldsMixin):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    branch = models.ForeignKey(CompanyBranch,on_delete=models.SET_NULL,null=True)
    # Data
    stock_request = models.ForeignKey(PurchaseOrderRequest, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="purchase_order_items_createdby")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"