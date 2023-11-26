from django.shortcuts import render
from .forms import ReceivedStockForm,ReceivedStockItemForm
from .models import ReceivedStock, ReceivedStockItem
from django.forms import formset_factory

def add_new_stock(request):
    context = {}
    form = ReceivedStockForm()
    ReceivedStockItemFormSet = formset_factory(ReceivedStockItemForm, extra=2)
    formset = ReceivedStockItemFormSet(prefix='items')

    if request.method == "POST":
        form_data = ReceivedStockForm(request.POST)
        formset_data = ReceivedStockItemFormSet(request.POST, prefix='items')

        if form_data.is_valid() and formset_data.is_valid():
            received_stock = form_data.save(commit=False)
            received_stock.company = None
            received_stock.branch = None
            received_stock.created_by = None
            received_stock.save()

            for formset_data_item in formset_data:
                item = formset_data_item.save(commit=False)
                item.received_stock = received_stock
                item.company = None
                item.branch = None
                item.created_by = None
                item.save()

            context['success_message'] = 'Stock added successfully'
        else:
            context['form'] = form_data
            context['formset'] = formset_data
            return render(request, 'stock/index.html', context=context)
    
    context['form'] = form  
    context['formset'] = formset  
    return render(request, 'stock/index.html', context=context)       
        
                    
