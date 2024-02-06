from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.http import JsonResponse
from .forms import RequiredFormSet
from .forms import ProductCategoryForm, ProductVariantForm
from .forms import ProductUnitsForm, SupplierForm
from .forms import StockItemForm, ReceivedStockForm,ReceivedStockItemForm
from .forms import StockRequestForm, StockRequestItemForm
from .models import ProductVariant, ProductCategory, ProductUnits, StockItem
from .models import ReceivedStock, ReceivedStockItem
from .models import StockRequest, StockRequestItem
from .mixins import CompanyMixin, CompanyFormMixin
from company.models import Company, Store, SupplierEntity

@login_required(login_url='/login')
def product_categories_list(request,store_id = None, company_id = None):
    form = ProductCategoryForm()
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

    results = ProductCategory.objects.filter(store = store)
    context["results"] = results

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
                category.store = store
                category.save()
                return JsonResponse({'success': True, 'category_id': category.id})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
            
    return render(request, 'categories/index.html', context=context) 


@login_required(login_url='/login')
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

    results = ProductVariant.objects.filter(store = store)
    context["results"] = results

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
                variant.store = store
                variant.save()
                return JsonResponse({'success': True, 'variant_id': variant.id})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
            
    return render(request, 'settings/variants/index.html', context=context) 


@login_required(login_url='/login')
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

    results = ProductUnits.objects.filter(store = store)
    context["results"] = results

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
                unit.store = store
                unit.save()
                return JsonResponse({'success': True, 'unit_id': unit.id})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
            
    return render(request, 'settings/units/index.html', context=context) 


@login_required(login_url='/login')
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

    results = SupplierEntity.objects.filter(store = store)
    context["results"] = results


    if request.is_ajax():
        if request.method == "POST":
            form = SupplierForm(request.POST)
            if form.is_valid():
                supplier = form.save(commit=False)
                if SupplierEntity.objects.filter(name = supplier.name.capitalize(), store = store).exists():
                    form.errors['name'] = ["Name ALready Exists!"]
                    return JsonResponse({'success': False, 'errors': form.errors})
                supplier.name = supplier.name.capitalize()
                supplier.store = store
                supplier.save()
                return JsonResponse({'success': True, 'supplier_id': supplier.id})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
            
    
    return render(request, 'suppliers/index.html', context=context) 


@login_required(login_url='/login')
def company_products_list(request, company_id):
    company = Company.objects.get(pk = company_id)
    results = StockItem.objects.filter(company = company)

    context = { "company": company, "results" : results }

    return render(request, 'products/list/index.html', context=context) 


@login_required(login_url='/login')
def stock_items_list(request, store_id):
    store = Store.objects.get(pk=store_id)
    company = store.company
    results = StockItem.objects.filter(store=store)

    context = { 
        "company": company,
        "store": store,
        "results" : results
        }

    return render(request, 'products/list/index.html', context=context) 

 
@login_required(login_url='/login')
def stock_items_detail(request, store_id, stock_item_id):
    store = Store.objects.get(pk=store_id)
    company = store.company
    product = StockItem.objects.get(pk = stock_item_id)

    context = { "company": company, "store": store, "product" : product }

    return render(request, 'products/detail/index.html', context=context) 


@login_required(login_url='/login')
def stock_items_new(request, store_id):
    company = None
    store = None

    if store_id is not None:
        store = Store.objects.get(pk=store_id)
        company = store.company


    form = StockItemForm(company=company)
    context = {
        "company": company,
        "store": store,
        "form" : form }

    if request.method == "POST":
        form = StockItemForm(request.POST, request.FILES, company=company)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            category = form.cleaned_data.get("category")
            variant = form.cleaned_data.get("variant")
            units = form.cleaned_data.get("units")
            item_photo = form.cleaned_data.get("item_photo", None)
            unit_price = form.cleaned_data.get("unit_price")
            reorder_min_qty = form.cleaned_data.get("reorder_min_qty")
            is_for_sale = form.cleaned_data.get("is_for_sale", True)
            is_consummable = form.cleaned_data.get("is_consummable", False)

            stock_item = StockItem(
                name = name, 
                description = description,
                category = category,
                variant = variant,
                units = units,
                item_photo = item_photo,
                unit_price = unit_price,
                reorder_min_qty = reorder_min_qty,
                is_for_sale = is_for_sale,
                is_consummable = is_consummable
            )

            stock_item.company = company
            stock_item.store = store
            stock_item.created_by = request.user
            stock_item.save()

            return redirect('inventory:store-products-list', store_id=store_id)
        else:
            context["form"] = form

    return render(request, 'products/new/index.html', context=context) 


@login_required(login_url='/login') 
def stock_items_edit(request, store_id, stock_item_id):
    company = None
    store = None
    if store_id is not None:
        store = Store.objects.get(pk=store_id)
        company = store.company

    product = StockItem.objects.get(pk = stock_item_id)

    form = StockItemForm(instance=product, company=company)

    context = { 
        "company": company,
        "store": store,
        "form" : form,
        "product": product
        }

    if request.method == "POST":
        form = StockItemForm(request.POST, request.FILES, instance=product)
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

            product.name = name
            product.description = description
            product.category = category
            product.variant = variant
            product.units = units
            product.item_photo = item_photo
            product.unit_price = unit_price
            product.reorder_min_qty = reorder_min_qty
            product.is_for_sale = is_for_sale
            product.is_consummable = is_consummable
            product.company = company
            product.store = store
            product.created_by = request.user
            product.save()

            return redirect('inventory:store-products-list', store_id=store_id)
        else:
            context["form"] = form

    return render(request, 'products/edit/index.html', context=context) 


@login_required(login_url='/login')
def stock_items_delete(request, store_id, stock_item_id):
    store = Store.objects.get(pk=store_id)
    company = store.company
    product = StockItem.objects.get(pk = stock_item_id)

    product.hard_delete()
    return redirect(reverse('inventory:store-products-list', kwargs={'store_id': store_id}))


@login_required(login_url='/login')
def company_received_stock_list(request, company_id):
    company = Company.objects.get(pk=company_id)

    results = ReceivedStock.objects.filter(company = company)
    context = {
        "company": company,
        "results" : results
        }

    return render(request, 'received_stock/list/index.html', context=context) 


@login_required(login_url='/login')
def store_received_stock_list(request, store_id):
    store = Store.objects.get(pk=store_id)
    company = store.company

    results = ReceivedStock.objects.filter(store = store)
    context = {
        "company": company,
        "store": store,
        "results": results
        }

    return render(request, 'received_stock/list/index.html', context=context) 


@login_required(login_url='/login')
def store_received_stock_detail(request, store_id, received_stock_id):
    store = Store.objects.get(pk=store_id)
    company = store.company

    received_stock = ReceivedStock.objects.get(pk = received_stock_id)
    context = { "company": company,"store": store, "received_stock": received_stock }

    return render(request, 'received_stock/detail/index.html', context=context) 


@login_required(login_url='/login')
def store_received_stock_new(request, store_id):
    store = Store.objects.get(pk=store_id)
    company = store.company

    context = {
        "company": company,
        "store": store}

    form = ReceivedStockForm(company=company, store=store)
    
    # ReceivedStockItemFormSet = formset_factory(ReceivedStockItemForm, extra=1, validate_min=True)
    ReceivedStockItemFormSet = formset_factory(ReceivedStockItemForm, formset=RequiredFormSet, extra=1, validate_min=True)

    formset = ReceivedStockItemFormSet(prefix='items', form_kwargs={'store': store})

    if request.method == "POST":
        form_data = ReceivedStockForm(request.POST,company=company, store=store)
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

                quantity = formset_data_item.cleaned_data.get("quantity")
                stock_item = item.stock_item
                stock_item.available_qty +=  quantity
                stock_item.save()

            context['success_message'] = 'Stock added successfully'
            return redirect('inventory:store-received-stock-list', store_id=store_id)
        else:
            context['form'] = form_data
            context['formset'] = formset_data
            return render(request, 'received_stock/new/index.html', context=context)
    
    context['form'] = form  
    context['formset'] = formset  
    return render(request, 'received_stock/new/index.html', context=context) 


@login_required(login_url='/login')
def store_received_stock_edit(request, store_id, received_stock_id):
    store = get_object_or_404(Store, pk=store_id)
    company = store.company

    received_stock = get_object_or_404(ReceivedStock, pk=received_stock_id, store=store)

    context = {
        "company": company,
        "store": store,
        "received_stock": received_stock,
    }

    form = ReceivedStockForm(instance = received_stock, company=company, store=store)

    ReceivedStockItemFormSet = modelformset_factory(ReceivedStockItem, form=ReceivedStockItemForm, extra=0)
    qs = received_stock.receivedstockitem_set.all()
    formset = ReceivedStockItemFormSet(prefix='items',queryset=qs, form_kwargs={'store': store})

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
                    quantity = formset_data_item.cleaned_data.get("quantity")
                    stock_item = item.stock_item
                    stock_item.available_qty += quantity
                    stock_item.save()
                else:
                    print("Old")
                    item.save()
                    # Update store product quantities
                    quantity = formset_data_item.cleaned_data.get("quantity")
                    stock_item = item.stock_item
                    stock_item.available_qty -= stock_item.available_qty
                    stock_item.available_qty += quantity
                    stock_item.save()

            context['success_message'] = 'Stock edited successfully'
            return redirect('inventory:received-stock-list', store_id=store_id)
        else:
            context['form'] = form_data
            context['formset'] = formset_data
            return render(request, 'received_stock/edit/index.html', context=context)

    
    context['form'] = form
    context['formset'] = formset
    return render(request, 'received_stock/edit/index.html', context=context)


@login_required(login_url='/login')
def store_received_stock_approve(request, store_id, received_stock_id):
    store = get_object_or_404(Store, pk=store_id)

    received_stock = get_object_or_404(ReceivedStock, pk=received_stock_id, store=store)

    if received_stock.status == "PENDING":
        print("APPROVED")
        received_stock.status = "APPROVED"
        received_stock.save()
    
        qs = received_stock.receivedstockitem_set.all()

        for item in qs:
            stock_item = item.stock_item
            new_actual_qty = item.stock_item.available_qty + item.stock_item.actual_qty
            stock_item.actual_qty = new_actual_qty
            stock_item.save()
    
    return redirect('inventory:store-received-stock-list', store_id=store_id)
    

@login_required(login_url='/login')
def company_stock_requests_list(request, company_id):
    company = Company.objects.get(pk=company_id)

    items = StockRequest.objects.filter(company = company)
    context = { "company": company,"items": items }

    return render(request, 'stock_requests/list/index.html', context=context) 


@login_required(login_url='/login')
def store_stock_requests_list(request, store_id):
    store = Store.objects.get(pk=store_id)
    company = store.company

    results = StockRequest.objects.filter(store = store)
    context = {
        "company": company,
        "store": store,
        "results": results
        }

    return render(request, 'stock_requests/list/index.html', context=context) 


@login_required(login_url='/login')
def store_stock_requests_detail(request, store_id, stock_request_id):
    store = Store.objects.get(pk=store_id)
    company = store.company

    stock_request = StockRequest.objects.get(pk = stock_request_id)

    context = { "company": company, "store": store, "stock_request": stock_request }

    return render(request, 'stock_requests/detail/index.html', context=context) 


@login_required(login_url='/login')
def store_stock_requests_new(request, store_id):
    store = Store.objects.get(pk=store_id)
    company = store.company

    context = {
        "company": company,
        "store": store}

    form = StockRequestForm() 
    
    StockRequestItemFormSet = formset_factory(StockRequestItemForm, formset=RequiredFormSet, extra=1, validate_min=True)

    formset = StockRequestItemFormSet(prefix='items')

    if request.method == "POST":  
        form_data = StockRequestForm(request.POST)
        formset_data = StockRequestItemFormSet(request.POST, prefix='items')

        if form_data.is_valid() and formset_data.is_valid():            
            stock_request = StockRequest(
                request_date = form_data.cleaned_data.get("request_date"),
                delivery_date = form_data.cleaned_data.get("delivery_date"),
                request_notes = form_data.cleaned_data.get("request_notes"),
            )
            
            stock_request.company = company
            stock_request.store = store
            stock_request.created_by = request.user
            stock_request.save()

            for formset_data_item in formset_data:
                item = formset_data_item.save(commit=False)
                item.stock_request = stock_request
                item.company = company
                item.store = store
                item.created_by = request.user
                item.save() 

                stock_item = item.stock_item
                item.available_quantity = stock_item.available_qty
                item.save() 

            context['success_message'] = 'Stock Request added successfully'
            return redirect('inventory:store-stock-requests-list', store_id=store_id)
        else:
            context['form'] = form_data
            context['formset'] = formset_data
            return render(request, 'stock_requests/new/index.html', context=context)
    
    context['form'] = form  
    context['formset'] = formset  
    return render(request, 'stock_requests/new/index.html', context=context) 


@login_required(login_url='/login')
def store_stock_requests_edit(request, store_id, stock_request_id):
    store = get_object_or_404(Store, pk=store_id)
    company = store.company

    stock_request = get_object_or_404(StockRequest, pk=stock_request_id, store=store)

    context = {
        "company": company,
        "store": store,
        "stock_request": stock_request,
    }

    form = StockRequestForm(instance = stock_request)

    StockRequestItemFormSet = modelformset_factory(StockRequestItem, form=StockRequestItemForm, extra=0)
    qs = stock_request.receivedstockitem_set.all()
    formset = StockRequestItemFormSet(prefix='items',queryset=qs)

    if request.method == "POST":
        form_data = StockRequestForm(request.POST, instance=stock_request)
        formset_data = StockRequestItemFormSet(request.POST, prefix='items', queryset=qs)

        if form_data.is_valid() and formset_data.is_valid():
            # Update the received stock details
            form_data.save()

            # Update each item in the formset
            for formset_data_item in formset_data:
                item = formset_data_item.save(commit=False)
                if item.id is None:
                    print("New")
                    item.stock_request = stock_request
                    item.company = company
                    item.store = store
                    item.created_by = request.user
                    item.save() # Save Instance
                else:
                    print("Old")
                    item.save() # Update Instance

            context['success_message'] = 'Stock Request edited successfully'
            return redirect('inventory:stock-requests-list', store_id=store_id)
        else:
            context['form'] = form_data
            context['formset'] = formset_data
            return render(request, 'stock_requests/edit/index.html', context=context)

    
    context['form'] = form
    context['formset'] = formset
    return render(request, 'stock_requests/edit/index.html', context=context)




