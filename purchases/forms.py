from django import forms
from .models import PurchaseOrderRequest
from .models import PurchaseOrderRequestItem 
from company.models import Supplier, Store
# from django.forms import inlineformset_factory
from django.forms import BaseFormSet


class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


class PurchaseOrderRequestForm(forms.ModelForm):
    
    supplier_type = forms.ChoiceField(
        choices = PurchaseOrderRequest.SUPPLIER_TYPES,
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
        model = PurchaseOrderRequest
        fields = [
            'order_date',
            'delivery_date',
            'order_notes','payment_terms',]
        exclude = ['company','store','updated_by','updated_at','created_by','created_at']


    def __init__(self, *args, company=None, **kwargs):
        super(PurchaseOrderRequestForm, self).__init__(*args, **kwargs)

        if company:
            self.fields['supplier_entity'].queryset = Supplier.objects.filter(company=company)
            self.fields['supplier_store'].queryset = Store.objects.filter(company=company)

                    # Check if an instance is passed and set the initial value for supplier_entity
        instance = kwargs.get('instance')
        if instance and instance.supplier_entity:
            self.initial['supplier_entity'] = instance.supplier_entity

        if instance and instance.supplier_store:
            self.initial['supplier_store'] = instance.supplier_store


class PurchaseOrderRequestItemForm(forms.ModelForm):
    total_cost = forms.DecimalField(initial=0,max_digits=12, decimal_places=3)
    class Meta:
        model = PurchaseOrderRequestItem
        fields = [
            'store_product','quantity','total_cost',
        ]
        exclude = ['company','store','order_request','updated_by','updated_at','created_by','created_at']