from django.shortcuts import render, redirect
from django.urls import reverse, resolve
from django.contrib.auth.decorators import login_required, permission_required
from pharmacy.utils import generate_random_number
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse,HttpResponseServerError
# from django.contrib.auth.models import Group
from utils.groups.access_groups import AccessGroups
from utils.groups.default_roles import DefaultRoles
from .forms import CompanyApplicationRegisterForm
from .forms import CompanyAccountActivationForm
# from .forms import CompanyAdminRegisterForm
from .forms import StoreForm
from .forms import PosCenterForm
from user.models import User, UserProfile
from .models import CompanyApplication
from .models import Company, Store, PosCenter
from .tasks import send_company_approval_email
from utils.defaults.init_company_groups import init_company_groups
from utils.defaults.init_company_groups import create_company_group
from utils.defaults.init_store_groups import init_store_groups

################### - Company Application - ################# 

@login_required(login_url='/login')
def company_application_list_view(request):
    applications = CompanyApplication.objects.all()

    context = { "applications" : applications }
    
    return render(request, 'company/application/list/index.html', context = context)


@login_required(login_url='/login')
def company_application_detail_view(request, app_id):
    data = CompanyApplication.objects.get(pk = app_id)

    context = { "data" : data }
    
    return render(request, 'company/application/detail/index.html', context = context)


def company_application_add_view(request):
    form = CompanyApplicationRegisterForm()

    context = { "form": form }

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
            print(form_data.errors)
            context = {"form": form_data}
            messages.error(request,"Failed To Submit Application!")

    return render(request, 'company/application/new/index.html', context=context)


@login_required(login_url='/login')
def company_application_edit_view(request, app_id):
    instance = CompanyApplication.objects.get(pk = app_id)

    form = CompanyApplicationRegisterForm(instance=instance)

    context = { "detail": instance ,"form": form }

    if request.method == "POST":
        form_data = CompanyApplicationRegisterForm(request.POST, request.FILES, instance=instance)

        if form_data.is_valid():
            application = form_data.save()
            code = generate_random_number()
            application.activation_code = code
            application.save()

            messages.info(request, "Application is edited successfully!")
            return redirect('company:company-application-list')
        else:
            print(form_data.errors)
            context["form"] = form_data
            messages.error(request,"Failed To Edit Application!")
    
    return render(request, 'company/application/edit/index.html', context = context)

 
def company_application_edit_status_view(request, app_id, new_status):
    valid_statuses = [ 'PENDING', 'APPROVED' , 'CREATED' ,'DECLINED', 'CANCELLED' ]

    if new_status not in valid_statuses:
        messages.error(request, 'Invalid status provided.')
        return render(request, 'company/application/list/index.html')

    # Retrieve the object based on the primary key
    obj = get_object_or_404(CompanyApplication, pk = app_id)

    # Change the status
    obj.status = new_status
    obj.save()

    if new_status == "APPROVED":
        recipient_email = obj.email
        activation_code = obj.activation_code
        redirect_view_name = 'company:company-account-activate'  # Use the correct view name
        # Reverse the view name to get the relative path
        relative_path = reverse(redirect_view_name)
        # Build the absolute URL by combining it with the base URL
        redirect_url = request.build_absolute_uri(relative_path)
        # print(redirect_url)
        send_company_approval_email(recipient_email, activation_code, redirect_url)


    messages.success(request, f'Status of application changed to {new_status}.')
    return redirect('company:company-application-list')


def company_account_activate_view(request):
    form = CompanyAccountActivationForm()

    context = {"form": form}

    if request.method == "POST":
        form = CompanyAccountActivationForm(request.POST, request.FILES)

        if form.is_valid():
            company_email = form.cleaned_data.get('company_email')
            activation_code = form.cleaned_data.get('activation_code')

            if not CompanyApplication.objects.filter(email = company_email, activation_code = activation_code).exists():
                messages.error(request, "Company Application Not Found!")
                return render(request, 'company/application/activation/index.html', context=context)
            else:
                companyApplication = CompanyApplication.objects.filter(email = company_email, activation_code = activation_code).first()
            

            if companyApplication.status == "DECLINED":
                messages.info(request, "Company application was declined!")
                return render(request, 'company/activation/index.html', context=context)
            
            if companyApplication.status == "APPROVED" or companyApplication.status == "CREATED":
                company, _ = Company.objects.get_or_create(
                            name = companyApplication.name,
                            phone = companyApplication.phone,
                            email = companyApplication.email,
                            location = companyApplication.location,
                            logo = companyApplication.logo,
                            activation_code = activation_code)
                
                init_company_groups(company_id=company.pk)
                
                companyApplication.status = "CREATED"
                companyApplication.save()

                first_name = form.cleaned_data.get("first_name")
                last_name = form.cleaned_data.get("last_name")
                phone = form.cleaned_data.get("phone")
                email = form.cleaned_data.get("email")
                password2 = form.cleaned_data.get("password2")

                user = User(
                    username = email,
                    email = email,
                    first_name = first_name,
                    last_name = last_name,
                    phone = phone)

                user.account_type = AccessGroups.COMPANY_ADMIN
                user.set_password(str(password2))
                user.save()

                UserProfile.objects.get_or_create(user=user, company=company)

                group = create_company_group(company_id=company.pk, role_name= DefaultRoles.ACCOUNT_HOLDER)

                if group:
                    user.groups.add(group)

                messages.info(request, "Company account activated successfully!")                  
                return redirect('user:home')
        else:
            context['form'] = form
            messages.error(request,"Failed To Submit Application!")

    return render(request, 'company/application/activation/index.html', context=context)


@login_required(login_url='/login')
def company_application_delete_view(request, app_id):
    app = CompanyApplication.objects.all(pk = app_id)

    app.hard_delete()

    return redirect('company:company-application-list')


###################### - Company - ####################

@login_required(login_url='/login')
@permission_required("company.list_company", raise_exception=True)
def company_list_view(request):
    companies = Company.objects.all()

    context = { "companies" : companies }
    
    return render(request, 'company/list/index.html', context = context)


@login_required(login_url='/login')
@permission_required("company.view_company", raise_exception=True)
def company_detail_view(request, company_id):
    company = Company.objects.get(pk = company_id)

    context = { "company" : company }
    
    return render(request, 'company/detail/index.html', context = context)


@login_required(login_url='/login')
@permission_required("company.edit_company", raise_exception=True)
def company_edit_view(request, company_id):
    data = Company.objects.all(pk = company_id)

    context = { "data" : data }
    
    return render(request, 'company/new/index.html', context = context)


@login_required(login_url='/login')
@csrf_exempt  # Use this decorator if you don't need CSRF protection for this view
@permission_required("company.deactivate_company", raise_exception=True)
def company_deactivate_view(request, company_id):
    if request.method == 'POST':
        try:
            company = get_object_or_404(Company, id=company_id)
            company.delete()
            return JsonResponse({'message': 'Company deactivated successfully'})
        except Exception as e:
            return HttpResponseServerError({'message': f'Failed to delete company. Error: {str(e)}'})


@permission_required("company.delete_company", raise_exception=True)
def company_delete_view(request, pk):
    data = Company.objects.all(pk = pk)

    context = { "data" : data }
    
    return render(request, 'company/new/index.html', context = context)


###################### - Company Store - ####################

@login_required(login_url='/login')
@permission_required("company.list_store", raise_exception=True) #app_name.codename
def company_store_list_view(request, company_id):
    company = Company.objects.get(pk=company_id) 
    stores = Store.objects.filter(company = company)

    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            store_exists = Store.objects.filter(company=company, name__iexact=name).exists()
            if store_exists:
                form.errors['name'] = ['Name Already Exists!']
                return JsonResponse({'success': False, 'errors': form.errors})
            else:         
                store = form.save(commit=False)
                store.created_by = request.user
                store.company = company
                store.save()

                init_store_groups(store_id=store.pk)
            
            return JsonResponse({'success': True})
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
@permission_required("company.view_store", raise_exception=True)
def store_detail_view(request, store_id):
    store = Store.objects.get(pk = store_id) 

    if request.is_ajax():
        if request.method == 'POST':
            form = StoreForm(request.POST, instance=store)
            if form.is_valid():
                store = form.save(commit=False)
                store.created_by = request.user
                store.company = store.company
                store.save()
                return JsonResponse({'success': True, 'store_id': store.id})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = StoreForm(instance=store)

    context = {  "company" : store.company, "store" : store, "form": form }
    
    return render(request, 'store/detail/index.html', context = context)


@login_required(login_url='/login')
@permission_required("company.delete_store", raise_exception=True)
def store_delete_view(request, company_id, store_id):
    company = Company.objects.get(pk=company_id) 
    store = Store.objects.get(pk = store_id) 

    store.hard_delete()
    if request.is_ajax():
        return JsonResponse({'success': True})
    else:
        return redirect(reverse('company:company-store-list', kwargs={'company_id': company.id}))


###################### - Company PosCenter - ####################

@login_required(login_url='/login')
@permission_required("company.list_pos_center", raise_exception=True)
def pos_list_view(request, store_id):
    store = Store.objects.get(pk=store_id) 
    pos_centers = PosCenter.objects.filter(store= store)

    if request.method == 'POST':
        form = PosCenterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            if PosCenter.objects.filter(store=store, name__iexact=name).exists():
                form.errors['name'] = ["Name ALready Exists!"]
                return JsonResponse({'success': False, 'errors': form.errors})
            
            pos_center = form.save(commit=False)
            pos_center.name = form.cleaned_data['name']
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


@login_required(login_url='/login')
def pos_sales_list_view(request, pos_id):
    pass


@login_required(login_url='/login')
def pos_sales_new_view(request, pos_id):
    pass