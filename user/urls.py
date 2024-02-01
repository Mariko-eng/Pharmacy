
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('',views.index, name="index"),
    path('login',views.index, name="login"),
    path('logout',views.logoutView, name="logout"),

    path('home/',views.home_view,name="home"),
    
    path('home/dashboard/',views.super_dashboard, name="super-dashboard"),
    path('home/company/<int:company_id>/dashboard/', views.company_dashboard, name="company-dashboard"),
    path('home/company/dashboard/', views.company_dashboard, name="company-dashboard"),
    path('home/store/<int:store_id>/dashboard/', views.store_dashboard, name="store-dashboard"),
    path('home/store/dashboard/', views.store_dashboard, name="store-dashboard"),
    path('home/pos/dashboard//<int:pos_id>/', views.pos_dashboard, name="pos-dashboard"),
    path('home/pos/dashboard/', views.pos_dashboard, name="pos-dashboard"),

    path('home/users/list/',views.users_list_view,name="users-list"),  
    path('home/user-roles/list/',views.users_roles_list_view, name="users-roles-list"),  
    path('home/user-roles/<int:role_id>/permissions/',views.users_roles_list_view, name="users-roles-permissions-list"),

    path('home/company/<int:company_id>/users/', views.users_company_list_view, name="users-company-list"),
    path('home/company/<int:company_id>/users/add/', views.users_company_new_view,name="users-company-new"),
    path('home/company/<int:company_id>/users/company_admin/add/', views.users_company_admin_user_new, name="users-company-admin-new"),
    path('home/company/<int:company_id>/users/store_admin/add/', views.users_company_store_admin_user_new, name="users-company-store-admin-new"),

    path('home/store/<int:store_id>/users/', views.users_store_list_view, name="users-store-list"),
    path('home/store/<int:store_id>/users/add/', views.users_store_new_view,name="users-store-new"),
    path('home/store/<int:store_id>/users/store_admin/add/', views.users_store_admin_user_new, name="users-store-admin-new"),
    path('home/store/<int:store_id>/users/pos_attendant/add/', views.users_store_pos_attendant_user_new, name="users-store-pos-attendant-new"),

    path('home/company/<int:company_id>/user-roles/', views.users_company_roles_list_view, name="users-company-roles-list"),
    path('home/company/<int:company_id>/user-roles/add/', views.users_company_roles_new_view, name="users-company-roles-new"),
    path('home/company/<int:company_id>/user-roles/<int:role_id>/permissions/',views.users_company_role_permissions_list_view, name="users-company-roles-permissions-list"),
    ]
