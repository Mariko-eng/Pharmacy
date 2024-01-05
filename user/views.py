from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect,Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse,HttpResponseServerError
from django.contrib.auth.models import Group, Permission
from user.permissions import DefaultRoles
from .forms import CompanyRoleFrom,CompanyUserForm
from .models import AccessGroups
from .models import User
from .models import Company
from .models import Store
from .models import PosCenter
from .models import CompanyGroup


# @unauthenticated_user
def index(request):
    next_url = request.GET.get('next')  # Get the value of 'next' parameter from the query string

    context = {}
    if request.user.is_authenticated:
        return redirect('user:home')
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)

            if request.user.is_superuser == False and request.user.is_staff == False:
                request.session['company_id'] = request.user.company.id
                request.session['company_name'] = request.user.company.name

            if next_url:
                return redirect(next_url)  # Redirect to the URL specified in 'next' parameter
        
            return redirect('user:home')
        else:
            messages.info(request, "Please Provide A Valid Username/Email And Paassword")

    return render(request,'auth/login/index.html',context)

def logoutView(request):
    # Clear the session data
    request.session.flush()
    
    logout(request)
    return redirect('user:login')


@login_required(login_url='/login')
def home_view(request):

    if request.user.account_type == AccessGroups.APP_ADMIN:
        return redirect('user:super-dashboard')
    
    if request.user.account_type == AccessGroups.COMPANY_ADMIN:
        return redirect(reverse('user:company-dashboard'))
        # return HttpResponseRedirect(reverse('user:company-dashboard'))
    
    if request.user.account_type == AccessGroups.STORE_ADMIN:
        return redirect(reverse('user:company-dashboard'))
        # return HttpResponseRedirect(reverse('user:company-dashboard'))
        
    if request.user.account_type == AccessGroups.POS_ATTENDANT:
        return redirect(reverse('user:company-dashboard'))
        # return HttpResponseRedirect(reverse('user:company-dashboard'))
        
    raise Http404('Page Not Found!')

########################### Dashboard ##################
def super_dashboard(request):
    context={}
    return render(request, "dashboard/super/index.html", context=context)

def company_dashboard(request, company_id = None):
    company = None
    if company_id is not None :
        company = Company.objects.get(pk = company_id)
    else :
        company = request.user.userprofile.company

    context={"company" : company}
    if company is not None:
        return render(request, "dashboard/company/index.html", context = context)
    else:
        raise Http404('Page Not Found!')


def store_dashboard(request, store_id = None):
    store = None
    if store_id is not None:
        store = Store.objects.get(pk = store_id)
    else :
        store = request.user.userprofile.store

    print(store)

    context={
        "company" : store.company,
        "store" : store
        }

    if store is not None:
        return render(request, "dashboard/store/index.html", context = context)
    else:
        raise Http404('Page Not Found!')


def pos_dashboard(request, pos_id = None):
    pos = None
    if pos_id is not None :
        pos = PosCenter.objects.get(pk = pos_id)
    else :
        pos = request.user.userprofile.store

    context={"pos" : pos}

    if pos is not None:
        return render(request, "dashboard/pos/index.html", context = context)
    else:
        raise Http404('Page Not Found!')


########################### Users ##################

@login_required(login_url='/login')
def users_list_view(request):
    users = User.objects.all()
    context = {
        "users" : users
    }
    return render(request, "user/super/list/index.html", context = context)


@login_required(login_url='/login')
def users_company_list_view(request, company_id):

    company = Company.objects.get(pk = company_id)

    users = User.objects.filter(userprofile__company=company)

    print(users)

    context = {
        "company": company,
        "users" : users
    }
    return render(request, "user/company/list/index.html", context = context)


@login_required(login_url='/login')
def users_company_new_view(request, company_id):

    company = Company.objects.get(pk = company_id)

    users = User.objects.filter(company=company)

    form = CompanyUserForm(company=company)

    context = {
        "users" : users,
        "company": company,
        "form": form }

    if request.method == "POST":
        form_data = CompanyUserForm(request.POST, company = company)
        
        if form_data.is_valid():
            roles = form_data.cleaned_data.pop('roles', [])
            stores = form_data.cleaned_data.pop('stores', [])

            user = User(
                company = company,
                first_name = form_data.cleaned_data['first_name'],
                last_name = form_data.cleaned_data['last_name'],
                email = form_data.cleaned_data['email'],
                phone_number = form_data.cleaned_data['phone_number'],
            )

            user.set_password(str(user.email))
            user.created_by = request.user
            user.save()

            for item in roles:
                group, created = Group.objects.get_or_create(name=item)
                if group:
                    user.groups.add(group)

            # for stores in stores:
            #     if not CompanyStaff.objects.filter(company = company,branch = branch,user =  user).exists():
            #         CompanyStaff.objects.create(
            #             company = company,
            #             branch = branch,
            #             user =  user,
            #             created_by = request.user)


            return redirect('user:company-users-list', company_id=company_id)

        context['form'] = form_data

    return render(request, "user/company/new/index.html", context=context)


########################### Roles #######################

@login_required(login_url='/login')
def users_roles_list_view(request):
    users = User.objects.all()
    context = {
        "users" : users
    }
    return render(request, "role/super/list/index.html", context = context)


@login_required(login_url='/login')
def users_role_permissions_list_view(request, role_id):
    group = Group.objects.get(pk=role_id)
    group_permissions = group.permissions.all()
    # Specify the app labels you want to include
    model_names = ['user', 'company','companymanager','companystaff']

    # Initialize an empty list to store permissions
    all_permissions = []

    # Loop through each app label and filter permissions
    for model_name in model_names:
        permissions_for_app = Permission.objects.filter(
            content_type__model=model_name
        )
        # print(permissions_for_app)
        all_permissions.extend(permissions_for_app)

    context = {
        "group": group,
        "group_permissions": group_permissions,
        "all_permissions" : all_permissions}

    if request.method == "POST":
        selected_perms = request.POST.getlist("permissions") 
        
        # Get the existing permissions of the group
        existing_perms = list(group.permissions.values_list('id', flat=True))

        for perm_id in selected_perms:
            selected_perm = Permission.objects.get(pk = perm_id)
            group.permissions.add(selected_perm)

        # Remove permissions that are not in the selected list
        for perm_id in existing_perms:
            if str(perm_id) not in selected_perms:
                existing_perm = Permission.objects.get(pk=perm_id)
                group.permissions.remove(existing_perm)
        
    return render(request, "user/super/roles/index.html", context= context)


########################### Company Roles #######################

@login_required(login_url='/login')
def users_company_roles_list_view(request, company_id):
    company = Company.objects.get(pk = company_id)

    groups_static = []
    default_groups = DefaultRoles.choices
    for default_group in default_groups:
        group, created = Group.objects.get_or_create(name = default_group[0])
        groups_static.append(group)

    company_groups =  CompanyGroup.objects.filter(company = company)

    context = {
        "company": company,
        "groups_static": groups_static,
        "company_groups": company_groups
    }

    return render(request, "role/company/list/index.html", context = context)


@login_required(login_url='/login')
def users_company_roles_new_view(request, company_id):

    company = Company.objects.get(pk = company_id)

    # Specify the app labels you want to include
    model_names = ['company','store','poscenter', 'supplierentity']

        # Initialize an empty list to store permissions
    all_permissions = []

    # Loop through each app label and filter permissions
    for model_name in model_names:
        permissions_for_app = Permission.objects.filter(
            content_type__model=model_name
        )
        # print(permissions_for_app)
        all_permissions.extend(permissions_for_app)

    form = CompanyRoleFrom()

    context = {
        "company": company,
        "all_permissions" : all_permissions,
        "form": form }

    if request.method == "POST":
        form_data = CompanyRoleFrom(request.POST)

        if form_data.is_valid():
            group_name = form_data.cleaned_data.get("name")
            selected_perms = request.POST.getlist("permissions") 
            company_group = CompanyGroup.create_company_group(group_name=group_name, company=company)

            for perm_id in selected_perms:
                selected_perm = Permission.objects.get(pk = perm_id)
                company_group.group.permissions.add(selected_perm)
        
            return redirect('user:company-roles-list', company_id=company_id)

        context['form'] = form_data

    return render(request, "role/company/new/index.html", context=context)


@login_required(login_url='/login')
def users_company_role_permissions_list_view(request, company_id, role_id):
    company = Company.objects.get(pk = company_id)

    group = Group.objects.get(pk=role_id)
    group_permissions = group.permissions.all()
    # Specify the app labels you want to include
    model_names = ['user', 'company','companymanager','companystaff']

    # Initialize an empty list to store permissions
    all_permissions = []

    # Loop through each app label and filter permissions
    for model_name in model_names:
        permissions_for_app = Permission.objects.filter(
            content_type__model=model_name
        )
        # print(permissions_for_app)
        all_permissions.extend(permissions_for_app)

    context = {
        "company": company,
        "group": group,
        "group_permissions": group_permissions,
        "all_permissions" : all_permissions}

    if request.method == "POST":
        selected_perms = request.POST.getlist("permissions") 
        
        # Get the existing permissions of the group
        existing_perms = list(group.permissions.values_list('id', flat=True))

        for perm_id in selected_perms:
            selected_perm = Permission.objects.get(pk = perm_id)
            group.permissions.add(selected_perm)

        # Remove permissions that are not in the selected list
        for perm_id in existing_perms:
            if str(perm_id) not in selected_perms:
                existing_perm = Permission.objects.get(pk=perm_id)
                group.permissions.remove(existing_perm)
        
    return render(request, "user/super/roles/index.html", context= context)



#################################
@login_required(login_url='/login')
def company_list(request):
    # companies = Company.objects.all()
    companies = Company.objects1.get_queryset(request.user).all()

    return render(request, "company/list/index.html", context={'companies': companies})

