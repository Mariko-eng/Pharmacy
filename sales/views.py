from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404
from django.forms import ValidationError
from .forms import RequiredFormSet
from .forms import SaleForm
from .forms import SaleItemForm
from company.models import Store, Customer
from inventory.models import StoreProduct
from .models import Sale
from .models import SaleItem


def store_sales_list(request, store_id):
    store = Store.objects.get(pk=store_id)
    company = store.company

    sales = Sale.objects.filter(store = store)
    context = {
        "company": company,
        "store": store,
        "sales": sales
        }

    return render(request, 'sales/list/index.html', context=context) 


def store_sales_new(request, store_id):
    store = Store.objects.get(pk=store_id)
    company = store.company
    store_products = StoreProduct.objects.filter(store = store)

    context = {
        "company": company,
        "store": store,
        "store_products": store_products
        }

    form = SaleForm(user=request.user, store= store)
    
    TestSaleItemFormset = formset_factory(SaleItemForm, formset=RequiredFormSet)
    test_formset = TestSaleItemFormset(prefix='test_items')

    SaleItemFormset = formset_factory(SaleItemForm, formset=RequiredFormSet, extra=0, validate_min=True)

    formset = SaleItemFormset(prefix='items')

    # empty_form_set_json = formset.management_form

    # print(empty_form_set_json)
    # print(formset.forms[0])

    if request.method == "POST":
        form_data = SaleForm(request.POST, user=request.user, store= store)

        formset_data = SaleItemFormset(request.POST, prefix='items')

        if form_data.is_valid() and formset_data.is_valid():
            customer_name = form_data.cleaned_data.get("customer_name", None)
            customer_email = form_data.cleaned_data.get("customer_email", None)
            customer_phone = form_data.cleaned_data.get("customer_phone", None)
            customer_address = form_data.cleaned_data.get("customer_address", None)

            customer = None

            if customer_name is not None or customer_name != "":
                if customer_phone is not None or customer_phone != "":
                    if  Customer.objects.filter(
                            name = customer_name, email = customer_email,
                            phone = customer_phone, address = customer_address).exists():
                        customer = Customer.objects.filter(
                            name = customer_name, email = customer_email,
                            phone = customer_phone, address = customer_address).first()
                    else:
                        customer = Customer.objects.create(
                            name = customer_name, email = customer_email,
                            phone = customer_phone, address = customer_address)
            
            sale = Sale(
                customer = customer,
                payment_option = form_data.cleaned_data.get("payment_option"),
                payment_details = form_data.cleaned_data.get("payment_details"),
                sale_date = form_data.cleaned_data.get("sale_date"),
                sale_remarks = form_data.cleaned_data.get("sale_remarks"),
            )

            sale.pos_center = form_data.cleaned_data.get("pos_center"),
            sale.company = company
            sale.store = store
            sale.created_by = request.user
            sale.save()

            for formset_data_item in formset_data:
                item = formset_data_item.save(commit=False)
                item.sale = sale
                item.company = company
                item.store = store
                item.created_by = request.user
                item.save() 

            context['success_message'] = 'Sale added successfully'
            return redirect('sales:sales-list', store_id=store_id)
        else:
            context['form'] = form_data
            context['formset'] = formset_data
            return render(request, 'sales/new/index.html', context=context)
    
    context['form'] = form  
    context['formset'] = formset  
    context['empty_form'] = test_formset.forms[0]  
    return render(request, 'sales/new/index.html', context=context) 


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
    return render(request, 'sales/edit/index.html', context=context)

