from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import CompanyForm,SuperUserForm,CompanyAdminUserForm
from django.contrib.auth.models import Group, Permission
from .models import Role, User, Company ,CompanyAdmin
from django.contrib.auth.hashers import make_password

# custom 404 view
def custom_404(request, exception):
    return render(request, '404.html', status=404)

# @unauthenticated_user
def index(request):
    next_url = request.GET.get('next')  # Get the value of 'next' parameter from the query string

    context = {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('user:home-super')
        
        return redirect('user:home')
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        # print(email)
        # print(password)
        
        user = authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)

            if next_url:
                return redirect(next_url)  # Redirect to the URL specified in 'next' parameter
            
            if request.user.is_superuser:
                return redirect('user:home-super')
            return redirect('user:home')
        else:
            messages.info(request, "Please Provide A Valid Username And Paassword")

    return render(request,'auth/login/index.html',context)
    # return render(request,'accounts/login.html',context)

def logoutView(request):
    # Clear the session data
    request.session.flush()
    
    logout(request)
    return redirect('user:login')

@login_required(login_url='/login')
def home_view(request):
    return render(request, "home/main/index.html", context={})

@login_required(login_url='/login')
def home_super_view(request):
    return render(request, "home/super/index.html", context={})

@login_required(login_url='/login')
def super_all_users_view(request):
    global_roles = Role.choices
    groups_static = []
    for role in global_roles:
        group, created = Group.objects.get_or_create(name = role[0])
        groups_static.append(group)

    groups_dynamic = Group.objects.exclude(name__in=[group.name for group in groups_static])
    users = User.objects.all()
    superUserForm = SuperUserForm(prefix="superUserForm")
    adminUserForm = CompanyAdminUserForm(prefix="adminUserForm")

    context = {
        "users" : users,
        "groups_static" : groups_static,
        "groups_dynamic" : groups_dynamic,
        "superUserForm" : superUserForm,
        "adminUserForm" : adminUserForm,
        }
    if request.method == 'POST':
        form_prefix = request.POST.get('form_prefix')
        # print(form_prefix)

        if form_prefix == 'superUserForm':
            superUserForm_data = SuperUserForm(request.POST or None,prefix="superUserForm")
            if superUserForm_data.is_valid():
                super_user = superUserForm_data.save(commit=False)
                super_user.is_superuser = True
                super_user.is_staff = True
                super_user.password = make_password(str(super_user.email))
                super_user.created_by = request.user
                super_user.save()

                return JsonResponse({'success': True, 'email': super_user.name})
            else:
                return JsonResponse({'success': False, 'errors': superUserForm_data.errors})

        if form_prefix == 'adminUserForm':
            adminUserForm_data = CompanyAdminUserForm(request.POST or None,prefix="adminUserForm")
            if adminUserForm_data.is_valid():
                admin_user = adminUserForm_data.save(commit=False)
                admin_user.password = make_password(str(admin_user.email))
                admin_user.created_by = request.user
                admin_user.save()

                CompanyAdmin.objects.create(user = admin_user, company = admin_user.company, created_by = admin_user.created_by)

                group, created = Group.objects.get_or_create(name = Role.COMPANY_ADMIN)
                admin_user.groups.add(group)

                return JsonResponse({'success': True, 'email': admin_user.email})
            else:
                return JsonResponse({'success': False, 'errors': adminUserForm_data.errors})

    return render(request, "user/super/index.html", context=context)

@login_required(login_url='/login')
def super_roles_permissions_edit_view(request, id):
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
        "all_permissions" : all_permissions
    }

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
        
        # return redirect('user:super-roles-permissions-edit', id=id)

    return render(request, "user/super/roles/index.html", context= context)


@login_required(login_url='/login')
def super_all_companies_view(request):
    companies = Company.objects.all()
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            return JsonResponse({'success': True, 'company_id': company.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CompanyForm()
    return render(request, "company/list/index.html", context={'form': form, 'companies': companies})

#  By the Super User
@login_required(login_url='/login')
def company_home_view(request, id):
    company = Company.objects.get(pk=id)
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
    return render(request, "company/home/index.html", context={'form': form, 'company': company})


# def index(request): 
#     form = NameForm()
#     context = {
#         'form': form
#     }
#     # if this is a POST request we need to process the form data
#     if request.method == "POST":
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)

#         # Check if the name is "Mark" and add a custom error if true
#         if form.data.get('name', '').lower() == 'mark':
#             form.add_error('name', forms.ValidationError("Bad name: 'Mark' is not allowed."))

#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             print("Valid")
#             context['form'] = form
#         else:
#             print("Invalid")
#             # for field, errors in form.errors.items():
#             #     form[field].field.widget.attrs['class'] += ' is-invalid'
#             #     print(form[field])
#             context['form'] = form

#     return render(request, "user/index.html", context=context)
