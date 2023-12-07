from django.shortcuts import get_object_or_404
from user.models import Company

class CompanyMixin:
    
    def get_user(self):
        # Replace this with your logic to get the company for the user, maybe from session or user profile
        # For demonstration purposes, assuming the company_id is stored in the session
        user = self.request.user
        # print(user)
        return user

    def get_company(self):
        # Replace this with your logic to get the company for the user, maybe from session or user profile
        # For demonstration purposes, assuming the company_id is stored in the session
        company_id = self.request.session.get('company_id')
        company = get_object_or_404(Company, id=company_id)
        # print(company)
        return company

class CompanyFormMixin:

    def get_user(self):
        # Replace this with your logic to get the company for the user, maybe from session or user profile
        # For demonstration purposes, assuming the company_id is stored in the session
        user = self.request.user
        # print(user)
        return user

    def get_company(self):
        # Replace this with your logic to get the company for the user, maybe from session or user profile
        # For demonstration purposes, assuming the company_id is stored in the session
        company_id = self.request.session.get('company_id')
        company = get_object_or_404(Company, id=company_id)
        # print(company)
        return company
    
    def form_valid(self, form):
        form.instance.company = self.get_company()
        form.instance.created_by = self.get_user()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.get_company()
        return context 