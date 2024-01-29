from django import forms
from django.contrib.auth.models import Permission
from .models import User
from .models import Company
from .models import Store
from .models import PosCenter
from .permissions import DefaultRoles
from .permissions import AccessGroups
# from .models import AppRoles
# from .models import CompanyRoles
# from .models import BranchRoles


class AppUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30)
    is_superuser = forms.BooleanField(initial=False, required=False)
    is_staff = forms.BooleanField(initial = True)
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'phone', 'is_superuser', 'is_staff',]

class CompanyUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30)
    account_type = forms.ChoiceField(
        choices=[('', '---------')] + AccessGroups.choices,
        widget=forms.RadioSelect()
    )
    roles = forms.MultipleChoiceField(
        choices=[('', '---------')] + DefaultRoles.choices,
        widget= forms.CheckboxSelectMultiple())
    access_to_all_branches = forms.BooleanField(
        initial=False, 
        required=False,
        widget=forms.CheckboxInput()
        )
    stores = forms.ModelMultipleChoiceField(
        queryset= None,  # Provide the queryset
        required= False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),  # Add Bootstrap classes
    )

    def __init__(self, *args, company=None, **kwargs):
        super(CompanyUserForm, self).__init__(*args, **kwargs)
        # Get the default choices from the DefaultRoles enum
        access_group_choices = [(access_group.value, access_group.label) for access_group in AccessGroups]
        # Exclude APP_ADMIN from the choices
        access_group_choices = [choice for choice in access_group_choices if choice[0] != AccessGroups.APP_ADMIN]
        # Set the updated choices for the 'role' field
        self.fields['account_type'].choices = access_group_choices

        # Get the default choices from the DefaultRoles enum
        role_choices = [(role.value, role.label) for role in DefaultRoles]
        # Exclude APP_ADMIN from the choices
        role_choices = [choice for choice in role_choices if choice[0] != DefaultRoles.APP_ADMIN]
        # Exclude ACCOUNT_HOLDER from the choices
        role_choices = [choice for choice in role_choices if choice[0] != DefaultRoles.ACCOUNT_HOLDER]
        # Exclude COMPANY_ADMIN from the choices
        role_choices = [choice for choice in role_choices if choice[0] != DefaultRoles.COMPANY_ADMIN]
        # Set the updated choices for the 'role' field
        self.fields['roles'].choices = role_choices

        if company:
            self.fields['stores'].queryset = Store.objects.filter(company=company)

    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'phone',]

    def clean(self):
        cleaned_data = super().clean()
        roles = cleaned_data.get('roles')

        if not len(roles):
            raise forms.ValidationError("Select at least one role for the user")

        return cleaned_data
    
    def clean_branches(self):
        cleaned_data = super().clean()
        roles = cleaned_data.get('roles')
        branches = cleaned_data.get('branches')

        if not len(roles):
            raise forms.ValidationError("Select at least one role for the user")

        if 'Company Admin' not in roles and not len(branches):
            raise forms.ValidationError("Select at least one branch if the role is not 'Company Admin'.")

        return branches

class CompanyRoleFrom(forms.Form):
    name = forms.CharField(max_length=30)        


class CompanyAdminUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'phone',]


class StoreAdminUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30)
    roles = forms.MultipleChoiceField(
        choices=[('', '---------')] + DefaultRoles.choices,
        widget= forms.CheckboxSelectMultiple())
    store = forms.ModelChoiceField(
        queryset= None,
        required= True,
        widget=forms.RadioSelect()
    )

    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'phone',]

    def __init__(self, *args, company=None, store=None, **kwargs):
        super(StoreAdminUserForm, self).__init__(*args, **kwargs)

        # Get the default choices from the DefaultRoles enum
        role_choices = [(role.value, role.label) for role in DefaultRoles]
        # Exclude APP_ADMIN from the choices
        role_choices = [choice for choice in role_choices if choice[0] != DefaultRoles.APP_ADMIN]
        # Exclude ACCOUNT_HOLDER from the choices
        role_choices = [choice for choice in role_choices if choice[0] != DefaultRoles.ACCOUNT_HOLDER]
        # Exclude COMPANY_ADMIN from the choices
        role_choices = [choice for choice in role_choices if choice[0] != DefaultRoles.COMPANY_ADMIN]
        # Exclude CASHIER from the choices
        role_choices = [choice for choice in role_choices if choice[0] != DefaultRoles.CASHIER]
        # Set the updated choices for the 'role' field
        self.fields['roles'].choices = role_choices

        if store:
            self.fields['store'].queryset = Store.objects.filter(id=store.id)
            self.fields['store'].initial = store
        elif company:
            self.fields['store'].queryset = Store.objects.filter(company=company)


class POSAttendantUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30)
    store = forms.ModelChoiceField(
        queryset= None,
        required= True,
        widget=forms.RadioSelect()
    )
    pos_center = forms.ModelChoiceField(
        queryset= None,
        required= True,
        widget=forms.RadioSelect()
    )

    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'phone',]

    def __init__(self, *args, company = None, store = None, **kwargs):
        super(POSAttendantUserForm, self).__init__(*args, **kwargs)

        if store:
            self.fields['store'].queryset = Store.objects.filter(id=store.id)
            self.fields['store'].initial = store
            self.fields['pos_center'].queryset = PosCenter.objects.filter(store=store)
        elif company:
            self.fields['store'].queryset = Store.objects.filter(company=company)

