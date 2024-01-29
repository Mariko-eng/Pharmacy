from django import forms
from .models import Sale
from .models import SaleItem 
from company.models import  PosCenter
from user.models import AccessGroups
from django.forms import BaseFormSet


class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


class SaleForm(forms.ModelForm):
    customer_name = forms.CharField(max_length=30,required=False)
    customer_email = forms.CharField(max_length=30,required=False)
    customer_phone = forms.CharField(max_length=30,required=False)
    customer_address = forms.CharField(max_length=30,required=False)
    
    pos_center = forms.ModelChoiceField(
        queryset= None,  # Provide the queryset
        required= True,
    )
  
    class Meta:
        model = Sale
        fields = [
            'pos_center',
            'payment_option',
            'payment_details',
            'sale_remarks',
            ]
        exclude = ['company','store','updated_by','updated_at','created_by','created_at']


    def __init__(self, *args, user=None, store=None, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)

        if user:
            if user.account_type == AccessGroups.POS_ATTENDANT:
                self.fields['pos_center'].queryset = user.userprofile.pos_center
                self.fields['pos_center'].initial = user.userprofile.pos_center
            else:
                if store:
                    self.fields['pos_center'].queryset = PosCenter.objects.filter(store=store)


class SaleItemForm(forms.ModelForm):
    quantity = forms.DecimalField(initial=0)
    class Meta:
        model = SaleItem
        fields = [
            'store_product','quantity'
        ]
        exclude = ['company','store','sale','unit_cost','total_cost','updated_by','updated_at','created_by','created_at']


class PosSaleForm(forms.ModelForm):
    customer_name = forms.CharField(max_length=30,required=False)
    customer_email = forms.CharField(max_length=30,required=False)
    customer_phone = forms.CharField(max_length=30,required=False)
    customer_address = forms.CharField(max_length=30,required=False)
  
    class Meta:
        model = Sale
        fields = [
            'payment_option',
            'payment_details',
            'sale_remarks',
            ]
        exclude = [
            'company','store','pos_center',
            'updated_by','updated_at',
            'created_by','created_at']