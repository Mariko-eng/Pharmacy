from django import forms
from .models import Company

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