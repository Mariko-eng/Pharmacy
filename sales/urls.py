from django.urls import path
from . import views

app_name = 'sales' 

urlpatterns = [

    #Store Purchase Orders     
    path('store/<int:store_id>/sales/list/',views.store_sales_list, name="sales-list"),
    path('store/<int:store_id>/sales/new/',views.store_sales_new, name="sales-new"),
    path('store/<int:store_id>/sales/edit/<int:sale_id>/',views.store_sales_edit, name="sales-edit"),
]
