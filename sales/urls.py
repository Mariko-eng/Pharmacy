from django.urls import path
from . import views

app_name = 'sales' 

urlpatterns = [

    #Store Sales     
    path('store/<int:store_id>/sales/list/', views.store_sales_list, name="store-sales-list"),
    path('store/<int:store_id>/sales/new/', views.store_sales_new, name="store-sales-new"),
    path('store/<int:store_id>/sales/edit/<int:sale_id>/', views.store_sales_edit, name="store-sales-edit"),

    #Pos Sales     
    path('pos/<int:pos_id>/sales/list/', views.pos_sales_list, name="pos-sales-list"),
    path('pos/<int:pos_id>/sales/new/', views.pos_sales_new, name="pos-sales-new"),
]
