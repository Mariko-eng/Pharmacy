
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('',views.index, name="index"),
    path('login',views.index, name="login"),
    path('logout',views.logoutView, name="logout"),

    path('home/',views.home_view,name="home"),
    
    path('home/dashboard/',views.super_dashboard,name="super-dashbaord"),
    path('home/dashboard/company/<int:company_id>/', views.company_dashboard, name="company-dashboard"),
    path('home/dashboard/company/', views.company_dashboard, name="company-dashboard"),
    path('home/dashboard/store/<int:store_id>/',views.store_dashboard,name="store-dashbaord"),
    path('home/dashboard/store/',views.store_dashboard,name="store-dashbaord"),
    path('home/dashboard/pos/<int:pos_id>/',views.pos_dashboard,name="pos-dashbaord"),
    path('home/dashboard/pos/',views.pos_dashboard,name="pos-dashbaord"),

    path('home/users/list/',views.users_list_view,name="users-list"),    

    path('home/users/company/<int:company_id>/', views.users_company_list_view,name="users-company-list"),

    path('home/users/company/<int:company_id>/add/', views.users_company_new_view,name="users-company-new"),

    path('home/users/roles/list/',views.users_roles_list_view, name="users-roles-list"),

    path('home/users/roles/<int:role_id>/permissions/',views.users_roles_list_view, name="users-roles-permissions-list"),

    path('home/users/company/<int:company_id>/roles/', 
        views.users_company_roles_list_view, name="users-company-roles-list"),

    path('home/users/company/<int:company_id>/roles/add/', 
        views.users_company_roles_new_view, name="users-company-roles-new"),

    path('home/users/company/<int:company_id>/roles/<int:role_id>/permissions/',
        views.users_company_role_permissions_list_view, name="users-company-roles-permissions-list"),
    
    ]
