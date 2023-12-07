from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('stock/',views.StockListCreateView.as_view(), name="stock"),
    path('stock/new/',views.StockCreateView.as_view(), name="stock"),
    path('stock/incoming/new/',views.stock_new, name="stock-new"),
    path('stock/settings/',views.settings_index,name="settings"),
]
