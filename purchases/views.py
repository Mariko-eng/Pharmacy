from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.shortcuts import get_object_or_404
from django.forms import ValidationError
from .forms import RequiredFormSet
from .forms import PurchaseOrderRequestForm
from .forms import PurchaseOrderRequestItemForm
from company.models import Store
from .models import PurchaseOrderRequest
from .models import PurchaseOrderRequestItem


def store_purchase_orders_list(request, store_id):
    store = Store.objects.get(pk=store_id)
    company = store.company

    order_requests = PurchaseOrderRequest.objects.filter(store = store)
    context = {
        "company": company,
        "store": store,
        "order_requests": order_requests
        }

    return render(request, 'purchase_orders/list/index.html', context=context) 


def store_purchase_orders_new(request, store_id):
    store = Store.objects.get(pk=store_id)
    company = store.company

    context = {
        "company": company,
        "store": store}

    form = PurchaseOrderRequestForm(company=company)
    
    PurchaseOrderRequestItemFormset = formset_factory(PurchaseOrderRequestItemForm, formset=RequiredFormSet, extra=1, validate_min=True)

    formset = PurchaseOrderRequestItemFormset(prefix='items')

    if request.method == "POST":
        form_data = PurchaseOrderRequestForm(request.POST,company=company)
        formset_data = PurchaseOrderRequestItemFormset(request.POST, prefix='items')

        if form_data.is_valid() and formset_data.is_valid():
            supplier_type = form_data.cleaned_data.get("supplier_type", None)
            supplier_entity =  form_data.cleaned_data.get("supplier_entity", None)
            supplier_store =  form_data.cleaned_data.get("supplier_store", None)
            
            if supplier_type == "SUPPLIER" and supplier_entity is None:
                form_data.add_error("supplier_entity", ValidationError("Select a supplier!"))
                context['form'] = form_data
                context['formset'] = formset 
                return render(request, 'purchase_orders/new/index.html', context=context)
            elif supplier_type == "STORE" and supplier_store is None:
                form_data.add_error("supplier_store", ValidationError("Select a store!"))
                context['form'] = form_data
                context['formset'] = formset 
                return render(request, 'purchase_orders/new/index.html', context=context)

            
            order_request = PurchaseOrderRequest(
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
            
            order_request.company = company
            order_request.store = store
            order_request.created_by = request.user
            order_request.save()

            for formset_data_item in formset_data:
                item = formset_data_item.save(commit=False)
                item.order_request = order_request
                item.company = company
                item.store = store
                item.created_by = request.user
                item.save() 

            context['success_message'] = 'Purcahse order added successfully'
            return redirect('purchase_orders:purchase-orders-list', store_id=store_id)
        else:
            context['form'] = form_data
            context['formset'] = formset_data
            return render(request, 'purchase_orders/new/index.html', context=context)
    
    context['form'] = form  
    context['formset'] = formset  
    return render(request, 'purchase_orders/new/index.html', context=context) 


def store_purchase_orders_edit(request, store_id, order_request_id):
    store = get_object_or_404(Store, pk=store_id)
    company = store.company

    order_request = get_object_or_404(PurchaseOrderRequest, pk=order_request_id, store=store)

    context = {
        "company": company,
        "store": store,
        "order_request": order_request,
    }

    form = PurchaseOrderRequestForm(instance = order_request, company=company)

    PurchaseOrderRequestItemFormSet = modelformset_factory(PurchaseOrderRequestItem, form=PurchaseOrderRequestItemForm, extra=0)
    qs = order_request.receivedstockitem_set.all()

    formset = PurchaseOrderRequestItemFormSet(prefix='items',queryset=qs)

    if request.method == "POST":
        form_data = PurchaseOrderRequestForm(request.POST, instance=order_request, company=company)
        formset_data = PurchaseOrderRequestItemFormSet(request.POST, prefix='items', queryset=qs)

        if form_data.is_valid() and formset_data.is_valid():
            # Update the received stock details
            form_data.save()

            # Update each item in the formset
            for formset_data_item in formset_data:
                item = formset_data_item.save(commit=False)
                if item.id is None:
                    print("New")
                    item.order_request = order_request
                    item.company = company
                    item.store = store
                    item.created_by = request.user
                    item.save() # Save Instance
                else:
                    print("Old")
                    item.save() #  Update Instance

            context['success_message'] = 'Purcahse order edited successfully'
            return redirect('purchase_orders:purchase-orders-list', store_id=store_id)
        else:
            context['form'] = form_data
            context['formset'] = formset_data
            return render(request, 'purchase_orders/edit/index.html', context=context)

    
    context['form'] = form
    context['formset'] = formset
    return render(request, 'purchase_orders/edit/index.html', context=context)

