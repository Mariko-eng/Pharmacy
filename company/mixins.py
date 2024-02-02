from django.db import models
from simple_history.models import HistoricalRecords
from .managers import CompanyDataManager, MyQueryset
from .managers import CompanyStoreQuerySet
from .managers import ProductManager, SaleManager, SaleItemManager

class Base(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords(inherit=True)

    objects = models.Manager()
    objects1 = CompanyDataManager()
    objects2 = MyQueryset().as_manager() 

    product_objects = ProductManager()
    sale_objects = SaleManager()
    sale_item_objects = SaleItemManager()

    company_store_objects = CompanyStoreQuerySet.as_manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save(using=using)
    
    def hard_delete(self, *args, **kwargs):
        # If you need to perform a hard delete, call this method
        super(Base, self).delete(*args, **kwargs)