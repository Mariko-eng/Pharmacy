from django.urls import path
from . import views

urlpatterns = [
    path('stock/new',views.add_new_stock)
]
