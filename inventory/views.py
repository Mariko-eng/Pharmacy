from django.shortcuts import render
from django.http import JsonResponse
from .forms import ProductTypeForm, ProductCategoryForm, ProductUnitsForm
from .forms import ProductForm, ReceivedStockForm,ReceivedStockItemForm
from .models import ProductType, ProductCategory, ProductUnits
from .models import ReceivedStock, ReceivedStockItem
from user.models import Company
from django.forms import formset_factory

def settings_index(request):
    company_id = request.session.get('company_id', None)
    company = None
    if company_id is not None:
        company = Company.objects.get(pk=company_id)
    elif request.user.company:
        company = request.user.company

    productTypeForm = ProductTypeForm(prefix="productTypeForm")
    productCategoryForm = ProductCategoryForm(prefix="productCategoryForm")
    productUnitsForm = ProductUnitsForm(prefix="productUnitsForm")

    productTypes = ProductType.objects.all()
    productCategories = ProductCategory.objects.all()
    productUnits = ProductUnits.objects.all()

    context = {
        "company" : company,
        "productTypes" : productTypes,
        "productCategories" : productCategories,
        "productUnits" : productUnits,
        "productTypeForm": productTypeForm,
        "productCategoryForm": productCategoryForm,
        "productUnitsForm": productUnitsForm}
    
    if request.method == "POST":
        form_prefix = request.POST.get('form_prefix')
        # print(form_prefix)

        if form_prefix == 'productTypeForm':
            productTypeForm_data = ProductTypeForm(request.POST or None,prefix="productTypeForm")
            if productTypeForm_data.is_valid():
                product_type = productTypeForm_data.save(commit=False)
                product_type.name = product_type.name.capitalize()
                product_type.save()
                return JsonResponse({'success': True, 'name': product_type.name})
            else:
                return JsonResponse({'success': False, 'errors': productTypeForm_data.errors})
        
        if form_prefix == 'productCategoryForm':
            productCategoryForm_data = ProductCategoryForm(request.POST or None,prefix="productCategoryForm")
            if productCategoryForm_data.is_valid():
                product_category = productCategoryForm_data.save(commit=False)
                product_category.name = product_category.name.capitalize()
                product_category.save()
                return JsonResponse({'success': True, 'name': product_category.name})
            else:
                return JsonResponse({'success': False, 'errors': productCategoryForm_data.errors})
        
        if form_prefix == 'productUnitsForm':
            productUnitsForm_data = ProductUnitsForm(request.POST or None,prefix="productUnitsForm")
            if productUnitsForm_data.is_valid():
                product_unit = productUnitsForm_data.save(commit=False)
                product_unit.name = product_unit.name.lower()
                product_unit.save()
                return JsonResponse({'success': True, 'name': product_unit.name})
            else:
                return JsonResponse({'success': False, 'errors': productUnitsForm_data.errors})
        
        return JsonResponse({'success': False, 'errors': {"name": "Form Prefix"}})

    return render(request, 'stock/settings/index.html', context=context)       


def stock_index(request):
    company_id = request.session.get('company_id', None)
    company = None
    if company_id is not None:
        company = Company.objects.get(pk=company_id)
    elif request.user.company:
        company = request.user.company

    form = ProductForm()

    context = {
        "company" :company,
        "form": form}

    if request.method == "POST":
        form_data = ProductForm(request.POST, request.FILES)
        if form_data.is_valid():
            product = form_data.save(commit=False)
            product.name = product.name.capitalize()
            product.save()
            return JsonResponse({'success': True, 'name': product.name})
        else:
            return JsonResponse({'success': False, 'errors': form_data.errors})

    return render(request, 'stock/index.html', context=context)       

def stock_new(request):
    context = {}
    form = ReceivedStockForm()
    ReceivedStockItemFormSet = formset_factory(ReceivedStockItemForm, extra=1)
    formset = ReceivedStockItemFormSet(prefix='items')

    if request.method == "POST":
        form_data = ReceivedStockForm(request.POST)
        formset_data = ReceivedStockItemFormSet(request.POST, prefix='items')

        print(form_data)
        print(formset_data)

        if form_data.is_valid() and formset_data.is_valid():
            received_stock = form_data.save(commit=False)
            received_stock.company = None
            received_stock.branch = None
            received_stock.created_by = None
            # received_stock.save()

            for formset_data_item in formset_data:
                item = formset_data_item.save(commit=False)
                item.received_stock = received_stock
                item.company = None
                item.branch = None
                item.created_by = None
                # item.save()

            context['success_message'] = 'Stock added successfully'
        else:
            context['form'] = form_data
            context['formset'] = formset_data
            return render(request, 'stock/index.html', context=context)
    
    context['form'] = form  
    context['formset'] = formset  
    return render(request, 'stock/new/index.html', context=context)       
        
                    
