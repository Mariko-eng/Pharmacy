from django.shortcuts import render, redirect
from django.db import transaction
from django.forms import ValidationError
from django.views import View
from django.views.generic import ListView,CreateView
from django.http import JsonResponse
from .forms import ProductCategoryForm, ProductVariantForm
from .forms import ProductUnitsForm, SupplierForm
from .forms import StoreProductForm, ReceivedStockForm,ReceivedStockItemForm
from .forms import StockRequestForm, StockRequestItemForm
from .models import ProductVariant, ProductCategory, ProductUnits, Product, StoreProduct
from .models import ReceivedStock, ReceivedStockItem
from .models import StockRequest, StockRequestItem
from .mixins import CompanyMixin, CompanyFormMixin
from company.models import Company, Store, Supplier
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from .forms import RequiredFormSet
from django.shortcuts import get_object_or_404


def product_categories_list(request,store_id = None, company_id = None):
    form = ProductCategoryForm()
    context = {
        "form" : form
    }

    store = None
    if store_id is not None:
        store = Store.objects.get(pk=store_id)
        company = store.company
        context["store"] = store
        context["company"] = company
    elif company_id is not None:
        company = Company.objects.get(pk=company_id)
        context["company"] = company

    categories = ProductCategory.objects.filter(company = company)
    context["categories"] = categories

    if request.is_ajax():
        if request.method == "POST":
            form = ProductCategoryForm(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                if ProductCategory.objects.filter(name = category.name.capitalize(), company = company).exists():
                    form.errors['name'] = ["Name ALready Exists!"]
                    return JsonResponse({'success': False, 'errors': form.errors})
                category.name = category.name.capitalize()
                category.company = company
                category.save()
                return JsonResponse({'success': True, 'category_id': category.id})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
            
    return render(request, 'categories/index.html', context=context) 


def product_variants_list(request,store_id = None, company_id = None):
    form = ProductVariantForm()

    context = { "form" : form }

    store = None
    if store_id is not None:
        store = Store.objects.get(pk=store_id)
        company = store.company
        context["store"] = store
        context["company"] = company
    elif company_id is not None:
        company = Company.objects.get(pk=company_id)
        context["company"] = company

    variants = ProductVariant.objects.filter(company = company)
    context["variants"] = variants

    if request.is_ajax():
        if request.method == "POST":
            form = ProductVariantForm(request.POST)
            if form.is_valid():
                variant = form.save(commit=False)
                if ProductVariant.objects.filter(name = variant.name.capitalize(), company = company).exists():
                    form.errors['name'] = ["Name ALready Exists!"]
                    return JsonResponse({'success': False, 'errors': form.errors})
                variant.name = variant.name.capitalize()
                variant.company = company
                variant.save()
                return JsonResponse({'success': True, 'variant_id': variant.id})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
            
    return render(request, 'settings/variants/index.html', context=context) 


def product_units_list(request,store_id = None, company_id = None):
    form = ProductUnitsForm()

    context = { "form" : form}

    store = None
    if store_id is not None:
        store = Store.objects.get(pk=store_id)
        company = store.company
        context["store"] = store
        context["company"] = company
    elif company_id is not None:
        company = Company.objects.get(pk=company_id)
        context["company"] = company

    units = ProductUnits.objects.filter(company = company)
    context["units"] = units

    if request.is_ajax():
        if request.method == "POST":
            form = ProductUnitsForm(request.POST)
            if form.is_valid():
                unit = form.save(commit=False)
                if ProductUnits.objects.filter(name = unit.name.capitalize(), company = company).exists():
                    form.errors['name'] = ["Name ALready Exists!"]
                    return JsonResponse({'success': False, 'errors': form.errors})
                unit.name = unit.name.capitalize()
                unit.company = company
                unit.save()
                return JsonResponse({'success': True, 'unit_id': unit.id})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
            
    return render(request, 'settings/units/index.html', context=context) 


def suppliers_list(request, store_id = None, company_id = None):
    form = SupplierForm()

    context = { "form" : form}

    store = None
    if store_id is not None:
        store = Store.objects.get(pk=store_id)
        company = store.company
        context["store"] = store
        context["company"] = company
    elif company_id is not None:
        company = Company.objects.get(pk=company_id)
        context["company"] = company

    suppliers = Supplier.objects.filter(company = company)
    context["suppliers"] = suppliers

    if request.is_ajax():
        if request.method == "POST":
            form = SupplierForm(request.POST)
            if form.is_valid():
                supplier = form.save(commit=False)
                if Supplier.objects.filter(name = supplier.name.capitalize(), company = company).exists():
                    form.errors['name'] = ["Name ALready Exists!"]
                    return JsonResponse({'success': False, 'errors': form.errors})
                supplier.name = supplier.name.capitalize()
                supplier.company = company
                supplier.save()
                return JsonResponse({'success': True, 'supplier_id': supplier.id})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
            
    return render(request, 'suppliers/index.html', context=context) 


def store_products_list(request, store_id):
    products = StoreProduct.objects.none()

    context = { "products" : products }

    store = None
    if store_id is not None:
        store = Store.objects.get(pk=store_id)
        company = store.company
        context["store"] = store
        context["company"] = company

    products = StoreProduct.objects.filter(store = store)
    context["products"] = products

    return render(request, 'products/list/index.html', context=context) 


def store_products_new(request, store_id):
    form = StoreProductForm()

    context = { "form" : form}

    store = None
    if store_id is not None:
        store = Store.objects.get(pk=store_id)
        company = store.company
        context["store"] = store
        context["company"] = company

    if request.method == "POST":
        form = StoreProductForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            category = form.cleaned_data.get("category")
            variant = form.cleaned_data.get("variant")
            units = form.cleaned_data.get("units")
            description = form.cleaned_data.get("description")
            item_photo = form.cleaned_data.get("item_photo", None)
            unit_price = form.cleaned_data.get("unit_price")
            reorder_min_qty = form.cleaned_data.get("reorder_min_qty")
            is_for_sale = form.cleaned_data.get("is_for_sale", True)
            is_consummable = form.cleaned_data.get("is_consummable", False)

            product, _  = Product.objects.get_or_create(
                company = company,
                name = name.capitalize(),
                category = category,
                variant = variant,
                units = units
            )

            product.created_by = request.user
            product.save()


            store_product, _ = StoreProduct.objects.get_or_create(store= store, product = product)

            store_product.description = description
            store_product.item_photo = item_photo
            store_product.unit_price = unit_price
            store_product.reorder_min_qty = reorder_min_qty
            store_product.is_for_sale = is_for_sale
            store_product.is_consummable = is_consummable
            store_product.created_by = request.user
            store_product.save()

            return redirect('inventory:store-products-list', store_id=store_id)
        else:
            context["form"] = form

    return render(request, 'products/new/index.html', context=context) 


def store_received_stock_list(request, store_id):
    store = Store.objects.get(pk=store_id)
    company = store.company

    items = ReceivedStock.objects.filter(store = store)
    context = {
        "company": company,
        "store": store,
        "items": items
        }

    return render(request, 'received_stock/list/index.html', context=context) 


def store_received_stock_new(request, store_id):
    store = Store.objects.get(pk=store_id)
    company = store.company

    context = {
        "company": company,
        "store": store}

    form = ReceivedStockForm(company=company)
    
    # ReceivedStockItemFormSet = formset_factory(ReceivedStockItemForm, extra=1, validate_min=True)
    ReceivedStockItemFormSet = formset_factory(ReceivedStockItemForm, formset=RequiredFormSet, extra=1, validate_min=True)

    formset = ReceivedStockItemFormSet(prefix='items')

    if request.method == "POST":
        form_data = ReceivedStockForm(request.POST,company=company)
        formset_data = ReceivedStockItemFormSet(request.POST, prefix='items')

        if form_data.is_valid() and formset_data.is_valid():
            supplier_type = form_data.cleaned_data.get("supplier_type", None)
            supplier_entity =  form_data.cleaned_data.get("supplier_entity", None)
            supplier_store =  form_data.cleaned_data.get("supplier_store", None)
            
            if supplier_type == "SUPPLIER" and supplier_entity is None:
                form_data.add_error("supplier_entity", ValidationError("Select a supplier!"))
                context['form'] = form_data
                context['formset'] = formset 
                return render(request, 'received_stock/new/index.html', context=context)
            elif supplier_type == "STORE" and supplier_store is None:
                form_data.add_error("supplier_store", ValidationError("Select a store!"))
                context['form'] = form_data
                context['formset'] = formset 
                return render(request, 'received_stock/new/index.html', context=context)

            
            received_stock = ReceivedStock(
                supplier_type = supplier_type,
                supplier_entity = supplier_entity,
                supplier_store = supplier_store,
                delivered_by_name = form_data.cleaned_data.get("delivered_by_name"),
                delivered_by_phone = form_data.cleaned_data.get("delivered_by_phone"),
                received_date = form_data.cleaned_data.get("received_date"),
                delivery_notes = form_data.cleaned_data.get("delivery_notes"),
                company = company,
                store = store,
            )
            
            received_stock.company = company
            received_stock.store = store
            received_stock.created_by = request.user
            received_stock.save()

            for formset_data_item in formset_data:
                item = formset_data_item.save(commit=False)
                item.received_stock = received_stock
                item.company = company
                item.store = store
                item.created_by = request.user
                item.save() 

                qty_received = formset_data_item.cleaned_data.get("qty_received")
                store_product = item.store_product
                store_product.available_qty +=  qty_received
                store_product.save()

            context['success_message'] = 'Stock added successfully'
            return redirect('inventory:received-stock-list', store_id=store_id)
        else:
            context['form'] = form_data
            context['formset'] = formset_data
            return render(request, 'received_stock/new/index.html', context=context)
    
    context['form'] = form  
    context['formset'] = formset  
    return render(request, 'received_stock/new/index.html', context=context) 


def store_received_stock_edit(request, store_id, received_stock_id):
    store = get_object_or_404(Store, pk=store_id)
    company = store.company

    received_stock = get_object_or_404(ReceivedStock, pk=received_stock_id, store=store)

    context = {
        "company": company,
        "store": store,
        "received_stock": received_stock,
    }

    form = ReceivedStockForm(instance = received_stock, company=company)

    ReceivedStockItemFormSet = modelformset_factory(ReceivedStockItem, form=ReceivedStockItemForm, extra=0)
    qs = received_stock.receivedstockitem_set.all()
    formset = ReceivedStockItemFormSet(prefix='items',queryset=qs)

    if request.method == "POST":
        form_data = ReceivedStockForm(request.POST, instance=received_stock, company=company)
        formset_data = ReceivedStockItemFormSet(request.POST, prefix='items', queryset=qs)

        if form_data.is_valid() and formset_data.is_valid():
            # Update the received stock details
            form_data.save()

            # Update each item in the formset
            for formset_data_item in formset_data:
                item = formset_data_item.save(commit=False)
                if item.id is None:
                    print("New")
                    item.received_stock = received_stock
                    item.company = company
                    item.store = store
                    item.created_by = request.user
                    item.save()
                
                    # Update store product quantities
                    qty_received = formset_data_item.cleaned_data.get("qty_received")
                    store_product = item.store_product
                    store_product.available_qty += qty_received
                    store_product.save()
                else:
                    print("Old")
                    item.save()
                    # Update store product quantities
                    qty_received = formset_data_item.cleaned_data.get("qty_received")
                    store_product = item.store_product
                    store_product.available_qty -= store_product.available_qty
                    store_product.available_qty += qty_received
                    store_product.save()

            context['success_message'] = 'Stock edited successfully'
            return redirect('inventory:received-stock-list', store_id=store_id)
        else:
            context['form'] = form_data
            context['formset'] = formset_data
            return render(request, 'received_stock/edit/index.html', context=context)

    
    context['form'] = form
    context['formset'] = formset
    return render(request, 'received_stock/edit/index.html', context=context)



def store_stock_requests_list(request, store_id):
    store = Store.objects.get(pk=store_id)
    company = store.company

    items = StockRequest.objects.filter(store = store)
    context = {
        "company": company,
        "store": store,
        "items": items
        }

    return render(request, 'stock_requests/list/index.html', context=context) 


def store_stock_requests_new(request, store_id):
    store = Store.objects.get(pk=store_id)
    company = store.company

    context = {
        "company": company,
        "store": store}

    form = StockRequestForm(company=company)
    
    StockRequestItemFormSet = formset_factory(StockRequestItemForm, formset=RequiredFormSet, extra=1, validate_min=True)

    formset = StockRequestItemFormSet(prefix='items')

    if request.method == "POST":
        form_data = StockRequestForm(request.POST,company=company)
        formset_data = StockRequestItemFormSet(request.POST, prefix='items')

        if form_data.is_valid() and formset_data.is_valid():
            supplier_type = form_data.cleaned_data.get("supplier_type", None)
            supplier_entity =  form_data.cleaned_data.get("supplier_entity", None)
            supplier_store =  form_data.cleaned_data.get("supplier_store", None)
            
            if supplier_type == "SUPPLIER" and supplier_entity is None:
                form_data.add_error("supplier_entity", ValidationError("Select a supplier!"))
                context['form'] = form_data
                context['formset'] = formset 
                return render(request, 'received_stock/new/index.html', context=context)
            elif supplier_type == "STORE" and supplier_store is None:
                form_data.add_error("supplier_store", ValidationError("Select a store!"))
                context['form'] = form_data
                context['formset'] = formset 
                return render(request, 'received_stock/new/index.html', context=context)

            
            received_stock = StockRequest(
                supplier_type = supplier_type,
                supplier_entity = supplier_entity,
                supplier_store = supplier_store,
                delivered_by_name = form_data.cleaned_data.get("delivered_by_name"),
                delivered_by_phone = form_data.cleaned_data.get("delivered_by_phone"),
                received_date = form_data.cleaned_data.get("received_date"),
                delivery_notes = form_data.cleaned_data.get("delivery_notes"),
                company = company,
                store = store,
            )
            
            received_stock.company = company
            received_stock.store = store
            received_stock.created_by = request.user
            received_stock.save()

            for formset_data_item in formset_data:
                item = formset_data_item.save(commit=False)
                item.received_stock = received_stock
                item.company = company
                item.store = store
                item.created_by = request.user
                item.save() 

                qty_received = formset_data_item.cleaned_data.get("qty_received")
                store_product = item.store_product
                store_product.available_qty +=  qty_received
                store_product.save()

            context['success_message'] = 'Stock added successfully'
            return redirect('inventory:stock-requests-list', store_id=store_id)
        else:
            context['form'] = form_data
            context['formset'] = formset_data
            return render(request, 'stock_requests/new/index.html', context=context)
    
    context['form'] = form  
    context['formset'] = formset  
    return render(request, 'stock_requests/new/index.html', context=context) 


def store_stock_requests_edit(request, store_id, stock_request_id):
    store = get_object_or_404(Store, pk=store_id)
    company = store.company

    received_stock = get_object_or_404(StockRequest, pk=stock_request_id, store=store)

    context = {
        "company": company,
        "store": store,
        "received_stock": received_stock,
    }

    form = StockRequestForm(instance = received_stock, company=company)

    StockRequestItemFormSet = modelformset_factory(StockRequestItem, form=StockRequestItemForm, extra=0)
    qs = received_stock.receivedstockitem_set.all()
    formset = StockRequestItemFormSet(prefix='items',queryset=qs)

    if request.method == "POST":
        form_data = StockRequestForm(request.POST, instance=received_stock, company=company)
        formset_data = StockRequestItemFormSet(request.POST, prefix='items', queryset=qs)

        if form_data.is_valid() and formset_data.is_valid():
            # Update the received stock details
            form_data.save()

            # Update each item in the formset
            for formset_data_item in formset_data:
                item = formset_data_item.save(commit=False)
                if item.id is None:
                    print("New")
                    item.received_stock = received_stock
                    item.company = company
                    item.store = store
                    item.created_by = request.user
                    item.save()
                
                    # Update store product quantities
                    qty_received = formset_data_item.cleaned_data.get("qty_received")
                    store_product = item.store_product
                    store_product.available_qty += qty_received
                    store_product.save()
                else:
                    print("Old")
                    item.save()
                    # Update store product quantities
                    qty_received = formset_data_item.cleaned_data.get("qty_received")
                    store_product = item.store_product
                    store_product.available_qty -= store_product.available_qty
                    store_product.available_qty += qty_received
                    store_product.save()

            context['success_message'] = 'Stock edited successfully'
            return redirect('inventory:stock-requests-list', store_id=store_id)
        else:
            context['form'] = form_data
            context['formset'] = formset_data
            return render(request, 'stock_requests/edit/index.html', context=context)

    
    context['form'] = form
    context['formset'] = formset
    return render(request, 'stock_requests/edit/index.html', context=context)














# class StockListCreateView(CompanyMixin, View):
#     form_class = ProductForm
#     initial = {"unit_price": 0}
#     template_name = "stock/index.html"

#     def get(self, request, *args, **kwargs):
#         form = self.form_class(initial=self.initial)
#         data = Product.objects.all()
#         return render(request, self.template_name, {"form": form, "results": data})

#     def post(self, request, *args, **kwargs): 
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.instance.company = self.get_company()
#             form.instance.created_by = self.get_user()
#             product = form.save(commit=False)
#             product.name = product.name.capitalize()
#             product.save() 

#             if self.request.is_ajax(): # Using Ajax 
#                 return JsonResponse({'success': True, 'name': product.name})
#         else: # Form is Invalid
#             if self.request.is_ajax(): # Using Ajax 
#                 return JsonResponse({'success': False, 'errors': form.errors})
        
#         return render(request, self.template_name, {"form": form})

# class StockCreateView(CompanyFormMixin, CreateView):
#     model = Product
#     form_class = ProductForm
#     template_name = 'stock/index.html'

#     def form_valid(self, form):
#         form.instance.company = self.get_company()
#         form.instance.created_by = self.get_user()
#         product = form.save(commit=False)
#         product.name = product.name.capitalize()
#         product.save() 
#         print(product.company)    
#         print(product.created_by)                  

#         if self.request.is_ajax():
#             # If it's an AJAX request, return a JsonResponse
#             return JsonResponse({'success': True, 'name': product.name})
#         else:
#             # If it's a regular form submission, redirect to success URL
#             return super().form_valid(form)


#     def form_invalid(self, form):
#         print("form.errors")

#         if self.request.is_ajax():
#             return JsonResponse({'success': False, 'errors': form.errors})
#         else:
#             # If it's a regular form submission and the form is invalid, render the form
#             return self.render_to_response(self.get_context_data(form=form))

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # print("context")
#         # print(context["company"])
#         return context


# def settings_index(request):
#     company_id = request.session.get('company_id', None)
#     company = None
#     if company_id is not None:
#         company = Company.objects.get(pk=company_id)
#     elif request.user.company:
#         company = request.user.company

#     productVariantForm = ProductVariantForm(prefix="ProductVariantForm")
#     productCategoryForm = ProductCategoryForm(prefix="productCategoryForm")
#     productUnitsForm = ProductUnitsForm(prefix="productUnitsForm")

#     productVariants = ProductVariant.objects.all()
#     productCategories = ProductCategory.objects.all()
#     productUnits = ProductUnits.objects.all()

#     context = {
#         "company" : company,
#         "productVariants" : productVariants,
#         "productCategories" : productCategories,
#         "productUnits" : productUnits,
#         "productVariantForm": productVariantForm,
#         "productCategoryForm": productCategoryForm,
#         "productUnitsForm": productUnitsForm}
    
#     if request.method == "POST":
#         form_prefix = request.POST.get('form_prefix')
#         # print(form_prefix)
 
#         if form_prefix == 'productVariantForm':
#             productVariantForm_data = ProductVariantForm(request.POST or None,prefix="productVariantForm")
#             if productVariantForm_data.is_valid():
#                 product_variant = productVariantForm_data.save(commit=False)
#                 product_variant.name = product_variant.name.capitalize()
#                 product_variant.company = company
#                 product_variant.save()
#                 return JsonResponse({'success': True, 'name': product_variant.name})
#             else:
#                 return JsonResponse({'success': False, 'errors': productVariantForm_data.errors})
        
#         if form_prefix == 'productCategoryForm':
#             productCategoryForm_data = ProductCategoryForm(request.POST or None,prefix="productCategoryForm")
#             if productCategoryForm_data.is_valid():
#                 product_category = productCategoryForm_data.save(commit=False)
#                 product_category.name = product_category.name.capitalize()
#                 product_category.company = company
#                 product_category.save()
#                 return JsonResponse({'success': True, 'name': product_category.name})
#             else:
#                 return JsonResponse({'success': False, 'errors': productCategoryForm_data.errors})
        
#         if form_prefix == 'productUnitsForm':
#             productUnitsForm_data = ProductUnitsForm(request.POST or None,prefix="productUnitsForm")
#             if productUnitsForm_data.is_valid():
#                 product_unit = productUnitsForm_data.save(commit=False)
#                 product_unit.name = product_unit.name.lower()
#                 product_unit.company = company
#                 product_unit.save()
#                 return JsonResponse({'success': True, 'name': product_unit.name})
#             else:
#                 return JsonResponse({'success': False, 'errors': productUnitsForm_data.errors})
        
#         return JsonResponse({'success': False, 'errors': {"name": "Form Prefix"}})

#     return render(request, 'stock/settings/index.html', context=context)       


# def stock_index(request):
#     company_id = request.session.get('company_id', None)
#     company = None
#     if company_id is not None:
#         company = Company.objects.get(pk=company_id)
#     elif request.user.company:
#         company = request.user.company

#     form = ProductForm()

#     context = {
#         "company" :company,
#         "form": form}

#     if request.method == "POST":
#         form_data = ProductForm(request.POST, request.FILES)
#         if form_data.is_valid():
#             product = form_data.save(commit=False)
#             product.name = product.name.capitalize()
#             product.save()
#             return JsonResponse({'success': True, 'name': product.name})
#         else:
#             return JsonResponse({'success': False, 'errors': form_data.errors})

#     return render(request, 'stock/index.html', context=context)       


# def stock_new(request):
#     context = {}
#     form = ReceivedStockForm()
#     ReceivedStockItemFormSet = formset_factory(ReceivedStockItemForm, extra=1)
#     formset = ReceivedStockItemFormSet(prefix='items')

#     if request.method == "POST":
#         form_data = ReceivedStockForm(request.POST)
#         formset_data = ReceivedStockItemFormSet(request.POST, prefix='items')

#         print(form_data)
#         print(formset_data)

#         if form_data.is_valid() and formset_data.is_valid():
#             received_stock = form_data.save(commit=False)
#             received_stock.company = None
#             received_stock.branch = None
#             received_stock.created_by = None
#             # received_stock.save()

#             for formset_data_item in formset_data:
#                 item = formset_data_item.save(commit=False)
#                 item.received_stock = received_stock
#                 item.company = None
#                 item.branch = None
#                 item.created_by = None
#                 # item.save()

#             context['success_message'] = 'Stock added successfully'
#         else:
#             context['form'] = form_data
#             context['formset'] = formset_data
#             return render(request, 'stock/index.html', context=context)
    
#     context['form'] = form  
#     context['formset'] = formset  
#     return render(request, 'stock/new/index.html', context=context)       
        
                    
