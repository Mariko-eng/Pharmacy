from django.db import models
from company.models import Company
from company.models import Store
from company.models import PosCenter
from company.models import Provider
from company.mixins import CommonFieldsMixin

class ProductCategory(CommonFieldsMixin):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    # Data    
    name = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.name
    
class ProductVariant(CommonFieldsMixin):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    # Data    
    name = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.name

class ProductUnits(CommonFieldsMixin): # Units Of Measure
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    # Data    
    name = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.name

class Product(CommonFieldsMixin):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data    
    unique_no = models.CharField(max_length=255,unique=True)
    name = models.CharField(max_length=255,unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(ProductCategory,on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(ProductVariant,on_delete=models.SET_NULL, null=True)
    units = models.ForeignKey(ProductUnits,on_delete=models.SET_NULL, null=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=3)
    available_qty = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    reorder_min_qty = models.DecimalField(max_digits=12, decimal_places=3,default=0)
    item_photo = models.ImageField(upload_to="products", null=True)
    is_consummable = models.BooleanField(default=False)
    is_for_sale = models.BooleanField(default=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="products_createdby")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ReceivedStock(CommonFieldsMixin):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data
    provider = models.ForeignKey(Provider,on_delete=models.SET_NULL,null=True)
    delivered_by_name = models.CharField(max_length=255,unique=True)
    delivered_by_phone = models.CharField(max_length=255,unique=True)
    received_date = models.DateField(null=True)
    delivery_notes = models.TextField(null=True,blank=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="received_stocks_createdby")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

class ReceivedStockItem(CommonFieldsMixin):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data
    received_stock = models.ForeignKey(ReceivedStock,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    batch_no = models.CharField(max_length=255,unique=True)
    qty_received = models.DecimalField(max_digits=12, decimal_places=3)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=3)
    manufactured_date = models.DateField(null=True)
    expiry_date = models.DateField(null=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="received_stock_items_createdby")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

class StockRequest(CommonFieldsMixin):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DECLINED', 'Declined'),
    )

    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data
    request_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    request_notes = models.TextField(null=True,blank=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="stock_requests_createdby")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.request_date} - {self.status}"

class StockRequestItem(CommonFieldsMixin):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data
    stock_request = models.ForeignKey(StockRequest, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="stock_request_items_createdby")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

class OutgoingConsumable(CommonFieldsMixin):
    #Owner
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12,decimal_places=3)
    remarks = models.TextField(null=True,blank=True)
    updated_by_id = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="outgoing_consumables_createdby")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"



    


