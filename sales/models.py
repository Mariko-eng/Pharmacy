from django.db import models
from inventory.models import StoreProduct
from company.models import Company,Store,PosCenter,Customer
from company.mixins import Base

# class PaymentMethod(Base):
#     #Owner
#     company = models.ForeignKey(Company,on_delete=models.CASCADE)
#     # Data    
#     name = models.CharField(max_length=255,unique=True)

class Sale(Base):
    PAYMENT_oPTIONS = [
        ('Cash', 'Cash'),
        ('Airtel MOney', 'Airtel MOney'),
        ('MTN MOney', 'MTN MOney'),
        ('Cheque', 'Cheque')
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('REVOKED', 'Revoked'),]

    #Owner 
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data
    pos_center = models.ForeignKey(PosCenter, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    payment_option = models.CharField(max_length=25, choices=PAYMENT_oPTIONS, default='Casn')
    payment_details = models.CharField(max_length=225, blank=True, null=True)
    sale_date = models.DateField(null=True)
    sale_remarks = models.TextField(null=True,blank=True)
    is_completed = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Completed')
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="sales_createdby")

    class Meta:
        ordering = ("-created_at",)

    @property
    def items_count(self):
        return self.saleitem_set.count()
    
    @property
    def total_cost(self):
        total = 0
        items = self.saleitem_set.all()
        for item in items:
            total = total + item.sub_total
        return total


class SaleItem(Base):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    store_product = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="sale_items_createdby")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units sold"
    
    @property
    def sub_total(self):
        return self.quantity * self.unit_cost