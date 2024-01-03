# from django.db import models
# from simple_history.models import HistoricalRecords
# from .managers import CompanyDataManager, MyQueryset

# class CommonFieldsMixin(models.Model):
#     is_active = models.BooleanField(default=True)
#     is_deleted = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     history = HistoricalRecords(inherit=True)

#     objects = models.Manager()
#     objects1 = CompanyDataManager()
#     objects2 = MyQueryset().as_manager()
    
#     class Meta:
#         abstract = True

#     def delete(self, using=None, keep_parents=False):
#         self.is_deleted = True
#         self.save(using=using)
    
#     def hard_delete(self, *args, **kwargs):
#         # If you need to perform a hard delete, call this method
#         super(CommonFieldsMixin, self).delete(*args, **kwargs)