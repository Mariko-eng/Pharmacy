from typing import Any, Mapping
from django import forms
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList
from .models import CompanyApplication
from .models import Company
from .models import Store
from .models import PosCenter
from user.models import User

class CompanyApplicationRegisterForm(forms.ModelForm):    
    class Meta:
        model = CompanyApplication
        fields = ['name', 'phone', 'email', 'location', 'logo',]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CompanyApplication.objects.filter(email = email).exists():
            raise forms.ValidationError("Email already exists!")
        
        if Company.objects.filter(email = email).exists():
            raise forms.ValidationError("Email already exists!")
        
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("Email already exists!")
        
        return email


class CompanyAccountActivationForm(forms.Form):
    company_email = forms.CharField(max_length=30)
    activation_code = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30)
    password1 = forms.CharField(max_length=30)
    password2 = forms.CharField(max_length=30)

    def clean_company_email(self):
        company_email = self.cleaned_data.get('company_email')
        if not CompanyApplication.objects.filter(email = company_email).exists():
            raise forms.ValidationError("Company Email does not exist!")
        return company_email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("User with email already exists!")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Password do not match!")
        return password2
     

# class CompanyAdminRegisterForm(forms.Form):
#     activation_code = forms.CharField(max_length=30)
#     first_name = forms.CharField(max_length=30)
#     last_name = forms.CharField(max_length=30)
#     phone = forms.CharField(max_length=30)
#     email = forms.CharField(max_length=30)
#     password1 = forms.CharField(max_length=30)
#     password2 = forms.CharField(max_length=30)

#     def __init__(self, *args, company=None, **kwargs):
#         super(CompanyAdminRegisterForm, self).__init__(*args, **kwargs)

#         if company:
#             self.fields['activation_code'].initial = company.activation_code
#             self.fields['activation_code'].widget = forms.HiddenInput()

#         if company:
#             self.fields['email'].initial = company.email


#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email = email).exists():
#             raise forms.ValidationError("Email already exists!")
#         return email

#     def clean_passord2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#         if password1 != password2:
#             raise forms.ValidationError("Password do not match!")
#         return password2


# class CompanyRegisterForm(forms.ModelForm):
    
#     class Meta:
#         model = Company
#         fields = ['name', 'phone', 'email', 'location', 'logo',]


class StoreForm(forms.ModelForm):
    store_type = forms.ChoiceField(choices=[('', '---------')] + Store.STORE_TYPES)
    status_type = forms.ChoiceField(choices=[('', '---------')] + Store.STATUS_TYPES)
    location_district = forms.CharField(max_length=30)
    location_village = forms.CharField(max_length=30)
    class Meta:
        model = Store
        fields = ['name','email','phone','location_district','location_village','store_type','status_type',]
 
class PosCenterForm(forms.ModelForm):
    class Meta:
        model = PosCenter
        fields = ['name',]


