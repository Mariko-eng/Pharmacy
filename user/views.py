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
from .forms import CompanyAdminUserForm
from .forms import StoreAdminUserForm
from .forms import POSAttendantUserForm
from .models import AccessGroups
from .models import User
from .models import UserProfile
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
    
    if request.user.account_type == AccessGroups.STORE_ADMIN:
        return redirect(reverse('user:store-dashboard'))
        
    if request.user.account_type == AccessGroups.POS_ATTENDANT:
        return redirect(reverse('user:pos-dashboard'))
        
    raise Http404('Page Not Found!')

########################### Dashboard ##################
@login_required(login_url='/login')
def super_dashboard(request):
    context={}
    return render(request, "dashboard/super/index.html", context=context)


@login_required(login_url='/login')
def company_dashboard(request, company_id = None):
    company = None
    if company_id is not None :
        company = Company.objects.get(pk = company_id)
    else :
        company = request.user.userprofile.company

    context = { "company" : company }

    if company is not None:
        return render(request, "dashboard/company/index.html", context = context)
    else:
        raise Http404('Page Not Found!')

@login_required(login_url='/login')
def store_dashboard(request, store_id = None):
    store = None
    if store_id is not None:
        store = Store.objects.get(pk = store_id)
    else :
        store = request.user.userprofile.store

    context={ "company" : store.company, "store" : store }

    if store is not None:
        return render(request, "dashboard/store/index.html", context = context)
    else:
        raise Http404('Page Not Found!')

@login_required(login_url='/login')
def pos_dashboard(request, pos_id = None):
    pos = None
    if pos_id is not None :
        pos = PosCenter.objects.get(pk = pos_id)
    else :
        pos = request.user.userprofile.pos_center

    context = { "company" : pos.store.company, "store" : pos.store, "pos" : pos }

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

    access_group = request.GET.get('access_group', None)

    if access_group is not None:
        users  = users.filter(account_type = access_group)

    context = {
        "company": company,
        "users" : users,
        "access_group": access_group
    }
    return render(request, "user/company/list/index.html", context = context)


@login_required(login_url='/login')
def users_company_new_view(request, company_id):
    access_group = request.GET.get('access_group', None)

    if  access_group == AccessGroups.COMPANY_ADMIN:
        return redirect(reverse('user:users-company-admin-new', kwargs={'company_id': company_id}))

    if  access_group == AccessGroups.STORE_ADMIN:
        return redirect(reverse('user:users-company-store-admin-new', kwargs={'company_id': company_id}))

    return redirect(reverse('user:users-company-list'))


@login_required(login_url='/login')
def users_company_admin_user_new(request, company_id):
    company = Company.objects.get(pk = company_id)
    form = CompanyAdminUserForm()

    context = { "company": company, "form": form }
    
    if request.method == "POST":
        form_data = CompanyAdminUserForm(request.POST)

        if form_data.is_valid():
            first_name = form_data.cleaned_data.get('first_name')
            last_name = form_data.cleaned_data.get('last_name')
            phone = form_data.cleaned_data.get('phone')
            email = form_data.cleaned_data.get('email')

            user = User(
                username = email,
                first_name = first_name,
                last_name = last_name,
                phone = phone,
                email = email,
            )
            user.account_type = AccessGroups.COMPANY_ADMIN
            user.set_password(str(email))
            user.save()

            group, created = Group.objects.get_or_create(
                name = DefaultRoles.COMPANY_ADMIN
            )

            user.groups.add(group)

            UserProfile.objects.get_or_create(user=user, company=company)

            messages.info(request, "Company admin account created successfully!")
            return redirect(reverse('user:users-company-list', kwargs={'company_id': company_id}))
        else:
            context['form'] = form_data
            print(form_data.errors)
            messages.error(request,"Failed to create company admin account!")
            
    return render(request, "user/company/new/company_admin.html", context=context)


@login_required(login_url='/login')
def users_company_store_admin_user_new(request, company_id):
    company = Company.objects.get(pk = company_id)
    form = StoreAdminUserForm(company=company)

    context = { "company": company, "form": form }
    
    if request.method == "POST":
        form_data = StoreAdminUserForm(request.POST,company=company)

        if form_data.is_valid():
            store = form_data.cleaned_data.pop('store', None)
            roles = form_data.cleaned_data.pop('roles', [])

            if store is None:
                form_data.errors['store'] = ['Please select a store!']
                context['form_data'] = form_data
                return render(request, "user/new/store_admin.html", context=context)

            if not len(roles):
                form_data.errors['roles'] = ['Select At leaset one role']
                context['form_data'] = form_data
                return render(request, "user/new/store_admin.html", context=context)

            first_name = form_data.cleaned_data.get('first_name')
            last_name = form_data.cleaned_data.get('last_name')
            phone = form_data.cleaned_data.get('phone')
            email = form_data.cleaned_data.get('email')

            user = User(
                username = email,
                first_name = first_name,
                last_name = last_name,
                phone = phone,
                email = email,
            )
            user.account_type = AccessGroups.STORE_ADMIN
            user.set_password(str(email))
            user.save()

            for role in roles:
                group, created = Group.objects.get_or_create(name = role)
                user.groups.add(group)

            user_profile, created = UserProfile.objects.get_or_create(user=user, company=company)
            user_profile.store = store
            user_profile.save()

            messages.info(request, "Store admin account created successfully!")
            return redirect(reverse('user:users-company-list', kwargs={'company_id': company_id}))
        else:
            context['form'] = form_data
            print(form_data.errors)
            messages.error(request,"Failed to create store admin account!")
            
    return render(request, "user/company/new/store_admin.html", context=context)


@login_required(login_url='/login')
def users_store_list_view(request, store_id):

    store = Store.objects.get(pk = store_id)

    users = User.objects.filter(userprofile__store=store)

    access_group = request.GET.get('access_group', None)

    if access_group is not None:
        if access_group == AccessGroups.COMPANY_ADMIN:
            users = User.objects.filter(userprofile__company=store.company)
            users  = users.filter(account_type = access_group)
        else:
            users  = users.filter(account_type = access_group)

    context = {
        "company": store.company,
        "store": store,
        "users" : users,
        "access_group": access_group
    }
    return render(request, "user/store/list/index.html", context = context)


@login_required(login_url='/login')
def users_store_new_view(request, store_id):
    access_group = request.GET.get('access_group', None)

    if  access_group == AccessGroups.STORE_ADMIN:
        return redirect(reverse('user:users-store-admin-new', kwargs={'store_id': store_id}))

    if  access_group == AccessGroups.POS_ATTENDANT:
        return redirect(reverse('user:users-store-pos-attendant-new', kwargs={'store_id': store_id}))

    return redirect(reverse('user:store-index'))


@login_required(login_url='/login')
def users_store_admin_user_new(request, store_id):
    store = Store.objects.get(pk = store_id)
    company = store.company

    form = StoreAdminUserForm(company=store.company,store=store)

    context = { "company": company, "store":store, "form": form }
    
    if request.method == "POST":
        form_data = StoreAdminUserForm(request.POST,company=company, store=store)

        if form_data.is_valid():
            store = form_data.cleaned_data.pop('store', None)
            roles = form_data.cleaned_data.pop('roles', [])

            if store is None:
                form_data.errors['store'] = ['Please select a store!']
                context['form_data'] = form_data
                return render(request, "user/new/store_admin.html", context=context)

            if not len(roles):
                form_data.errors['roles'] = ['Select At leaset one role']
                context['form_data'] = form_data
                return render(request, "user/new/store_admin.html", context=context)

            first_name = form_data.cleaned_data.get('first_name')
            last_name = form_data.cleaned_data.get('last_name')
            phone = form_data.cleaned_data.get('phone')
            email = form_data.cleaned_data.get('email')

            user = User(
                username = email,
                first_name = first_name,
                last_name = last_name,
                phone = phone,
                email = email,
            )
            user.account_type = AccessGroups.STORE_ADMIN
            user.set_password(str(email))
            user.save()

            for role in roles:
                group, created = Group.objects.get_or_create(name = role)
                user.groups.add(group)

            user_profile, created = UserProfile.objects.get_or_create(user=user, company=company)
            user_profile.store = store
            user_profile.save()

            messages.info(request, "Store admin account created successfully!")
            return redirect(reverse('user:users-store-list', kwargs={'store_id': store_id}))
        else:
            context['form'] = form_data
            print(form_data.errors)
            messages.error(request,"Failed to create store admin account!")
            
    return render(request, "user/store/new/store_admin.html", context=context)



@login_required(login_url='/login')
def users_store_pos_attendant_user_new(request, store_id):
    store = Store.objects.get(pk = store_id)
    company = store.company

    form = POSAttendantUserForm(company=company,store=store)

    context = { "company": company, "store":store, "form": form }

    if request.method == "POST":
        form_data = POSAttendantUserForm(request.POST,company=company,store=store)

        if form_data.is_valid():
            store = form_data.cleaned_data.pop('store', None)
            pos_center = form_data.cleaned_data.pop('pos_center', None)

            if store is None:
                form_data.errors['store'] = ['Please select a store!']
                context['form_data'] = form_data
                return render(request, "user/new/pos_attendant.html", context=context)
            
            if pos_center is None:
                form_data.errors['pos_center'] = ['Please select a pos center!']
                context['form_data'] = form_data
                return render(request, "user/new/pos_attendant.html", context=context)

            first_name = form_data.cleaned_data.get('first_name')
            last_name = form_data.cleaned_data.get('last_name')
            phone = form_data.cleaned_data.get('phone')
            email = form_data.cleaned_data.get('email')

            user = User(
                username = email,
                first_name = first_name,
                last_name = last_name,
                phone = phone,
                email = email,
            )
            user.account_type = AccessGroups.POS_ATTENDANT
            user.set_password(str(email))
            user.save()

            group, created = Group.objects.get_or_create(name = DefaultRoles.CASHIER)
            user.groups.add(group)

            user_profile, created = UserProfile.objects.get_or_create(user=user, company=company)
            user_profile.store = store
            user_profile.pos_center = pos_center
            user_profile.save()

            messages.info(request, "POS attendant account created successfully!")
            return redirect(reverse('user:users-store-list', kwargs={'store_id': store_id}))
        else:
            context['form'] = form_data
            print(form_data.errors)
            messages.error(request,"Failed to create a POS attendant account!")

    return render(request, "user/store/new/pos_attendant.html", context=context)


    


@login_required(login_url='/login')
def users_company_new_view1(request, company_id):

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
                phone = form_data.cleaned_data['phone'],
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

