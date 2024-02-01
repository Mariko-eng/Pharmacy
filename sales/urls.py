from django.urls import path
from . import views

app_name = 'sales' 

urlpatterns = [
    
    # Company Sales     
    path('home/company/<int:company_id>/sales/list/', views.company_sales_list, name="company-sales-list"),

    # Store Sales     
    path('home/store/<int:store_id>/sales/list/', views.store_sales_list, name="store-sales-list"),
    path('home/store/<int:store_id>/sales/new/', views.store_sales_new, name="store-sales-new"),
    path('home/store/<int:store_id>/sales/detail/<int:sale_id>/', views.store_sales_detail, name="store-sales-detail"),
    path('home/store/<int:store_id>/sales/invoice/<int:sale_id>/', views.store_sales_invoice, name="store-sales-invoice"),
    path('home/store/<int:store_id>/sales/edit/<int:sale_id>/', views.store_sales_edit, name="store-sales-edit"),

    # Pos Sales     
    path('home/pos/<int:pos_id>/sales/list/', views.pos_sales_list, name="pos-sales-list"),
    path('home/pos/<int:pos_id>/sales/new/', views.pos_sales_new, name="pos-sales-new"),
]
