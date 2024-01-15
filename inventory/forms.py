from django import forms
from .models import ProductVariant, ProductCategory, ProductUnits
from .models import Product, StoreProduct, ReceivedStock, ReceivedStockItem
from company.models import SupplierEntity, Provider, Store
from django.forms import inlineformset_factory
from django.forms import BaseFormSet

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name']

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['name']
        
class ProductUnitsForm(forms.ModelForm):
    class Meta:
        model = ProductUnits
        fields = ['name']

class SupplierEntityForm(forms.ModelForm):
    class Meta:
        model = SupplierEntity
        fields = ['name','phone','email','location']

# class ProductForm(forms.ModelForm):
#     name = forms.CharField(max_length=30)
#     description = forms.CharField(widget=forms.Textarea) # For type TextField
#     item_photo = forms.ImageField(required=False)
#     category = forms.ModelChoiceField(
#         queryset= ProductCategory.objects.all(),  # Provide the queryset
#         required= True,  # Set to True if you want it to be required
#     )
#     variant = forms.ModelChoiceField(
#         queryset= ProductVariant.objects.all(),  # Provide the queryset
#         required= True,  # Set to True if you want it to be required
#     )
#     units = forms.ModelChoiceField(
#         queryset= ProductUnits.objects.all(),  # Provide the queryset
#         required= True,  # Set to True if you want it to be required
#     )
#     unit_price = forms.DecimalField(initial=0)
#     reorder_min_qty = forms.DecimalField(initial=0)

#     class Meta:
#         model = Product
#         fields = [
#             'name',
#             'description',
#             'variant',
#             'category',
#             'units',
#         ]
#         exclude = ['company','unique_no','updated_by','updated_at','created_by','created_at']


class StoreProductForm(forms.ModelForm):
    name = forms.CharField(max_length=30)
    description = forms.CharField(widget=forms.Textarea) # For type TextField
    item_photo = forms.ImageField(required=False)
    category = forms.ModelChoiceField(
        queryset= ProductCategory.objects.all(),  # Provide the queryset
        required= True,  # Set to True if you want it to be required
    )
    variant = forms.ModelChoiceField(
        queryset= ProductVariant.objects.all(),  # Provide the queryset
        required= True,  # Set to True if you want it to be required
    )
    units = forms.ModelChoiceField(
        queryset= ProductUnits.objects.all(),  # Provide the queryset
        required= True,  # Set to True if you want it to be required
    )
    unit_price = forms.DecimalField(initial=0)
    reorder_min_qty = forms.DecimalField(initial=0)

    class Meta:
        model = StoreProduct
        fields = [
            'name',
            'description',
            'variant',
            'category',
            'units',
            'unit_price',
            'item_photo',
            'reorder_min_qty',
            'is_for_sale',
            'is_consummable',
        ]
        exclude = ['company','updated_by','updated_at','created_by','created_at']


class ReceivedStockForm(forms.ModelForm):

    provider_type = forms.ChoiceField(
        choices = Provider.PROVIDER_TYPES,
        widget = forms.RadioSelect(),
        initial = ""
    )

    supplier = forms.ModelChoiceField(
        queryset= None,  # Provide the queryset
        required= False,
    )

    store = forms.ModelChoiceField(
        queryset= None,  # Provide the queryset
        required= False,
    )
    
    class Meta:
        model = ReceivedStock
        fields = [
            # 'provider',
            'delivered_by_name','delivered_by_phone',
            'received_date','delivery_notes',]
        exclude = ['company','store','updated_by_id','updated_at','created_by','created_at']


    def __init__(self, *args, company=None, **kwargs):
        super(ReceivedStockForm, self).__init__(*args, **kwargs)

        if company:
            self.fields['supplier'].queryset = SupplierEntity.objects.filter(company=company)
            self.fields['store'].queryset = Store.objects.filter(company=company)

class ReceivedStockItemForm(forms.ModelForm):
    class Meta:
        model = ReceivedStockItem
        fields = [
            'store_product','batch_no','qty_received',
            'total_cost','manufactured_date','expiry_date',
        ]
        exclude = ['company','store','received_stock','updated_by_id','updated_at','created_by','created_at']



ReceivedStockItemFormSet = inlineformset_factory(
    ReceivedStock, ReceivedStockItem, form=ReceivedStockItemForm,
    extra=1, can_delete=True, can_delete_extra=True
)

# function:: inlineformset_factory(parent_model, model, form=ModelForm, formset=BaseInlineFormSet, fk_name=None, fields=None, exclude=None, extra=3, can_order=False, can_delete=True, max_num=None, formfield_callback=None, widgets=None, validate_max=False, localized_fields=None, labels=None, help_texts=None, error_messages=None, min_num=None, validate_min=False, field_classes=None, absolute_max=None, can_delete_extra=True, renderer=None, edit_only=False)



class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False