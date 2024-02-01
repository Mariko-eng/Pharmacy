from django.urls import path
from . import views

app_name = 'inventory' 

urlpatterns = [
    ## Company Categories
    path('home/company/<int:company_id>/inventory/products/categories/list/',
        views.product_categories_list, name="company-product-categories-list"),
    # Store Categories
    path('home/store/<int:store_id>/inventory/products/categories/list/',
        views.product_categories_list, name="store-product-categories-list"),

    ## Company Variants
    path('home/company/<int:company_id>/inventory/products/variants/list/',
        views.product_variants_list, name="company-product-variants-list"),
    # Store Variants
    path('home/store/<int:store_id>/inventory/products/variants/list/',
        views.product_variants_list, name="store-product-variants-list"),

    ## Company Product Units
    path('home/company/<int:company_id>/inventory/products/units/list/',
        views.product_units_list, name="company-product-units-list"),
    # Store Product Units
    path('home/store/<int:store_id>/inventory/products/units/list/',
        views.product_units_list, name="store-product-units-list"),

    ## Company Suppliers
    path('home/company/<int:company_id>/inventory/products/suppliers/list/',
        views.suppliers_list, name="company-product-suppliers-list"),
    # Store Suppliers
    path('home/store/<int:store_id>/inventory/products/suppliers/list/',
        views.suppliers_list, name="store-product-suppliers-list"),


    ## Company Products
    path('home/company/<int:company_id>/inventory/products/list/',
        views.company_products_list, name="company-products-list"),
    # Store Products
    path('home/store/<int:store_id>/inventory/products/list/',
        views.store_products_list, name="store-products-list"),
    path('home/store/<int:store_id>/inventory/products/detail/<int:store_product_id>/',
        views.store_products_detail, name="store-products-detail"),
    path('home/store/<int:store_id>/inventory/products/new/',
        views.store_products_new, name="store-products-new"),


    ## Company Recieved Stock 
    path('home/company/<int:company_id>/inventory/received_stock/list/',
        views.company_received_stock_list, name="company-received-stock-list"),
    #Store Recieved Stock     
    path('home/store/<int:store_id>/inventory/received_stock/list/',
        views.store_received_stock_list, name="store-received-stock-list"),
    path('home/store/<int:store_id>/inventory/received_stock/detail/<int:received_stock_id>/',
        views.store_received_stock_detail, name="store-received-stock-detail"),
    path('home/store/<int:store_id>/inventory/received_stock/new/',
        views.store_received_stock_new, name="store-received-stock-new"),
    path('home/store/<int:store_id>/inventory/received_stock/edit/<int:received_stock_id>/',
        views.store_received_stock_edit, name="store-received-stock-edit"),

    #Company Recieved Stock     
    path('home/company/<int:company_id>/inventory/stock-requests/list/',
        views.company_stock_requests_list, name="company-stock-requests-list"),

    #Store Recieved Stock     
    path('home/store/<int:store_id>/inventory/stock-requests/list/',
        views.store_stock_requests_list, name="store-stock-requests-list"),
    path('home/store/<int:store_id>/inventory/stock-requests/detail/<int:stock_request_id>/',
        views.store_stock_requests_detail, name="store-stock-requests-detail"),
    path('home/store/<int:store_id>/inventory/stock-requests/new/',
        views.store_stock_requests_new, name="store-stock-requests-new"),
    path('home/store/<int:store_id>/inventory/stock-requests/edit/<int:stock_request_id>/',
        views.store_stock_requests_edit, name="store-stock-requests-edit"),

]
