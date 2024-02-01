import os
from django.db import models
from django.db.models import Sum
from django.core.files import File
from uuid import uuid4
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.template.defaultfilters import slugify
from company.mixins import Base
from company.models import Company, Store
from company.models import PosCenter, Customer
from inventory.models import StoreProduct
from .tasks import generatePDf

class Sale(Base):
    PAYMENT_oPTIONS = [
        ('Cash', 'Cash'),
        ('Airtel MOney', 'Airtel MOney'),
        ('MTN MOney', 'MTN MOney'),
        ('Cheque', 'Cheque'),]
    
    PAYMENT_PERIODS = [
        ('Instant', 'Instant'),
        ('After 7 days', 'After 7 days'),
        ('After 14 days', 'After 14 days'),
        ('After 30 days', 'After 30 days'),
        ('After 60 days', 'After 60 days'),]

    PAYMENT_STATUS = [ 
        ('PAID', 'PAID'),
        ('CURRENT', 'CURRENT'),
        ('OVERDUE', 'OVERDUE'),]

    SALE_STATUS = [
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),]

    #Owner 
    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    # Data
    pos_center = models.ForeignKey(PosCenter, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    payment_option = models.CharField(max_length=25, choices=PAYMENT_oPTIONS, default='Cash')
    payment_period = models.CharField(max_length=25, choices=PAYMENT_PERIODS, default='Instant')
    payment_status = models.CharField(max_length=25, choices=PAYMENT_STATUS, default='PAID')
    status = models.CharField(max_length=25, choices = SALE_STATUS, default='Completed')
    remarks = models.TextField(null=True,blank=True)
    invoice_file = models.FileField(upload_to="invoices", null=True)

    #Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="sales_createdby")

    class Meta:
        ordering = ("-created_at",)
    
    @property
    def sale_unique_id(self):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.save()
            
        return self.uniqueId

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
    
    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        super(Sale, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        # Delete the file from the storage when the AccountImage instance is deleted
        if self.invoice_file:
            # Get the file's path
            file_path = self.invoice_file.path

            # Check if the file exists and delete it
            if os.path.exists(file_path):
                os.remove(file_path)

        super(Sale, self).delete(*args, **kwargs)


    def generate_invoice(self, context = {}):
        if self.uniqueId:
            filename = f"INV-{self.uniqueId}-data.pdf"
        else:
            self.uniqueId = f"INV-{self.id}"
            self.save()
            filename = f"INV-{self.uniqueId}-data.pdf"

        sale_items = self.saleitem_set.all()

        context['sale'] = self
        context['sale_items'] = sale_items
        context['items_count'] = self.items_count
        context['total_cost'] = self.total_cost

        
        pdf_file_path = generatePDf(context = context)

        with open(pdf_file_path, 'rb') as pdf_file:
            django_file = File(file = pdf_file, name= filename)

            # Delete the old file associated with the model field, if any
            if self.invoice_file:
                self.invoice_file.delete(save=False)

            # Assign the new file to the model field
            self.invoice_file = django_file
            self.save()

            # Remove the temporary PDF file
            os.remove(pdf_file_path)
            return self

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
    is_paid = models.BooleanField(default=False)  # New field to track payment status
    updated_by = models.CharField(max_length=225,null=True,blank=True)
    created_by = models.ForeignKey("user.User",null=True,on_delete=models.SET_NULL,related_name="sale_items_createdby")

    def __str__(self):
        return f"{self.store_product.product.name} - {self.quantity} units sold"
    
    @property
    def sub_total(self):
        return self.quantity * self.unit_cost
    

    @classmethod
    def get_sales_count(cls, start_date, end_date, store=None, company=None, pos=None):
        # Ensure that start_date and end_date are datetime objects
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        # Make them timezone-aware
        start_date_aware = timezone.make_aware(start_datetime, timezone.get_current_timezone())
        end_date_aware = timezone.make_aware(end_datetime, timezone.get_current_timezone())

        total = 0

        if pos is not None:
            result = cls.sale_objects.for_pos(pos).filter(created_at__range=[start_date_aware, end_date_aware]).count()
            if result is not None:
                total = result
            return total

        if store is not None:
            result = cls.sale_objects.for_store(store).filter(created_at__range=[start_date_aware, end_date_aware]).count()
            if result is not None:
                total = result
            return total
        
        if company is not None:
            result = cls.sale_objects.for_company(company).filter(created_at__range=[start_date_aware, end_date_aware]).count()
            if result is not None:
                total = result
            return total
        
        result = cls.sale_objects.filter(created_at__range=[start_date_aware, end_date_aware]).count()
        if result is not None:
            total = result

        return total


    @classmethod
    def get_revenue(cls, start_date, end_date, store=None, company=None, pos=None):
        # Ensure that start_date and end_date are datetime objects
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        # Make them timezone-aware
        start_date_aware = timezone.make_aware(start_datetime, timezone.get_current_timezone())
        end_date_aware = timezone.make_aware(end_datetime, timezone.get_current_timezone())
            
        total = 0

        if pos is not None:
            result = cls.sale_objects.for_pos(pos).filter(created_at__range=[start_date_aware, end_date_aware]).aggregate(Sum('total_cost'))['total_cost__sum']
            if result is not None:
                total = result
            return total

        if store is not None:
            result = cls.sale_objects.for_store(store).filter(created_at__range=[start_date_aware, end_date_aware]).aggregate(Sum('total_cost'))['total_cost__sum']
            if result is not None:
                total = result
            return total
        
        if company is not None:
            result = cls.sale_objects.for_company(company).filter(created_at__range=[start_date_aware, end_date_aware]).aggregate(Sum('total_cost'))['total_cost__sum']
            if result is not None:
                total = result
            return total
        
        result = cls.sale_objects.filter(created_at__range=[start_date_aware, end_date_aware]).aggregate(Sum('total_cost'))['total_cost__sum']
        if result is not None:
            total = result

        return total
    
    @classmethod
    def get_recent_sales(cls, store=None, company=None, pos=None):
        queryset = cls.sale_objects.order_by('-created_at')

        if pos is not None:
            queryset = queryset.for_pos(pos)[:5]
            return queryset

        if store is not None:
            queryset = queryset.for_store(store)[:5]
            return queryset

        if company is not None:
            queryset = queryset.for_company(store)[:5]
            return queryset
        
        return queryset[:5]
    
    @classmethod
    def get_top_sales(cls, start_date, end_date, store=None, company=None, pos=None):
        # Ensure that start_date and end_date are datetime objects
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        # Make them timezone-aware
        start_date_aware = timezone.make_aware(start_datetime, timezone.get_current_timezone())
        end_date_aware = timezone.make_aware(end_datetime, timezone.get_current_timezone())

        queryset = cls.sale_objects.filter(created_at__range=[start_date_aware, end_date_aware])
        queryset = queryset.order_by('-total_cost')

        if pos is not None:
            queryset = queryset.for_pos(pos)[:5]
            return queryset

        if store is not None:
            queryset = queryset.for_store(store)[:5]
            return queryset

        if company is not None:
            queryset = queryset.for_company(store)[:5]
            return queryset
        
        return queryset[:5]


    @classmethod
    def get_sales_and_revenue(cls, store=None, company=None, pos=None):
        today = datetime.now()
        today_sales = cls.get_sales_count(today, today, store= store, company=company, pos=pos)
        today_revenue = cls.get_revenue(today, today, store= store, company=company, pos=pos)

        first_day_of_this_month = datetime.now().replace(day=1).date()
        last_day_of_this_month = (datetime.now() + timedelta(days=32)).replace(day=1).date() - timedelta(days=1)
        this_month_sales = cls.get_sales_count(first_day_of_this_month, last_day_of_this_month, store= store, company=company, pos=pos)
        this_month_revenue= cls.get_revenue(first_day_of_this_month, last_day_of_this_month,store= store, company=company, pos=pos)

        first_day_of_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1).date()
        last_day_of_last_month = today.replace(day=1).date() - timedelta(days=1)
        last_month_sales = cls.get_sales_count(first_day_of_last_month, last_day_of_last_month, store= store, company=company, pos=pos)
        last_month_revenue = cls.get_revenue(first_day_of_last_month, last_day_of_last_month, store= store, company=company, pos=pos)
    
        first_day_of_year = datetime.now().replace(month=1, day=1).date()
        last_day_of_year = datetime.now().date()
        this_year_sales = cls.get_sales_count(first_day_of_year, last_day_of_year, store= store, company=company, pos=pos)
        this_year_revenue = cls.get_revenue(first_day_of_year, last_day_of_year, store= store, company=company, pos=pos)

        return {
            "today_sales" : today_sales,
            "today_revenue" : today_revenue,
            "this_month_sales" : this_month_sales,
            "this_month_revenue" : this_month_revenue,
            "last_month_sales" : last_month_sales,
            "last_month_revenue": last_month_revenue,
            "this_year_sales" : this_year_sales,
            "this_year_revenue": this_year_revenue
        }


    @classmethod
    def get_sales_data(cls, store=None, company=None, pos=None):
        recent_sales = cls.get_recent_sales(store= store, company=company, pos=pos)

        today_top_sales = cls.get_top_sales(datetime.now(), datetime.now(), store= store, company=company, pos=pos)

        start_of_this_week = datetime.now() - timedelta(days=datetime.now().weekday())
        end_of_this_week = start_of_this_week + timedelta(days=6)
        this_week_top_sales= cls.get_top_sales(start_of_this_week, end_of_this_week, store=store, company=company, pos=pos)

        start_of_last_week = datetime.now() - timedelta(days=(datetime.now().weekday() + 7))
        end_of_last_week = start_of_last_week + timedelta(days=6)
        last_week_top_sales = cls.get_top_sales(start_of_this_week, end_of_last_week, store=store, company=company, pos=pos)

        first_day_of_this_month = datetime.now().replace(day=1).date()
        last_day_of_this_month = (datetime.now() + timedelta(days=32)).replace(day=1).date() - timedelta(days=1)
        this_month_top_sales = cls.get_top_sales(first_day_of_this_month, last_day_of_this_month, store=store, company=company, pos=pos)

        first_day_of_last_month = (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1).date()
        last_day_of_last_month = datetime.now().replace(day=1).date() - timedelta(days=1)
        last_month_top_sales = cls.get_top_sales(first_day_of_last_month, last_day_of_last_month, store=store, company=company, pos=pos)

        first_day_of_year = datetime.now().replace(month=1, day=1).date()
        last_day_of_year = datetime.now().date()
        this_year_top_sales = cls.get_top_sales(first_day_of_year, last_day_of_year, store=store, company=company, pos=pos)

        return {
            "recent_sales" : recent_sales,
            "today_top_sales" : today_top_sales,
            "this_week_top_sales" : this_week_top_sales,
            "last_week_top_sales" : last_week_top_sales,
            "this_month_top_sales" : this_month_top_sales,
            "last_month_top_sales" : last_month_top_sales,
            "this_year_top_sales": this_year_top_sales
        }


