from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import RequiredFormSet
from .forms import SaleForm,PosSaleForm
from .forms import SaleItemForm
from company.models import Company, Store, PosCenter, Client
from inventory.models import StockItem
from .models import Sale
from .models import SaleItem


@login_required(login_url='/login')
def company_sales_list(request, company_id):
    company = Company.objects.get(pk=company_id)

    sales = Sale.objects.filter(company = company)
    context = {
            "company": company,
            "sales": sales
        }

    return render(request, 'sales/company/list/index.html', context=context) 


@login_required(login_url='/login')
def store_sales_list(request, store_id):
    store = Store.objects.get(pk=store_id)
    company = store.company

    sales = Sale.objects.filter(store = store)
    context = {
            "company": company,
            "store": store,
            "sales": sales
        }

    return render(request, 'sales/store/list/index.html', context=context) 


@login_required(login_url='/login')
def store_sales_detail(request, store_id, sale_id):
    store = Store.objects.get(pk=store_id)
    company = store.company

    sale = Sale.objects.get(pk = sale_id)
    context = {
            "company": company,
            "store": store,
            "sale": sale
        }

    return render(request, 'sales/store/detail/index.html', context=context) 


# @login_required(login_url='/login')
def store_sales_invoice(request, store_id, sale_id):
    store = Store.objects.get(pk=store_id)
    company = store.company

    sale = Sale.objects.get(pk = sale_id)

    context = { 
        "company": company,
        "store": store,
        "title": "Sale Invoice",
        "sale": sale
        } 

    print("Before Generating....")
    sale = sale.generate_invoice( context = context)
    print("After Generating....")
    
    # Prepare the sale data to be returned as JSON
    sale_data = {
        "sale_id": sale.id,
        "invoice_url" : request.build_absolute_uri(sale.invoice_file.url) if sale.invoice_file else None,

    }

    return JsonResponse(sale_data)


@login_required(login_url='/login')
def store_sales_new(request, store_id):
    store = Store.objects.get(pk=store_id)
    company = store.company
    products = StockItem.objects.filter(store = store)

    context = { "company": company, "store": store, "products": products }
 
    form = SaleForm(user=request.user, store= store)
    
    TestSaleItemFormset = formset_factory(SaleItemForm, formset=RequiredFormSet)
    test_formset = TestSaleItemFormset(prefix='test_items')
    # print(test_formset)

    SaleItemFormset = formset_factory(SaleItemForm, formset=RequiredFormSet, extra=0, validate_min=True)

    formset = SaleItemFormset(prefix='items')

    if request.is_ajax():
        if request.method == "POST":
            form_data = SaleForm(request.POST, user=request.user, store= store)
            formset_data = SaleItemFormset(request.POST, prefix='items')

            if form_data.is_valid() and formset_data.is_valid():
                customer_name = form_data.cleaned_data.get("customer_name", None)
                customer_email = form_data.cleaned_data.get("customer_email", None)
                customer_phone = form_data.cleaned_data.get("customer_phone", None)
                customer_address = form_data.cleaned_data.get("customer_address", None)

                customer = None
                if customer_name is not None and customer_name != "":
                    if customer_phone is not None and customer_phone != "":
                        customer, _ = Client.objects.get_or_create(
                            name=customer_name, email=customer_email,
                            phone=customer_phone, address=customer_address,
                            store=store )
                
                sale = Sale(
                    customer = customer,
                    payment_option = form_data.cleaned_data.get("payment_option"),
                    payment_period = form_data.cleaned_data.get("payment_period"),
                    remarks = form_data.cleaned_data.get("remarks"))

                pos_data =form_data.cleaned_data.get("pos_center")
                pos_center = PosCenter.objects.get(id = pos_data.id)

                sale.pos_center = pos_center
                sale.company = company
                sale.store = store 
                sale.created_by = request.user
                sale.save()

                if form_data.cleaned_data.get("payment_period") == "INSTANT":
                    payment_status = "CURRENT"
                    sale.payment_status = payment_status
                    sale.save()

                for formset_data_item in formset_data:
                    item = formset_data_item.save(commit=False)
                    item.sale = sale

                    item.total_cost = item.stock_item.unit_price * item.quantity
                    item.unit_cost = item.stock_item.unit_price
                    item.company = company
                    item.store = store
                    item.pos_center = pos_center
                    item.created_by = request.user
                    item.save() 
                 
                    stock_item = item.stock_item
                    new_available_qty = stock_item.available_qty - item.quantity
                    new_actual_qty = stock_item.actual_qty - item.quantity
                    stock_item.available_qty = new_available_qty
                    stock_item.actual_qty = new_actual_qty

                    stock_item.save() 
                return JsonResponse({'success': True})
            else:
                print(form_data.errors)
                print(formset_data.errors)
                return JsonResponse({'failure': False})
    
    context['form'] = form  
    context['formset'] = formset  
    context['empty_form'] = test_formset.forms[0]  
    return render(request, 'sales/store/new/index.html', context=context) 


@login_required(login_url='/login')
def store_sales_edit(request, store_id, sale_id):
    store = get_object_or_404(Store, pk=store_id)
    company = store.company

    sale = get_object_or_404(Sale, pk=sale_id, store=store)

    context = {
        "company": company,
        "store": store,
        "sale": sale,
    }

    form = SaleForm(instance=sale, user=request.user, store= store)

    SaleItemFormset = modelformset_factory(SaleItem, form=SaleItemForm, extra=0)
    qs = sale.receivedstockitem_set.all()

    formset = SaleItemFormset(prefix='items',queryset=qs)

    if request.method == "POST":
        form_data = SaleForm(request.POST, instance=sale, user=request.user, store= store)
        formset_data = SaleItemFormset(request.POST, prefix='items', queryset=qs)

        if form_data.is_valid() and formset_data.is_valid():
            # Update the received stock details
            form_data.save()

            # Update each item in the formset
            for formset_data_item in formset_data:
                item = formset_data_item.save(commit=False)
                if item.id is None:
                    print("New")
                    item.sale = sale
                    item.company = company
                    item.store = store
                    item.created_by = request.user
                    item.save() # Save Instance
                else:
                    print("Old")
                    item.save() #  Update Instance

            context['success_message'] = 'Sale edited successfully'
            return redirect('sales:sales-list', store_id=store_id)
        else:
            context['form'] = form_data
            context['formset'] = formset_data
            return render(request, 'sales/edit/index.html', context=context)

    context['form'] = form
    context['formset'] = formset
    return render(request, 'sales/store/edit/index.html', context=context)


@login_required(login_url='/login')
def pos_sales_list(request, pos_id):
    pos = get_object_or_404(PosCenter, pk=pos_id)
    store = pos.store
    company = store.company

    sales = Sale.objects.filter(pos_center = pos)
    context = { "company": company, "store": store, "pos": pos, "sales": sales }

    return render(request, 'sales/pos/list/index.html', context=context) 


@login_required(login_url='/login')
def pos_sales_new(request, pos_id):
    pos_center = get_object_or_404(PosCenter, pk=pos_id)
    store = pos_center.store
    company = store.company

    products = StockItem.objects.filter(store = store)

    context = { "company": company, "store": store, "pos": pos_center, "products": products }
 
    form = PosSaleForm()
    
    TestSaleItemFormset = formset_factory(SaleItemForm, formset=RequiredFormSet)
    test_formset = TestSaleItemFormset(prefix='test_items')

    SaleItemFormset = formset_factory(SaleItemForm, formset=RequiredFormSet, extra=0, validate_min=True)

    formset = SaleItemFormset(prefix='items')

    if request.is_ajax():
        if request.method == "POST":
            form_data = PosSaleForm(request.POST)
            formset_data = SaleItemFormset(request.POST, prefix='items')
            
            if form_data.is_valid() and formset_data.is_valid():
                customer_name = form_data.cleaned_data.get("customer_name", None)
                customer_email = form_data.cleaned_data.get("customer_email", None)
                customer_phone = form_data.cleaned_data.get("customer_phone", None)
                customer_address = form_data.cleaned_data.get("customer_address", None)
            
                customer = None
                if customer_name is not None and customer_name != "":
                    if customer_phone is not None and customer_phone != "":
                        customer, _ = Client.objects.get_or_create(
                            name=customer_name, email=customer_email,
                            phone=customer_phone, address=customer_address,
                            store=store
                        )
                
                sale = Sale(
                    customer = customer,
                    payment_option = form_data.cleaned_data.get("payment_option"),
                    payment_period = form_data.cleaned_data.get("payment_period"),
                    remarks = form_data.cleaned_data.get("remarks"))
                
                sale.company = company
                sale.store = store 
                sale.pos_center = pos_center
                sale.created_by = request.user
                sale.save()

                if form_data.cleaned_data.get("payment_period") == "INSTANT":
                    payment_status = "CURRENT"
                    sale.payment_status = payment_status
                    sale.save()

                for formset_data_item in formset_data:
                    item = formset_data_item.save(commit=False)
                    item.sale = sale

                    item.total_cost = item.stock_item.unit_price * item.quantity
                    item.unit_cost = item.stock_item.unit_price
                    item.company = company
                    item.store = store
                    item.pos_center = pos_center
                    item.created_by = request.user
                    item.save() 
                 
                    stock_item = item.stock_item
                    new_available_qty = stock_item.available_qty - item.quantity
                    new_actual_qty = stock_item.actual_qty - item.quantity
                    stock_item.available_qty = new_available_qty
                    stock_item.actual_qty = new_actual_qty

                    stock_item.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'failure': False})
    
    context['form'] = form  
    context['formset'] = formset  
    context['empty_form'] = test_formset.forms[0]  
    return render(request, 'sales/pos/new/index.html', context=context) 