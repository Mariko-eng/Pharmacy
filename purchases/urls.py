from django.urls import path
from . import views

app_name = 'purchase_orders' 

urlpatterns = [

    #Store Purchase Orders     
    path('store/<int:store_id>/purchase_orders/list/',
        views.store_purchase_orders_list, name="purchase-orders-list"),
    path('store/<int:store_id>/purchase_orders/new/',
        views.store_purchase_orders_new, name="purchase-orders-new"),
    path('store/<int:store_id>/purchase_orders/edit/<int:order_request_id>/',
        views.store_purchase_orders_edit, name="purchase-orders"),
]
