
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('',views.index, name="index"),
    path('login',views.index, name="login"),
    path('logout',views.logoutView, name="logout"),

    path('home/',views.home_view,name="home"),  
]
