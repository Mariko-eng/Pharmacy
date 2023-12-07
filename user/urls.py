from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('',views.index, name="index"),
    path('login',views.index, name="login"),
    path('logout',views.logoutView, name="logout"),

    path('home/',views.home_view,name="home"),
    path('home/super/',views.home_super_view,name="home-super"),
    path('super/all-users/', views.super_all_users_view, name='super-all-users'),
    path('super/all-users/', views.super_all_users_view, name='super-all-users'),
    path('super/roles-edit/<int:id>/', views.super_roles_permissions_edit_view, name='super-roles-permissions-edit'),
    
    path('company/home/<int:id>/', views.company_home_view, name='company-home')
]
