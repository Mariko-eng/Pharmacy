from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pharmacy.utils import generate_random_number
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse,HttpResponseServerError
from django.contrib.auth.models import Group
from .forms import CompanyApplicationRegisterForm
from .forms import CompanyAccountActivationForm
from .forms import CompanyAdminRegisterForm
from .forms import StoreForm
from .forms import PosCenterForm
from user.models import AccessGroups, User, UserProfile
from user.permissions import DefaultRoles
from .models import CompanyApplication
from .models import Company, Store, PosCenter

################### - Company Application - ################# 

def company_application_add_view(request):
    form = CompanyApplicationRegisterForm()

    context = {"form": form}

    if request.method == "POST":
        form_data = CompanyApplicationRegisterForm(request.POST, request.FILES)

        if form_data.is_valid():
            application = form_data.save()
            code = generate_random_number()
            print("code is : " + str(code))
            application.activation_code = code
            application.save()

            messages.info(request, "Application is submitted successfully!")
            # return redirect('user:home')
        else:
            context = {"form": form_data}
            messages.error(request,"Failed To Submit Application!")

    return render(request, 'company/application/new/index.html', context=context)


def company_account_activate_view(request):
    form = CompanyAccountActivationForm()

    context = {"form": form}

    if request.method == "POST":
        form = CompanyAccountActivationForm(request.POST, request.FILES)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            activation_code = form.cleaned_data.get('activation_code')

            if CompanyApplication.objects.filter(email = email, activation_code = activation_code).exists():
                companyApplication = CompanyApplication.objects.filter(email = email, activation_code = activation_code).first()

                if companyApplication.status == "DECLINED":
                    messages.info(request, "Company application was not successful!")
                    return render(request, 'company/activation/index.html', context=context)

                company, created = Company.objects.get_or_create(
                    name = companyApplication.name,
                    phone = companyApplication.phone,
                    email = email,
                    location = companyApplication.location,
                    logo = companyApplication.logo,
                    activation_code = activation_code)

                if companyApplication.status != "APPROVED":
                    companyApplication.status = "APPROVED"
                    companyApplication.save()
                    messages.info(request, "Company account activated successfully!")
                else:
                    messages.info(request, "Company account already activated!")                    

                return redirect('company:company-admin-user-register', company_id = company.id)
            else:
                messages.error(request,"Failed To Activate Company!")
                form.errors['activation_code'] = ['You have submitted a Wrong code!'] 
        else:
            messages.error(request,"Failed To Submit Application!")

    return render(request, 'company/activation/index.html', context=context)

def company_admin_user_register_view(request, company_id):
    company = Company.objects.get(pk = company_id)

    form = CompanyAdminRegisterForm()
    context = { 
        "company": company,
        "form": form 
        }

    if request.method == "POST":
        form_data = CompanyAdminRegisterForm(request.POST)

        if form_data.is_valid():
            first_name = form_data.cleaned_data.get('first_name')
            last_name = form_data.cleaned_data.get('last_name')
            phone = form_data.cleaned_data.get('phone')
            email = form_data.cleaned_data.get('email')
            password2 = form_data.cleaned_data.get('password2')

            user = User(
                username = email,
                first_name = first_name,
                last_name = last_name,
                phone = phone,
                email = email,
            )
            user.account_type = AccessGroups.COMPANY_ADMIN
            user.set_password(str(password2))
            user.save()

            group, created = Group.objects.get_or_create(
                name = DefaultRoles.ACCOUNT_HOLDER
            )

            user.groups.add(group)

            UserProfile.objects.get_or_create(user=user, company=company)

            messages.info(request, "Company admin account created successfully!")
            return redirect('user:home')
        else:
            context['form'] = form_data
            print(form_data.errors)
            messages.error(request,"Failed to create company admin account!")
            
    return render(request, 'company/admin_account/new.html', context=context)


@login_required(login_url='/login')
def company_application_list_view(request):
    data = CompanyApplication.objects.all()

    context = { "data" : data }
    
    return render(request, 'company/new/index.html', context = context)

@login_required(login_url='/login')
def company_application_detail_view(request, pk):
    data = CompanyApplication.objects.all(pk = pk)

    context = { "data" : data }
    
    return render(request, 'company/new/index.html', context = context)

@login_required(login_url='/login')
def company_application_edit_view(request, pk):
    data = CompanyApplication.objects.all(pk = pk)

    context = { "data" : data }
    
    return render(request, 'company/new/index.html', context = context)

@login_required(login_url='/login')
def company_application_delete_view(request, pk):
    data = CompanyApplication.objects.all(pk = pk)

    context = { "data" : data }
    
    return render(request, 'company/new/index.html', context = context)


###################### - Company - ####################

@login_required(login_url='/login')
def company_list_view(request):
    data = Company.objects.all()

    context = { "data" : data }
    
    return render(request, 'company/new/index.html', context = context)


@login_required(login_url='/login')
def company_detail_view(request, company_id):
    company = Company.objects.get(pk = company_id)

    context = { "company" : company }
    
    return render(request, 'company/detail/index.html', context = context)

@login_required(login_url='/login')
def company_edit_view(request, company_id):
    data = Company.objects.all(pk = company_id)

    context = { "data" : data }
    
    return render(request, 'company/new/index.html', context = context)

@login_required(login_url='/login')
@csrf_exempt  # Use this decorator if you don't need CSRF protection for this view
def company_deactivate_view(request, company_id):
    if request.method == 'POST':
        try:
            company = get_object_or_404(Company, id=company_id)
            company.delete()
            return JsonResponse({'message': 'Company deactivated successfully'})
        except Exception as e:
            return HttpResponseServerError({'message': f'Failed to delete company. Error: {str(e)}'})


def company_delete_view(request, pk):
    data = Company.objects.all(pk = pk)

    context = { "data" : data }
    
    return render(request, 'company/new/index.html', context = context)

###################### - Company Store - ####################

@login_required(login_url='/login')
def store_list_view(request, company_id):
    company = Company.objects.get(pk=company_id) 
    stores = Store.objects.filter(company = company)

    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.created_by = request.user
            store.company = company
            store.save()
            return JsonResponse({'success': True, 'store_id': store.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = StoreForm()
    
    context = {
        'form': form,
        'company': company,
        'stores': stores }
    
    return render(request, 'store/list/index.html', context = context)

@login_required(login_url='/login')
def store_detail_view(request, company_id, store_id):
    company = Company.objects.get(pk= company_id) 
    store = Store.objects.get(pk = store_id) 

    context = { 
        "company" : company,
        "store" : store }
    
    return render(request, 'store/detail/index.html', context = context)

@login_required(login_url='/login')
def store_edit_view(request, company_id, store_id):
    company = Company.objects.get(pk= company_id) 
    store = Store.objects.get(pk = store_id) 

    context = { 
        "company" : company,
        "store" : store }
    
    return render(request, 'store/new/index.html', context = context)


@login_required(login_url='/login')
def store_delete_view(request, company_id, store_id):
    company = Company.objects.get(pk= company_id) 
    store = Store.objects.get(pk = store_id) 

    context = { 
        "company" : company,
        "store" : store }
    
    return render(request, 'store/new/index.html', context = context)


###################### - Company PosCenter - ####################

@login_required(login_url='/login')
def pos_list_view(request, store_id):
    store = Store.objects.get(pk=store_id) 
    pos_centers = PosCenter.objects.filter(store= store)

    if request.method == 'POST':
        form = PosCenterForm(request.POST)
        if form.is_valid():
            pos_center = form.save(commit=False)
            if PosCenter.objects.filter(name = pos_center.name.capitalize(), store = store).exists():
                form.errors['name'] = ["Name ALready Exists!"]
                return JsonResponse({'success': False, 'errors': form.errors})
            
            pos_center.name = form.cleaned_data['name'].capitalize()
            pos_center.created_by = request.user
            pos_center.store = store
            pos_center.save()
        
            return JsonResponse({'success': True, 'pos_center_id': pos_center.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PosCenterForm()
    
    context = {
        'form': form,
        'company': store.company,
        'store': store,
        'pos_centers': pos_centers }
    
    return render(request, 'pos/list/index.html', context = context)

@login_required(login_url='/login')
def pos_detail_view(request, store_id, pos_id):
    store = Store.objects.get(pk=store_id) 
    pos_center = PosCenter.objects.filter(pk = pos_id)

    context = { 
        'company': store.company,
        "store" : store,
        "pos_center": pos_center}
    
    return render(request, 'pos/detail/index.html', context = context)


@login_required(login_url='/login')
def pos_edit_view(request, store_id, pos_id):
    store = Store.objects.get(pk=store_id) 
    pos_center = PosCenter.objects.filter(pk = pos_id)

    context = { 
        'company': store.company,
        "store" : store,
        "pos_center": pos_center}
    
    return render(request, 'pos/new/index.html', context = context)


@login_required(login_url='/login')
def pos_delete_view(request, store_id, pos_id):
    store = Store.objects.get(pk=store_id) 
    pos_center = PosCenter.objects.filter(pk = pos_id)

    context = { 
        'company': store.company,
        "store" : store,
        "pos_center": pos_center}
    
    return render(request, 'pos/new/index.html', context = context)