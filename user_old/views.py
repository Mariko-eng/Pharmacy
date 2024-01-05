from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse,HttpResponseServerError
from django.contrib.auth.models import Group, Permission
from .forms import AppUserForm
# from .forms import AdminUserForm
# from .forms import ManagerUserForm
# from .forms import PosUserForm
# from .forms import OtherStaffUserForm
from .forms import CompanyForm
from .forms import CompanyBranchForm
from .forms import CompanyPosForm
from .forms import CompanyUserForm,CompanyRoleFrom
from .permissions import DefaultGroups
# from .models import AppRoles, CompanyRoles, BranchRoles
from .models import User, UserRoleTrail,CompanyGroup
from .models import CompanyStaff, PosAttendant
from .models import Company, CompanyBranch, CompanyPos

# @unauthenticated_user
def index(request):
    next_url = request.GET.get('next')  # Get the value of 'next' parameter from the query string

    context = {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('user:home')
        
        return redirect('user:home')
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)

            if request.user.is_superuser == False and request.user.is_staff == False:
                request.session['company_id'] = request.user.company.id
                request.session['company_name'] = request.user.company.name

            # if request.user.groups.filter(name = BranchRoles.BRANCH_MANAGER):
            #     companyStaffDetails = CompanyStaff.objects.filter(user=request.user).firxt()
            #     request.session['branch_id'] = companyStaffDetails.branch.id
            #     request.session['branch_name'] = companyStaffDetails.branch.name

            if next_url:
                return redirect(next_url)  # Redirect to the URL specified in 'next' parameter
        
            return redirect('user:home')
        else:
            messages.info(request, "Please Provide A Valid Email And Paassword")

    return render(request,'auth/login/index.html',context)

def logoutView(request):
    # Clear the session data
    request.session.flush()
    
    logout(request)
    return redirect('user:login')

@login_required(login_url='/login')
def home_view(request):
    if request.user.is_superuser or request.user.is_staff:
        return render(request, "dashboard/super/index.html", context={})
    
    if request.user.groups.filter(name = DefaultGroups.ACCOUNT_HOLDER):
        company = request.user.company
        context = {"company" : company}
        return render(request, "dashboard/company/index.html", context=context)
    
    if request.user.groups.filter(name = DefaultGroups.COMPANY_ADMIN):
        company = request.user.company
        context = {"company" : company}
        return render(request, "dashboard/company/index.html", context=context)
    
    # if request.user.groups.filter(name = CompanyRoles.COMPANY_OWNER):
    #     return render(request, "dashboard/company/index.html", context={})
    
    # if request.user.groups.filter(name = CompanyRoles.COMPANY_ADMIN):
    #     return render(request, "dashboard/company/index.html", context={})

    return render(request, "dashboard/branch/index.html", context={})


@login_required(login_url='/login')
def company_admins_list_view(request):
    company_id = request.session.get('company_id', None)
    company = None
    if company_id is not None:
        company = Company.objects.get(pk=company_id)
    elif request.user.company:
        company = request.user.company

    owner_group = Group.objects.get(name=DefaultGroups.AACOUNT_HOLDER)

    admin_group = Group.objects.get(name=DefaultGroups.COMPANY_ADMIN)

    owner_users = owner_group.user_set.all()

    owner_users = owner_users.filter(company=company)

    admin_users = admin_group.user_set.all()

    admin_users = admin_users.filter(company=company)

    users = []
    for owner_user in owner_users:
        users.append(owner_user)

    for admin_user in admin_users:
        users.append(admin_user)

    # form = AdminUserForm()
    
    # if request.method == 'POST':
    #     form_data = AdminUserForm(request.POST or None)
    #     if form_data.is_valid():            
    #         user = form_data.save(commit=False)
    #         group, created = Group.objects.get_or_create(name = CompanyRoles.COMPANY_ADMIN)
    #         user.company = company
    #         user.set_password(str(user.email))
    #         user.created_by = request.user
    #         user.save()

    #         # Add user to group
    #         user.groups.add(group)

    #         UserRoleTrail.objects.create(company=company,user=user, group=group)

    #         return JsonResponse({'success': True, 'email': form_data.cleaned_data['email']})
    #     else:
    #         return JsonResponse({'success': False, 'errors': form_data.errors})
    
    context = {
        'users': users, 
        # 'form': form
        }

    return render(request, "user/accounts/admin/index.html", context = context)

@login_required(login_url='/login')
def company_managers_list_view(request):
    company_id = request.session.get('company_id', None)
    branch_id = request.session.get('branch_id', None)
    company = None
    if company_id is not None:
        company = Company.objects.get(pk=company_id)
    elif request.user.company:
        company = request.user.company

    branch = None
    if branch_id is not None:
        branch = CompanyBranch.objects.get(pk=branch_id)

    companyStaffs = CompanyStaff.objects.filter(company = company)
    users = []

    for companyStaff in companyStaffs:
        users.append(companyStaff.user)

    # if request.method == 'POST':
    #     form_data = ManagerUserForm(request.POST,company = company)
    #     if form_data.is_valid():
    #         branch = form_data.cleaned_data.pop("branch")

    #         # Create the user
    #         user = form_data.save(commit=False)
    #         user.company = company 
    #         user.set_password(str(user.email))
    #         user.created_by = request.user
    #         user.save()

    #         companyStaff = CompanyStaff.objects.create(user=user,company=company,branch=branch)

    #         group, created = Group.objects.get_or_create(name = BranchRoles.BRANCH_MANAGER)
    #         user.groups.add(group)

    #         UserRoleTrail.objects.create(company=company,user=user, group=group)

    #         return JsonResponse({'success': True, 'manager_id': companyStaff.id})
    #     else:
    #         return JsonResponse({'success': False, 'errors': form_data.errors})

    # form = ManagerUserForm(company = company)

    context = {
    'users': users, 
    # 'form': form
    }

    return render(request, "user/accounts/manager/index.html", context = context)

@login_required(login_url='/login')
def company_pos_attendants_list_view(request, bId):
    company_id = request.session.get('company_id', None)
    branch_id = request.session.get('branch_id', None)
    company = None
    if company_id is not None:
        company = Company.objects.get(pk=company_id)
    elif request.user.company:
        company = request.user.company

    branch = None
    if branch_id is not None:
        branch = CompanyBranch.objects.get(pk=branch_id)
    else:
        branch = CompanyBranch.objects.get(pk=bId)

    pos_attendants = PosAttendant.objects.filter(company = company, branch = branch)
    users = []

    for pos_attendant in pos_attendants:
        users.append(pos_attendant.user)

    # if request.method == 'POST':
    #     form = CompanyPosAttendantForm(request.POST,branch=branch)
    #     if form.is_valid():
    #         pos = form.cleaned_data.pop("pos")

    #         # Create the user
    #         user = form.save(commit=False)
    #         user.company = company 
    #         user.set_password(str(user.email))
    #         user.created_by = request.user
    #         user.save()

    #         staff = BranchStaff.objects.create(user=user,company=company,branch=branch)
    #         attendant = PosAttendant.objects.create(staff=staff,pos=pos)

    #         group, created = Group.objects.get_or_create(name = BranchRoles.POS_ATTENDANT)
    #         user.groups.add(group)

    #         return JsonResponse({'success': True, 'attendant_id': attendant.id})
    #     else:
    #         return JsonResponse({'success': False, 'errors': form.errors})

    # form = PosUserForm(branch=branch)

    context = {
    'users': users, 
    # 'form': form
    }

    return render(request, "user/accounts/manager/index.html", context = context)

##3####################- ALL -############################

def users_and_roles_list(request):
    groups_static = []
    default_groups = DefaultGroups.choices
    for default_group in default_groups:
        group, created = Group.objects.get_or_create(name = default_group[0])
        groups_static.append(group)

    # app_roles = AppRoles.choices
    # for app_role in app_roles:
    #     group, created = Group.objects.get_or_create(name = app_role[0])
    #     groups_static.append(group)
    # company_roles = CompanyRoles.choices
    # for company_role in company_roles:
    #     group, created = Group.objects.get_or_create(name = company_role[0])
    #     groups_static.append(group)
    # branch_roles = BranchRoles.choices
    # for branch_role in branch_roles:
    #     group, created = Group.objects.get_or_create(name = branch_role[0])
    #     groups_static.append(group)

    groups_dynamic = Group.objects.exclude(name__in=[group.name for group in groups_static])
    users = User.objects.all()
    superUserForm = AppUserForm(prefix="superUserForm")

    context = {
        "users" : users,
        "groups_static" : groups_static,
        "groups_dynamic" : groups_dynamic,
        "superUserForm" : superUserForm,
        }
    
    if request.method == 'POST':
        form_prefix = request.POST.get('form_prefix')

        if form_prefix == 'superUserForm':
            form_data = AppUserForm(request.POST or None,prefix="superUserForm")
            # print(form_data)
            if form_data.is_valid():
                user = form_data.save(commit=False)
                user.set_password(str(user.email))
                user.created_by = request.user
                user.save()
                return JsonResponse({'success': True, 'email': form_data.cleaned_data['email']})
            else:
                return JsonResponse({'success': False, 'errors': form_data.errors})

    
    # if request.method == 'POST':
    #     form_prefix = request.POST.get('form_prefix')

    #     if form_prefix == 'superUserForm':
    #         form_data = AppUserForm(request.POST or None,prefix="superUserForm")
    #         if form_data.is_valid():
    #             if form_data.cleaned_data['role'] == CompanyRoles.COMPANY_OWNER:
    #                 if form_data.cleaned_data['company'] is None:
    #                     form_data.errors['company'] = ['This field is required!']
    #                     return JsonResponse({'success': False, 'errors': form_data.errors})
                
    #             user = form_data.save(commit=False)
    #             if form_data.cleaned_data['role'] == AppRoles.APP_ADMIN:
    #                 group, created = Group.objects.get_or_create(name = AppRoles.APP_ADMIN)
    #                 user.is_superuser = True
    #                 user.is_staff = True
    #                 user.company = None
    #             if form_data.cleaned_data['role'] == AppRoles.APP_MANAGER:
    #                 group, created = Group.objects.get_or_create(name = AppRoles.APP_MANAGER)
    #                 user.is_superuser = False
    #                 user.is_staff = True
    #                 user.company = None
    #             if form_data.cleaned_data['role'] == CompanyRoles.COMPANY_OWNER:
    #                 group, created = Group.objects.get_or_create(name = CompanyRoles.COMPANY_OWNER)
    #                 user.is_superuser = False
    #                 user.is_staff = False
    #                 user.company = form_data.cleaned_data['company']
            
    #             user.set_password(str(user.email))
    #             user.created_by = request.user
    #             user.save()

    #             # Add user to group
    #             user.groups.add(group)

    #             return JsonResponse({'success': True, 'email': form_data.cleaned_data['email']})
    #         else:
    #             return JsonResponse({'success': False, 'errors': form_data.errors})

    return render(request, "user/super/list/index.html", context=context)


@login_required(login_url='/login')
def role_permissions_list(request, id):
    group = Group.objects.get(pk=id)
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

@login_required(login_url='/login')
def company_list(request):
    # companies = Company.objects.all()
    companies = Company.objects1.get_queryset(request.user).all()
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.pop("first_name")
            last_name = form.cleaned_data.pop("last_name")
            email = form.cleaned_data.pop("email")
            phone_number = form.cleaned_data.pop("phone_number")
            if User.objects.filter(email = email).exists():
                form.errors['email'] = ['Email Already Exists!']
                return JsonResponse({'success': False, 'errors': form.errors})
            
            company = form.save() 
            # Create Comapny Owner
            user = User(first_name = first_name,last_name = last_name,email = email,phone_number = phone_number)
            user.is_superuser = False
            user.is_staff = False
            user.company = company
            user.set_password(str(user.email))
            user.created_by = request.user
            user.save()

            # Assign User To Group
            group, created = Group.objects.get_or_create(name = DefaultGroups.ACCOUNT_HOLDER)
            user.groups.add(group)

            return JsonResponse({'success': True, 'company_id': company.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CompanyForm()
    return render(request, "company/list/index.html", context={'form': form, 'companies': companies})


@login_required(login_url='/login')
@csrf_exempt  # Use this decorator if you don't need CSRF protection for this view
def company_deactivate(request,company_id):
    if request.method == 'POST':
        try:
            company = get_object_or_404(Company, id=company_id)
            company.delete()
            return JsonResponse({'message': 'Company deactivated successfully'})
        except Exception as e:
            return HttpResponseServerError({'message': f'Failed to delete company. Error: {str(e)}'})


@login_required(login_url='/login')
@csrf_exempt  # Use this decorator if you don't need CSRF protection for this view
def company_delete(request,company_id):
    if request.method == 'POST':
        try:
            company = get_object_or_404(Company, id=company_id)
            print(company)
            company.hard_delete()
            return JsonResponse({'message': 'Company deleted successfully'})
        except Exception as e:
            print(e)
            return HttpResponseServerError({'message': f'Failed to delete company. Error: {str(e)}'})


##3####################- Company -############################
@login_required(login_url='/login')
def company_detail(request, company_id):
    company = Company.objects.get(pk=company_id)
    request.session['company_id'] = company.id
    request.session['company_name'] = company.name
    if request.method == 'POST':
        form = CompanyForm(request.POST,instance=company)
        if form.is_valid():
            company = form.save()
            return JsonResponse({'success': True, 'company_id': company.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}) 
    else:
        form = CompanyForm(instance=company)
    context = {
        'form': form,
        'company': company
    }
    return render(request, "dashboard/company/index.html", context=context)


@login_required(login_url='/login')
def company_branches_list(request, company_id):
    company = None
    if company_id is not None:
        company = Company.objects.get(pk=company_id) 
    elif request.user.company:
        company = request.user.company

    if request.user.is_superuser:
        branches = CompanyBranch.objects.all()
    else:
        branches = CompanyBranch.objects.filter(company=company)

    if request.method == 'POST':
        form = CompanyBranchForm(request.POST)
        if form.is_valid():
            branch = form.save(commit=False)
            branch.created_by = request.user 
            branch.company = company
            branch.save()
            return JsonResponse({'success': True, 'branch_id': branch.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CompanyBranchForm()
    
    context = {
        'form': form,
        'company': company,
        'branches': branches
    }
    return render(request, "branch/list/index.html", context = context)


@login_required(login_url='/login')
def company_pos_list(request, company_id):
    company = None
    if company_id is not None:
        company = Company.objects.get(pk=company_id)
    elif request.user.company:
        company = request.user.company

    context = { "company": company }
    return render(request, "pos/index.html", context = context)

@login_required(login_url='/login')
def company_users_list(request, company_id):
    company = None
    if company_id is not None:
        company = Company.objects.get(pk=company_id)
    elif request.user.company:
        company = request.user.company

    users = User.objects.filter(company=company)

    context = {
        "users" : users,
        "company": company
    }

    return render(request, "user/company/list/index.html", context=context)

@login_required(login_url='/login')
def company_users_new(request, company_id):
    company = None
    if company_id is not None:
        company = Company.objects.get(pk=company_id)
    elif request.user.company:
        company = request.user.company

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
            branches = form_data.cleaned_data.pop('branches', [])

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

            for branch in branches:
                if not CompanyStaff.objects.filter(company = company,branch = branch,user =  user).exists():
                    CompanyStaff.objects.create(
                        company = company,
                        branch = branch,
                        user =  user,
                        created_by = request.user)

                # print(staff)

            return redirect('user:company-users-list', company_id=company_id)

        context['form'] = form_data

    return render(request, "user/company/new/index.html", context=context)

@login_required(login_url='/login')
def company_roles_list(request, company_id):
    company = None
    if company_id is not None:
        company = Company.objects.get(pk=company_id)
    elif request.user.company:
        company = request.user.company

    groups_static = []
    default_groups = DefaultGroups.choices
    for default_group in default_groups:
        group, created = Group.objects.get_or_create(name = default_group[0])
        groups_static.append(group)

    # groups_dynamic = Group.objects.filter(name__startswith=f"{company.id}_")

    # groups_dynamic = []
    company_groups =  CompanyGroup.objects.filter(company = company)
    # print(company_groups[0].name)
    # for cg in company_groups:
    #     groups_dynamic.append(cg.group)
    # print(groups_dynamic)

    #groups_dynamic = Group.objects.exclude(name__in=[group.name for group in groups_static])

    context = {
        "company": company,
        "groups_static": groups_static,
        # "groups_dynamic": groups_dynamic,
        "company_groups": company_groups
    }

    return render(request, "role/company/list/index.html", context=context)

@login_required(login_url='/login')
def company_roles_new(request, company_id):
    company = None
    if company_id is not None:
        company = Company.objects.get(pk=company_id)
    elif request.user.company:
        company = request.user.company

    # Specify the app labels you want to include
    model_names = ['company','companybranch','companypos']

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
def company_roles_delete(request, company_id, group_id):
    company = None
    if company_id is not None:
        company = Company.objects.get(pk=company_id)
    elif request.user.company:
        company = request.user.company

    group = Group.objects.get(pk = group_id)

    if CompanyGroup.objects.filter(company = company, group = group).exists():
        group.delete()

    return redirect('user:company-roles-list', company_id=company_id)
    


##3####################- Branch -############################
@login_required(login_url='/login')
def company_branch_detail(request, company_id, branch_id):
    company = Company.objects.get(id=company_id)
    branch = CompanyBranch.objects.get(id=branch_id)
    context = {
        "company": company,
        "branch": branch,
    }
    return render(request, "dashboard/branch/index.html", context=context)

def company_branch_pos_list(request, company_id, branch_id):
    company = None
    if company_id is not None:
        company = Company.objects.get(pk=company_id)
    elif request.user.company:
        company = request.user.company

    branch = None
    if branch_id is not None:
        branch = CompanyBranch.objects.get(pk=branch_id)

    pos_list = CompanyPos.objects1.get_queryset(request.user,branch=branch).all()

    if request.method == 'POST':
        form = CompanyPosForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # pos = form.save(commit=False)
            # pos.created_by = request.user
            # pos.company = company
            # pos.branch = branch
            # pos.save()  
            return JsonResponse({'success': True, 'pos_id': "pos.id"})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    form = CompanyPosForm()
    context = {
        "company": company, "branch": branch,
        "pos_list": pos_list, "form": form}
    
    print("Here")
    return render(request, "pos/list/index.html", context=context)


def company_branch_users_list(request, company_id, branch_id):
    company = Company.objects.get(id=company_id)
    branch = CompanyBranch.objects.get(id=branch_id)
    context = {
        "company": company,
        "branch": branch,
    }
    return render(request, "user/branch/list/index.html", context=context)


##3####################- Branch -############################
@login_required(login_url='/login')
def company_branch_pos_detail(request, company_id, branch_id, pos_id):
    company = Company.objects.get(id=company_id)
    branch = CompanyBranch.objects.get(id=branch_id)
    pos = CompanyPos.objects.get(id=pos_id)
    context = {
        "company": company,
        "branch": branch,
        "pos":pos
    }
    return render(request, "pos/detail/index.html", context=context)

def company_branch_pos_users_list(request, company_id, branch_id,pos_id):
    company = Company.objects.get(id=company_id)
    branch = CompanyBranch.objects.get(id=branch_id)
    pos = CompanyPos.objects.get(id=pos_id)
    context = {
        "company": company,
        "branch": branch,
        "pos":pos
    }
    return render(request, "user/accounts/manager/index.html", context=context)


