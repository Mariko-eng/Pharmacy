from django import forms
from .models import Company, User

class SuperUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=30)
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'phone_number']

class CompanyAdminUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=30)
    company = forms.ModelChoiceField(
        queryset= Company.objects.all(),  # Provide the queryset
        required= True,  # Set to True if you want it to be required
    )
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'phone_number','company']

class CompanyForm(forms.ModelForm):
    
    class Meta:
        model = Company
        fields = ['name']

class NameForm(forms.Form):
    name = forms.CharField(label="Your name", max_length=100,)
    state = forms.CharField(label="Your state", max_length=100,)
    terms = forms.CharField(label="Your terms", max_length=100,)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name.lower() == 'mark':
            raise forms.ValidationError("Bad name: 'Mark' is not allowed.")
        return name