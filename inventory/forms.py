from django import forms
from .models import ProductType, ProductCategory, ProductUnits
from .models import Product, ReceivedStock, ReceivedStockItem
from django.forms import inlineformset_factory

class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = [
            'name'
        ]

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = [
            'name'
        ]

class ProductUnitsForm(forms.ModelForm):
    class Meta:
        model = ProductUnits
        fields = [
            'name'
        ]


class ProductForm(forms.ModelForm):
    type = forms.ModelChoiceField(
        queryset= ProductType.objects.all(),  # Provide the queryset
        required= True,  # Set to True if you want it to be required
    )
    category = forms.ModelChoiceField(
        queryset= ProductCategory.objects.all(),  # Provide the queryset
        required= True,  # Set to True if you want it to be required
    )
    name = forms.CharField(max_length=30)
    description = forms.CharField(widget=forms.Textarea) # For type TextField
    units = forms.ModelChoiceField(
        queryset= ProductUnits.objects.all(),  # Provide the queryset
        required= True,  # Set to True if you want it to be required
    )
    item_photo = forms.ImageField(required=False)
    reorder_min_qty = forms.DecimalField(initial=0)

    class Meta:
        model = Product
        fields = [
            'type','category',
            'name','description',
            'units','unit_price',
            'item_photo','reorder_min_qty',
            'is_for_sale','is_consummable',
        ]
        exclude = ['company','unique_no','updated_by_id','updated_at','created_by','created_at']

class ReceivedStockForm(forms.ModelForm):
    
    class Meta:
        model = ReceivedStock
        fields = [
            'provider','delivered_by_name','delivered_by_phone',
            'received_date','delivery_notes',
        ]
        exclude = ['company','branch','updated_by_id','updated_at','created_by','created_at']


class ReceivedStockItemForm(forms.ModelForm):
    
    class Meta:
        model = ReceivedStockItem
        fields = [
            'product','batch_no','qty_received',
            'unit_cost','manufactured_date','expiry_date',
        ]
        exclude = ['company','branch','received_stock','updated_by_id','updated_at','created_by','created_at']



ReceivedStockItemFormSet = inlineformset_factory(
    ReceivedStock, ReceivedStockItem, form=ReceivedStockItemForm,
    extra=1, can_delete=True, can_delete_extra=True
)

# function:: inlineformset_factory(parent_model, model, form=ModelForm, formset=BaseInlineFormSet, fk_name=None, fields=None, exclude=None, extra=3, can_order=False, can_delete=True, max_num=None, formfield_callback=None, widgets=None, validate_max=False, localized_fields=None, labels=None, help_texts=None, error_messages=None, min_num=None, validate_min=False, field_classes=None, absolute_max=None, can_delete_extra=True, renderer=None, edit_only=False)
