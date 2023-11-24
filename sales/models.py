from django.db import models
from inventory.models import Product
from user.models import Company,CompanyBranch,Pos,Customer

class PaymentMethod(models.Model):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    # Data    
    name = models.CharField(max_length=255,unique=True)


class Sale(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('REVOKED', 'Revoked'),
    )

    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    branch = models.ForeignKey(CompanyBranch,on_delete=models.SET_NULL,null=True)
    # Data
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    payment_method = models.ForeignKey(PaymentMethod,on_delete=models.SET_NULL,null=True)
    sale_date = models.DateField(null=True)
    sale_notes = models.TextField(null=True,blank=True)
    is_completed = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Completed')
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="sales_createdby")
    created_at = models.DateTimeField(auto_now_add=True)


class SaleItem(models.Model):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    branch = models.ForeignKey(CompanyBranch,on_delete=models.SET_NULL,null=True)
    # Data
    pos = models.ForeignKey(Pos, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    price_sold = models.DecimalField(max_digits=10, decimal_places=2)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="sale_items_createdby")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity_sold} units sold"