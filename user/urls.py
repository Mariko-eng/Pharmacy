from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('',views.index, name="index"),
    path('login',views.index, name="login"),
    path('logout',views.logoutView, name="logout"),

    path('home/',views.home_view,name="home"),
    path('home/super/',views.home_super_view,name="home-super"),
    path('company/list/', views.company_view, name='company-list'),
    path('company/home/<int:id>/', views.company_home_view, name='company-home')
]
