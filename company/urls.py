from django.urls import path
from . import views

app_name = 'company'

urlpatterns = [
    path('company/application/add/', views.company_application_add_view, name="company-application-add"),
    path('company/account/activate/', views.company_account_activate_view, name="company-account-activate"),
    path('company/admin-user/register/<int:company_id>/', views.company_admin_user_register_view, name="company-admin-user-register"),

    path('company/application/list/', views.company_application_list_view, name="company-application-list"),
    path('company/application/<int:pk>/', views.company_application_detail_view, name="company-application-detail"),
    path('company/application/edit/<int:pk>/', views.company_application_edit_view, name="company-application-edit"),
    path('company/application/delete/<int:pk>/', views.company_application_delete_view, name="company-application-delete"),
    
    path('company/list/', views.company_list_view, name="company-list"),
    path('company/<int:pk>/', views.company_detail_view, name="company-detail"),
    path('company/edit/<int:pk>/', views.company_edit_view, name="company-edit"),
    path('company/delete/<int:pk>/', views.company_delete_view, name="company-delete"),
]
