from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.http import JsonResponse
from .forms import RequiredFormSet
from .forms import CategoryForm, VariantForm
from .forms import UnitsForm, SupplierEntityForm
from .forms import StockItemNewForm, StockItemEditForm, ReceivedStockForm,ReceivedStockItemForm
from .forms import StockRequestForm, StockRequestItemForm
from .models import Variant, Category, Units, StockItem
from .models import ReceivedStock, ReceivedStockItem
from .models import StockRequest, StockRequestItem
from company.models import Company, Store, PosCenter, SupplierEntity

@login_required(login_url='/login')
def suppliers_list(request, store_id = None, company_id = None):
    form = SupplierEntityForm()

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
            form = SupplierEntityForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get("name")
                if SupplierEntity.objects.filter(name = name, store = store).exists():
                    form.errors['name'] = ["Name ALready Exists!"]
                    return JsonResponse({'success': False, 'errors': form.errors})
        
                supplier = form.save(commit=False)
                supplier.store = store
                supplier.save()
                return JsonResponse({'success': True, 'supplier_id': supplier.id})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
            
    
    return render(request, 'suppliers/index.html', context=context) 


@login_required(login_url='/login')
def store_product_categories_list_view(request, store_id = None, company_id = None):
    form = CategoryForm()
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

    results = Category.objects.filter(store = store)
    context["results"] = results

    if request.is_ajax():
        if request.method == "POST":
            form = CategoryForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get("name")
                if Category.objects.filter(name__iexact = name, store = store).exists():
                    form.errors['name'] = ["Name ALready Exists!"]
                    return JsonResponse({'success': False, 'errors': form.errors})
        
                category = form.save(commit=False)
                category.company = company
                category.store = store
                category.save()
                return JsonResponse({'success': True, 'category_id': category.id})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
            
    return render(request, 'settings/categories/index.html', context=context) 


@login_required(login_url='/login')
def pos_product_categories_list_view(request, pos_id):
    pos = PosCenter.objects.get(pk = pos_id)

    store = pos.store

    company = store.company

    results = Category.objects.filter(store = store)

    context = { "company" : company, "store": store, "pos": pos, "results": results}
            
    return render(request, 'settings/categories/pos/index.html', context=context) 


@login_required(login_url='/login')
def store_product_variants_list_view(request,store_id = None, company_id = None):
    form = VariantForm()
    context = { "form" : form }

    store = None
    company = None
    if store_id is not None:
        store = Store.objects.get(pk=store_id)
        company = store.company
        context["store"] = store
        context["company"] = company
    elif company_id is not None:
        company = Company.objects.get(pk=company_id)
        context["company"] = company

    results = Variant.objects.filter(store = store)
    context["results"] = results

    if request.is_ajax():
        if request.method == "POST":
            form = VariantForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get("name")
                if Variant.objects.filter(name__iexact = name, store = store).exists():
                    form.errors['name'] = ["Name ALready Exists!"]
                    return JsonResponse({'success': False, 'errors': form.errors})
                
                variant = form.save(commit=False)
                variant.company = company
                variant.store = store
                variant.save()
                return JsonResponse({'success': True, 'variant_id': variant.id})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
            
    return render(request, 'settings/variants/index.html', context=context) 


@login_required(login_url='/login')
def pos_product_variants_list_view(request, pos_id):
    pos = PosCenter.objects.get(pk = pos_id)

    store = pos.store

    company = store.company

    results = Variant.objects.filter(store = store)

    context = { "company" : company, "store": store, "pos": pos, "results": results}

    return render(request, 'settings/variants/pos/index.html', context=context) 


@login_required(login_url='/login')
def store_product_units_list_view(request,store_id = None, company_id = None):
    form = UnitsForm()
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

    results = Units.objects.filter(store = store)
    context["results"] = results

    if request.is_ajax():
        if request.method == "POST":
            form = UnitsForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get("name")
                if Units.objects.filter(name__iexact = name, store = store).exists():
                    form.errors['name'] = ["Name ALready Exists!"]
                    return JsonResponse({'success': False, 'errors': form.errors})
            
                units = form.save(commit=False)
                units.company = company
                units.store = store
                units.save()
                return JsonResponse({'success': True, 'unit_id': units.id})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
            
    return render(request, 'settings/units/index.html', context=context) 


@login_required(login_url='/login')
def pos_product_units_list_view(request, pos_id):
    pos = PosCenter.objects.get(pk = pos_id)

    store = pos.store

    company = store.company

    results = Units.objects.filter(store = store)

    context = { "company" : company, "store": store, "pos": pos, "results": results}

    return render(request, 'settings/units/pos/index.html', context=context) 


@login_required(login_url='/login')
def store_stock_items_list_view(request, store_id):
    store = Store.objects.get(pk=store_id)
    company = store.company
    results = StockItem.objects.filter(store=store)

    context = { 
        "company": company,
        "store": store,
        "results" : results}

    return render(request, 'products/list/index.html', context=context) 


@login_required(login_url='/login')
def pos_stock_items_list_view(request, pos_id):
    pos = PosCenter.objects.get(pk=pos_id)
    store = pos.store
    company = store.company
    results = StockItem.objects.filter(store=store)

    context = { "company" : company, "store": store, "pos": pos, "results": results}

    return render(request, 'products/list/pos/index.html', context=context) 


@login_required(login_url='/login')
def company_stock_items_list_view(request, company_id):
    company = Company.objects.get(pk = company_id)
    results = StockItem.objects.filter(company = company)

    context = { "company": company, "results" : results }

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


    form = StockItemNewForm(store=store)
    context = {
        "company": company,
        "store": store,
        "form" : form }

    if request.method == "POST":
        form = StockItemNewForm(request.POST, request.FILES, store=store)
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

    product = get_object_or_404(StockItem, pk=stock_item_id)

    form = StockItemEditForm(instance=product, store=store)

    context = { 
        "company": company,
        "store": store,
        "form" : form,
        "product": product
        }

    if request.method == "POST":
        form = StockItemEditForm(request.POST, request.FILES, instance=product, store=store)
        
        if form.is_valid():
            # name = form.cleaned_data.get("name")
            # category = form.cleaned_data.get("category")
            # variant = form.cleaned_data.get("variant")
            # units = form.cleaned_data.get("units")
            # description = form.cleaned_data.get("description")
            # item_photo = form.cleaned_data.get("item_photo", None)
            # unit_price = form.cleaned_data.get("unit_price")
            # reorder_min_qty = form.cleaned_data.get("reorder_min_qty")
            # is_for_sale = form.cleaned_data.get("is_for_sale", True)
            # is_consummable = form.cleaned_data.get("is_consummable", False)

            item_photo_clear = form.cleaned_data.get("item_photo_clear", False)
            if item_photo_clear == True:
                product.item_photo.delete()
                product.item_photo = None
                product.save()

            stock_item = form.save(commit=False)

            if 'item_photo' in request.FILES: # Update the Image
                stock_item.item_photo = request.FILES['item_photo']
            
            stock_item.save()
            return redirect(reverse('inventory:store-products-detail', kwargs={'store_id': store_id, "stock_item_id": stock_item_id}))

            # product.name = name
            # product.description = description
            # product.category = category
            # product.variant = variant
            # product.units = units
            # product.item_photo = item_photo
            # product.unit_price = unit_price
            # product.reorder_min_qty = reorder_min_qty
            # product.is_for_sale = is_for_sale
            # product.is_consummable = is_consummable
            # product.company = company
            # product.store = store
            # product.created_by = request.user
            # product.save()

            # return redirect('inventory:store-products-list', store_id=store_id)
        else:
            print(form.errors)
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

    form = ReceivedStockForm(company=company,store=store)
    
    ReceivedStockItemFormSet = formset_factory(ReceivedStockItemForm, formset=RequiredFormSet, extra=1, validate_min=True)

    formset = ReceivedStockItemFormSet(prefix='items', form_kwargs={'store': store})

    if request.method == "POST":
        form_data = ReceivedStockForm(request.POST, company=company, store=store)
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
        form_data = ReceivedStockForm(request.POST, instance=received_stock, company=company, store=store)
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
def store_received_stock_cancel(request, store_id, received_stock_id):
    store = get_object_or_404(Store, pk=store_id)

    received_stock = get_object_or_404(ReceivedStock, pk=received_stock_id, store=store)

    if received_stock.status == "PENDING":
        received_stock.status = "CANCELLED"
        received_stock.save()
    
        qs = received_stock.receivedstockitem_set.all()

        for item in qs:
            stock_item = item.stock_item
            new_actual_qty = item.stock_item.available_qty + item.stock_item.actual_qty
            stock_item.actual_qty = new_actual_qty
            stock_item.save()
    
    return redirect('inventory:store-received-stock-list', store_id=store_id)
    
   
@login_required(login_url='/login')
def store_received_stock_delete(request, store_id, received_stock_id):
    store = get_object_or_404(Store, pk=store_id)

    received_stock = get_object_or_404(ReceivedStock, pk=received_stock_id, store=store)

    if received_stock.status != "APPROVED":
        received_stock.hard_delete()
    
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




