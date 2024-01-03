# from django import forms
# from django.contrib.auth.models import Permission
# from .models import Company
# from .models import CompanyBranch
# from .models import CompanyPos
# from .models import User
# from .permissions import DefaultGroups
# # from .models import AppRoles
# # from .models import CompanyRoles
# # from .models import BranchRoles

# class CompanyForm(forms.ModelForm):
#     first_name = forms.CharField(max_length=30) # Company Owner  Details
#     last_name = forms.CharField(max_length=30) # Company Owner  Details
#     email = forms.CharField(max_length=30) # Company Owner  Details
#     phone_number = forms.CharField(max_length=30) # Company Owner  Details
#     class Meta:
#         model = Company
#         fields = ['name']

# class CompanyBranchForm(forms.ModelForm):
#     branch_type = forms.ChoiceField(choices=[('', '---------')] + CompanyBranch.BRANCH_TYPES)
#     region = forms.ChoiceField(choices=[('', '---------')] + CompanyBranch.REGION_CHOICES)
#     class Meta:
#         model = CompanyBranch
#         fields = ['name','branch_type','region','district','village']

# class CompanyPosForm(forms.ModelForm):
#     class Meta:
#         model = CompanyPos
#         fields = ['unique_no']

# class AppUserForm(forms.ModelForm):
#     first_name = forms.CharField(max_length=30)
#     last_name = forms.CharField(max_length=30)
#     email = forms.CharField(max_length=30)
#     phone_number = forms.CharField(max_length=30)
#     is_superuser = forms.BooleanField(initial=False, required=False)
#     is_staff = forms.BooleanField(initial = True)
#     class Meta:
#         model = User
#         fields = ['first_name','last_name', 'email', 'phone_number', 'is_superuser', 'is_staff',]

# class CompanyUserForm(forms.ModelForm):
#     first_name = forms.CharField(max_length=30)
#     last_name = forms.CharField(max_length=30)
#     email = forms.CharField(max_length=30)
#     phone_number = forms.CharField(max_length=30)
#     roles = forms.MultipleChoiceField(
#         choices=[('', '---------')] + DefaultGroups.choices,
#         widget= forms.CheckboxSelectMultiple())
#     access_to_all_branches = forms.BooleanField(
#         initial=False, 
#         required=False,
#         widget=forms.CheckboxInput()
#         )
#     branches = forms.ModelMultipleChoiceField(
#         queryset= None,  # Provide the queryset
#         required= False,
#         widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),  # Add Bootstrap classes
#     )

#     def __init__(self, *args, company=None, **kwargs):
#         super(CompanyUserForm, self).__init__(*args, **kwargs)
#         # Get the default choices from the BranchRoles enum
#         role_choices = [(role.value, role.label) for role in DefaultGroups]
#         # Exclude ACCOUNT_HOLDER from the choices
#         role_choices = [choice for choice in role_choices if choice[0] != DefaultGroups.ACCOUNT_HOLDER]
#         # Set the updated choices for the 'role' field
#         self.fields['roles'].choices = role_choices

#         if company:
#             self.fields['branches'].queryset = CompanyBranch.objects.filter(company=company)

#     class Meta:
#         model = User
#         fields = ['first_name','last_name', 'email', 'phone_number',]

#     def clean(self):
#         cleaned_data = super().clean()
#         roles = cleaned_data.get('roles')

#         if not len(roles):
#             raise forms.ValidationError("Select at least one role for the user")

#         return cleaned_data
    
#     def clean_branches(self):
#         cleaned_data = super().clean()
#         roles = cleaned_data.get('roles')
#         branches = cleaned_data.get('branches')

#         if not len(roles):
#             raise forms.ValidationError("Select at least one role for the user")

#         if 'Company Admin' not in roles and not len(branches):
#             raise forms.ValidationError("Select at least one branch if the role is not 'Company Admin'.")

#         return branches

# class CompanyRoleFrom(forms.Form):
#     name = forms.CharField(max_length=30)        

# # class AdminUserForm(forms.ModelForm):
# #     first_name = forms.CharField(max_length=30)
# #     last_name = forms.CharField(max_length=30)
# #     email = forms.CharField(max_length=30)
# #     phone_number = forms.CharField(max_length=30)
# #     role = forms.ChoiceField(choices=[('', '---------')] + CompanyRoles.choices)

# #     def __init__(self, *args, **kwargs):
# #         super().__init__(*args, **kwargs)
# #         # Get the default choices from the CompanyRoles enum
# #         role_choices = [(role.value, role.label) for role in CompanyRoles]
# #         # Exclude COMPANY_OWNER from the choices
# #         role_choices = [choice for choice in role_choices if choice[0] != CompanyRoles.COMPANY_OWNER]
# #         # Set the updated choices for the 'role' field
# #         self.fields['role'].choices = role_choices
# #     class Meta:
# #         model = User
# #         fields = ['first_name','last_name', 'email', 'phone_number']


# # class ManagerUserForm(forms.ModelForm):
# #     first_name = forms.CharField(max_length=30)
# #     last_name = forms.CharField(max_length=30)
# #     email = forms.CharField(max_length=30)
# #     phone_number = forms.CharField(max_length=30)
# #     role = forms.ChoiceField(choices=[('', '---------')] + BranchRoles.choices)
# #     branch = forms.ModelChoiceField(
# #         queryset= None,  # Provide the queryset
# #         required= True,  # Set to True if you want it to be required
# #     )

# #     # def __init__(self, companyinstance = None, *args, **kwargs):
# #     def __init__(self, *args, company=None, **kwargs):
# #         super(ManagerUserForm, self).__init__(*args, **kwargs)
# #         # Get the default choices from the BranchRoles enum
# #         role_choices = [(role.value, role.label) for role in BranchRoles]
# #         # Include only BRANCH_MANAGER from the choices
# #         role_choices = [choice for choice in role_choices if choice[0] == BranchRoles.BRANCH_MANAGER]
# #         # Set the updated choices for the 'role' field
# #         self.fields['role'].choices = role_choices

# #         if company:
# #             self.fields['branch'].queryset = CompanyBranch.objects.filter(company=company)
# #     class Meta:
# #         model = User
# #         fields = ['first_name','last_name', 'email', 'phone_number']


# # class PosUserForm(forms.ModelForm):
# #     first_name = forms.CharField(max_length=30)
# #     last_name = forms.CharField(max_length=30)
# #     email = forms.CharField(max_length=30)
# #     phone_number = forms.CharField(max_length=30)
# #     role = forms.ChoiceField(choices=[('', '---------')] + BranchRoles.choices)
# #     pos = forms.ModelChoiceField(
# #         queryset= None,  # Provide the queryset
# #         required= True,  # Set to True if you want it to be required
# #     )

# #     def __init__(self,*args,company= None, branch= None, **kwargs):
# #         super().__init__(*args, **kwargs)
# #         # Get the default choices from the BranchRoles enum
# #         role_choices = [(role.value, role.label) for role in BranchRoles]
# #         # Include only POS_ATTENDANT from the choices
# #         role_choices = [choice for choice in role_choices if choice[0] == BranchRoles.POS_ATTENDANT]
# #         # Set the updated choices for the 'role' field
# #         self.fields['role'].choices = role_choices

# #         if company:
# #             if branch:
# #                 self.fields['pos'].queryset = CompanyPos.objects.filter(company=company,branch=branch)
# #     class Meta:
# #         model = User
# #         fields = ['first_name','last_name', 'email', 'phone_number']


# # class OtherStaffUserForm(forms.ModelForm):
# #     first_name = forms.CharField(max_length=30)
# #     last_name = forms.CharField(max_length=30)
# #     email = forms.CharField(max_length=30)
# #     phone_number = forms.CharField(max_length=30)
# #     role = forms.ChoiceField(choices=[('', '---------')] + BranchRoles.choices)

# #     def __init__(self, *args, **kwargs):
# #         super().__init__(*args, **kwargs)
# #         # Get the default choices from the BranchRoles enum
# #         role_choices = [(role.value, role.label) for role in BranchRoles]
# #         # Exclude POS_ATTENDANT & BRANCH_MANAGER from the choices
# #         role_choices = [choice for choice in role_choices if choice[0] != BranchRoles.BRANCH_MANAGER]
# #         role_choices = [choice for choice in role_choices if choice[0] != BranchRoles.POS_ATTENDANT]
# #         # Set the updated choices for the 'role' field
# #         self.fields['role'].choices = role_choices
# #     class Meta:
# #         model = User
# #         fields = ['first_name','last_name', 'email', 'phone_number']

# class CompanyStaffUserFormA(forms.ModelForm):
#     first_name = forms.CharField(max_length=30)
#     last_name = forms.CharField(max_length=30)
#     email = forms.CharField(max_length=30)
#     phone_number = forms.CharField(max_length=30)
#     branch = forms.ModelChoiceField(
#         queryset= None,  # Provide the queryset
#         required= True,  # Set to True if you want it to be required
#     )

#     def __init__(self, *args, company=None, **kwargs):
#         super(CompanyStaffUserFormA, self).__init__(*args, **kwargs)
        
#         # Filter the queryset based on the company
#         if company:
#             self.fields['branch'].queryset = CompanyBranch.objects.filter(company=company)
#     class Meta:
#         model = User
#         fields = ['first_name','last_name', 'email', 'phone_number']

# class CompanyStaffUserFormB(forms.ModelForm):
#     first_name = forms.CharField(max_length=30)
#     last_name = forms.CharField(max_length=30)
#     email = forms.CharField(max_length=30)
#     phone_number = forms.CharField(max_length=30)
#     class Meta:
#         model = User
#         fields = ['first_name','last_name', 'email', 'phone_number']

# class CompanyPosAttendantForm(forms.ModelForm):
#     first_name = forms.CharField(max_length=30)
#     last_name = forms.CharField(max_length=30)
#     email = forms.CharField(max_length=30)
#     phone_number = forms.CharField(max_length=30)
#     pos = forms.ModelChoiceField(
#         queryset= None,  # Provide the queryset
#         required= True,  # Set to True if you want it to be required
#     )

#     def __init__(self, *args, branch=None, **kwargs):
#         super(CompanyPosAttendantForm, self).__init__(*args, **kwargs)
        
#         # Filter the queryset based on the company
#         if branch:
#             self.fields['pos'].queryset = CompanyPos.objects.filter(branch=branch)
#     class Meta:
#         model = User
#         fields = ['first_name','last_name', 'email', 'phone_number']


# # class NameForm(forms.Form):
# #     name = forms.CharField(label="Your name", max_length=100,)
# #     state = forms.CharField(label="Your state", max_length=100,)
# #     terms = forms.CharField(label="Your terms", max_length=100,)

# #     def clean_name(self):
# #         name = self.cleaned_data.get('name')
# #         if name.lower() == 'mark':
# #             raise forms.ValidationError("Bad name: 'Mark' is not allowed.")
# #         return name