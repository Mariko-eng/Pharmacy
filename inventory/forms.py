from django import forms
from .models import Variant, Category, Units
from .models import StockItem, ReceivedStock, ReceivedStockItem
from .models import StockRequest, StockRequestItem
from company.models import SupplierEntity, Store
from django.forms import BaseFormSet

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ['name']
        
class UnitsForm(forms.ModelForm):
    class Meta:
        model = Units 
        fields = ['name']

class SupplierEntityForm(forms.ModelForm):
    class Meta:
        model = SupplierEntity
        fields = ['name','phone','email','location']

class StockItemForm(forms.ModelForm):
    name = forms.CharField(max_length=30)
    description = forms.CharField(widget=forms.Textarea, required=False) # For type TextField
    item_photo = forms.ImageField(required=False)
    category = forms.ModelChoiceField(
        queryset= None,  # Provide the queryset
        required= True,  # Set to True if you want it to be required
    )
    variant = forms.ModelChoiceField(
        queryset= None,  # Provide the queryset
        required= False,  # Set to True if you want it to be required
    )
    units = forms.ModelChoiceField(
        queryset= None,  # Provide the queryset
        required= True,  # Set to True if you want it to be required
    )
    unit_price = forms.DecimalField(initial=0)
    reorder_min_qty = forms.DecimalField(initial=0)

    class Meta:
        model = StockItem
        fields = [ 
            'name',
            'description',
            'category',
            'variant',
            'units',
            'unit_price',
            'item_photo',
            'reorder_min_qty',
            'is_for_sale',
            'is_consummable',
        ]
        exclude = ['company',
                   'updated_by',
                   'updated_at',
                   'created_by',
                   'created_at',]
        
    def __init__(self, *args, store=None, **kwargs):
        super(StockItemForm, self).__init__(*args, **kwargs)

        if store:
            self.fields['category'].queryset = Category.objects.filter(store=store)
            self.fields['variant'].queryset = Variant.objects.filter(store=store)
            self.fields['units'].queryset = Units.objects.filter(store=store)


class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

class ReceivedStockForm(forms.ModelForm):

    supplier_type = forms.ChoiceField(
        choices = ReceivedStock.SUPPLIER_TYPES,
        widget = forms.RadioSelect(),
    )

    supplier_entity = forms.ModelChoiceField(
        queryset= None,  # Provide the queryset
        required= False,
    )

    supplier_store = forms.ModelChoiceField(
        queryset= None,  # Provide the queryset
        required= False,
    )
    
    class Meta:
        model = ReceivedStock
        fields = [
            'supplier_type',
            'delivered_by_name',
            'delivered_by_phone',
            'received_date',
            'delivery_notes',]
        exclude = ['company','store','updated_by','updated_at','created_by','created_at']


    def __init__(self, *args, company=None, store=None, **kwargs):
        super(ReceivedStockForm, self).__init__(*args, **kwargs)

        if store:
            self.fields['supplier_entity'].queryset = SupplierEntity.objects.filter(store=store)

        if company:
            if store:
                self.fields['supplier_store'].queryset = Store.objects.filter(company=company).exclude(pk=store.id)

        # Check if an instance is passed and set the initial value for supplier_entity
        instance = kwargs.get('instance')
        if instance and instance.supplier_entity:
            self.initial['supplier_entity'] = instance.supplier_entity

        if instance and instance.supplier_store:
            self.initial['supplier_store'] = instance.supplier_store


class ReceivedStockItemForm(forms.ModelForm):
    class Meta:
        model = ReceivedStockItem
        fields = [
            'stock_item','batch_no','quantity',
            'total_cost','manufactured_date','expiry_date',
        ]
        exclude = ['company','store','received_stock','updated_by','updated_at','created_by','created_at']


    def __init__(self, *args, store=None, **kwargs):
        super(ReceivedStockItemForm, self).__init__(*args, **kwargs)

        if store:
            self.fields['stock_item'].queryset = StockItem.objects.filter(store = store)



# ReceivedStockItemFormSet = inlineformset_factory(
#     ReceivedStock, ReceivedStockItem, form=ReceivedStockItemForm,
#     extra=1, can_delete=True, can_delete_extra=True
# )


class StockRequestForm(forms.ModelForm):
    
    class Meta:
        model = StockRequest
        fields = [ 'request_date', 'delivery_date', 'request_notes',]
        exclude = ['company','store', 'updated_by', 'updated_at','created_by','created_at']

class StockRequestItemForm(forms.ModelForm):

    quantity = forms.DecimalField()
    class Meta:
        model = StockRequestItem
        fields = [
            'stock_item','quantity','reason',
        ]
        exclude = ['company','store','stock_request','available_quantity',
                   'updated_by','updated_at','created_by','created_at']