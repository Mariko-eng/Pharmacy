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
    path('company/<int:company_id>/', views.company_detail_view, name="company-detail"),
    path('company/edit/<int:company_id>/', views.company_edit_view, name="company-edit"),
    path('company/deactivate/<int:company_id>/', views.company_deactivate_view, name='company-deactivate'),
    path('company/delete/<int:company_id>/', views.company_delete_view, name="company-delete"),

    path('company/<int:company_id>/store/list/', views.store_list_view, name="company-store-list"),
    path('company/<int:company_id>/store/<int:store_id>/', views.store_detail_view, name="company-store-detail"),
    path('company/<int:company_id>/store/edit/<int:store_id>/', views.store_edit_view, name="company-store-edit"),
    path('company/<int:company_id>/store/delete/<int:store_id>/', views.store_delete_view, name="company-store-delete"),

    path('company/<int:company_id>/pos-center/list/', views.pos_list_view, name="company-pos-list"),
    path('company/store/<int:store_id>/pos-center/list/', views.pos_list_view, name="store-pos-list"),
    path('company/store/<int:store_id>/pos-center/<int:pos_id>/', views.pos_detail_view, name="store-pos-detail"),
    path('company/store/<int:store_id>/pos-center/edit/<int:pos_id>/', views.pos_edit_view, name="store-pos-edit"),
    path('company/store/<int:store_id>/pos-center/delete/<int:pos_id>/', views.pos_delete_view, name="store-pos-delete"),
]
