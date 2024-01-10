from django import forms
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
    email = forms.CharField(max_length=30)
    activation_code = forms.CharField(max_length=30)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not CompanyApplication.objects.filter(email = email).exists():
            raise forms.ValidationError("Company Email does not exists!")
        return email
    
class CompanyAdminRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30)
    email = forms.CharField(max_length=30)
    password1 = forms.CharField(max_length=30)
    password2 = forms.CharField(max_length=30)


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("Email already exists!")
        return email

    def clean_passord2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Password do not match!")
        return password2


# class CompanyRegisterForm(forms.ModelForm):
    
#     class Meta:
#         model = Company
#         fields = ['name', 'phone', 'email', 'location', 'logo',]


class StoreForm(forms.ModelForm):
    store_type = forms.ChoiceField(choices=[('', '---------')] + Store.STORE_TYPES)
    status = forms.ChoiceField(choices=[('', '---------')] + Store.STATUS_TYPES)
    location_district = forms.CharField(max_length=30)
    location_village = forms.CharField(max_length=30)
    class Meta:
        model = Store
        fields = ['name','email','phone','location_district','location_village','store_type','status',]

class PosCenterForm(forms.ModelForm):
    class Meta:
        model = PosCenter
        fields = ['name',]


