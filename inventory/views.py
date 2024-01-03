from django.shortcuts import render
from django.views import View
from django.views.generic import ListView,CreateView
from django.http import JsonResponse
from .forms import ProductTypeForm, ProductCategoryForm, ProductUnitsForm
from .forms import ProductForm, ReceivedStockForm,ReceivedStockItemForm
from .models import ProductType, ProductCategory, ProductUnits, Product
from .models import ReceivedStock, ReceivedStockItem
from .mixins import CompanyMixin, CompanyFormMixin
from company.models import Company
from django.forms import formset_factory


class StockListCreateView(CompanyMixin, View):
    form_class = ProductForm
    initial = {"unit_price": 0}
    template_name = "stock/index.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        data = Product.objects.all()
        return render(request, self.template_name, {"form": form, "results": data})

    def post(self, request, *args, **kwargs): 
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.company = self.get_company()
            form.instance.created_by = self.get_user()
            product = form.save(commit=False)
            product.name = product.name.capitalize()
            product.save() 

            if self.request.is_ajax(): # Using Ajax 
                return JsonResponse({'success': True, 'name': product.name})
        else: # Form is Invalid
            if self.request.is_ajax(): # Using Ajax 
                return JsonResponse({'success': False, 'errors': form.errors})
        
        return render(request, self.template_name, {"form": form})


class StockCreateView(CompanyFormMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'stock/index.html'

    def form_valid(self, form):
        form.instance.company = self.get_company()
        form.instance.created_by = self.get_user()
        product = form.save(commit=False)
        product.name = product.name.capitalize()
        product.save() 
        print(product.company)    
        print(product.created_by)                  

        if self.request.is_ajax():
            # If it's an AJAX request, return a JsonResponse
            return JsonResponse({'success': True, 'name': product.name})
        else:
            # If it's a regular form submission, redirect to success URL
            return super().form_valid(form)


    def form_invalid(self, form):
        print("form.errors")

        if self.request.is_ajax():
            return JsonResponse({'success': False, 'errors': form.errors})
        else:
            # If it's a regular form submission and the form is invalid, render the form
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print("context")
        # print(context["company"])
        return context


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
                product_type.company = company
                product_type.save()
                return JsonResponse({'success': True, 'name': product_type.name})
            else:
                return JsonResponse({'success': False, 'errors': productTypeForm_data.errors})
        
        if form_prefix == 'productCategoryForm':
            productCategoryForm_data = ProductCategoryForm(request.POST or None,prefix="productCategoryForm")
            if productCategoryForm_data.is_valid():
                product_category = productCategoryForm_data.save(commit=False)
                product_category.name = product_category.name.capitalize()
                product_category.company = company
                product_category.save()
                return JsonResponse({'success': True, 'name': product_category.name})
            else:
                return JsonResponse({'success': False, 'errors': productCategoryForm_data.errors})
        
        if form_prefix == 'productUnitsForm':
            productUnitsForm_data = ProductUnitsForm(request.POST or None,prefix="productUnitsForm")
            if productUnitsForm_data.is_valid():
                product_unit = productUnitsForm_data.save(commit=False)
                product_unit.name = product_unit.name.lower()
                product_unit.company = company
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
        
                    
