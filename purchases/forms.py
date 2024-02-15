from django import forms
from .models import PurchaseOrder
from .models import PurchaseOrderItem 
from company.models import SupplierEntity, Store
from django.forms import BaseFormSet


class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


class PurchaseOrderForm(forms.ModelForm):
    
    supplier_type = forms.ChoiceField(
        choices = PurchaseOrder.SUPPLIER_TYPES,
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
        model = PurchaseOrder
        fields = [
            'supplier_type',
            'supplier_entity',
            'supplier_store',
            'order_date',
            'delivery_date',
            'order_notes',] 
        exclude = ['company','store','payment_period','updated_by','updated_at','created_by','created_at']

    def __init__(self, *args, company=None, store=None, **kwargs):
        super(PurchaseOrderForm, self).__init__(*args, **kwargs)

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


class PurchaseOrderItemForm(forms.ModelForm):
    total_cost = forms.DecimalField(max_digits=12, decimal_places=3)
    class Meta:
        model = PurchaseOrderItem
        fields = [
            'stock_item','quantity','total_cost',
        ]
        exclude = ['company','store','order_request','updated_by','updated_at','created_by','created_at']
