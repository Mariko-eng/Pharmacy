from django.urls import path
from . import views

app_name = 'inventory' 

urlpatterns = [
    # Categories
    path('inventory/products/categories/list/company/<int:company_id>/',
        views.product_categories_list, name="company-product-categories-list"),
    path('inventory/products/categories/list/store/<int:store_id>/',
        views.product_categories_list, name="store-product-categories-list"),

    # Variants
    path('inventory/products/variants/list/company/<int:company_id>/',
        views.product_variants_list, name="company-product-variants-list"),
    path('inventory/products/variants/list/store/<int:store_id>/',
        views.product_variants_list, name="store-product-variants-list"),

    # Units
    path('inventory/products/units/list/company/<int:company_id>/',
        views.product_units_list, name="conpany-product-units-list"),
    path('inventory/products/units/list/store/<int:store_id>/',
        views.product_units_list, name="store-product-units-list"),

    # Suppliers
    path('inventory/products/suppliers/list/company/<int:company_id>/',
        views.suppliers_list, name="company-product-suppliers-list"),
    path('inventory/products/suppliers/list/store/<int:store_id>/',
        views.suppliers_list, name="store-product-suppliers-list"),
    
    #Store Products-list
    path('store/inventory/products/list/store/<int:store_id>/',
        views.store_products_list, name="store-products-list"),
    path('store/<int:store_id>/inventory/products/new/',
        views.store_products_new, name="store-products-new"),
    path('store/<int:store_id>/inventory/received_stock/list/',
        views.store_received_stock_list, name="received-stock-list"),
    path('store/<int:store_id>/inventory/received_stock/new/',
        views.store_received_stock_new, name="received-stock-new"),


    # path('stock/',views.StockListCreateView.as_view(), name="stock"),
    # path('stock/new/',views.StockCreateView.as_view(), name="stock"),
    # path('stock/incoming/new/',views.stock_new, name="stock-new"),
    # path('stock/settings/',views.settings_index,name="settings"),
]
