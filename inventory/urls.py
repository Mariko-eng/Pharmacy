from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('stock',views.stock_index, name="stock"),
    path('stock/new',views.stock_new, name="stock-new"),
    path('stock/settings/',views.settings_index,name="settings"),
]
