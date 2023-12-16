from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('',views.index, name="index"),
    path('login',views.index, name="login"),
    path('logout',views.logoutView, name="logout"),

    path('home/',views.home_view,name="home"),    

    path('company/admins/', views.company_admins_list_view, name='company-admins-list'),
    path('company/managers/', views.company_managers_list_view, name='company-managers-list'),


    # ALL - Top Leve;
    path('companies/', views.company_list, name='company-list'),
    path('company/deactivate/<int:company_id>/', views.company_deactivate, name='company-deactivate'),
    path('company/delete/<int:company_id>/', views.company_delete, name='company-delete'),
    path('users-&-roles/', views.users_and_roles_list, name='users-and-roles-list'),
    path('role/<int:id>/permissions/', views.role_permissions_list, name='role-permissions-list'),

    # Company
    path('company/<int:company_id>/', views.company_detail, name='company-detail'),
    path('company/<int:company_id>/branches/', views.company_branches_list, name='company-branch-list'),
    path('company/<int:company_id>/pos/', views.company_pos_list, name='company-pos-list'),
    path('company/<int:company_id>/users/', views.company_users_list, name='company-users-list'),

    # Branch
    path('company/<int:company_id>/branch/<int:branch_id>/', views.company_branch_detail, name='company-branch-detail'),
    path('company/<int:company_id>/branch/<int:branch_id>/pos/', views.company_branch_pos_list, name='company-branch-pos-list'),
    path('company/<int:company_id>/branch/<int:branch_id>/users/', views.company_branch_users_list, name='company-branch-users-list'),

    # Pos
    path('company/<int:company_id>/branch/<int:branch_id>/pos/<int:pos_id>/', views.company_branch_pos_detail, name='company-branch-pos-detail'),
    path('company/<int:company_id>/branch/<int:branch_id>/pos/<int:pos_id>/users/', views.company_branch_pos_users_list, name='company-branch-pos-users-list'),


]
