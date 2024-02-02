from django.urls import path
from . import views

app_name = 'company'

urlpatterns = [
    path('test_mail/', views.test_mail),


    path('company/application/add/', views.company_application_add_view, name="company-application-add"),
    path('company/account/activate/', views.company_account_activate_view, name="company-account-activate"),
    path('company/<int:company_id>/admin-user/register/', views.company_admin_user_register_view, name="company-admin-user-register"),

    path('company/application/list/', views.company_application_list_view, name="company-application-list"),
    path('company/application/<int:app_id>/', views.company_application_detail_view, name="company-application-detail"),
    path('company/application/<int:app_id>/edit/', views.company_application_edit_view, name="company-application-edit"), 
    path('company/application/<int:app_id>/edit-status/<str:new_status>/', views.company_application_edit_status, name='company-application-edit-status'),
    path('company/application/<int:app_id>/delete/', views.company_application_delete_view, name="company-application-delete"),
    
    path('home/company/list/', views.company_list_view, name="company-list"),
    path('home/company/<int:company_id>/', views.company_detail_view, name="company-detail"),
    path('home/company/<int:company_id>/edit/', views.company_edit_view, name="company-edit"),
    path('home/company/<int:company_id>/deactivate', views.company_deactivate_view, name='company-deactivate'),
    path('home/company/<int:company_id>/delete/', views.company_delete_view, name="company-delete"),

    ## Company Store List
    path('home/company/<int:company_id>/store/list/', views.company_store_list_view, name="company-store-list"),

    ## Store Proifle
    path('home/store/<int:store_id>/profile/', views.store_profile_view, name="store-profile"),
    path('home/store/<int:store_id>/delete/', views.store_delete_view, name="store-delete"),

    path('home/company/<int:company_id>/pos-center/list/', views.pos_list_view, name="company-pos-list"),
    path('home/company/store/<int:store_id>/pos-center/list/', views.pos_list_view, name="store-pos-list"),
    path('home/company/store/<int:store_id>/pos-center/<int:pos_id>/', views.pos_detail_view, name="store-pos-detail"),
    path('home/company/store/<int:store_id>/pos-center/edit/<int:pos_id>/', views.pos_edit_view, name="store-pos-edit"),
    path('home/company/store/<int:store_id>/pos-center/delete/<int:pos_id>/', views.pos_delete_view, name="store-pos-delete"),
]
