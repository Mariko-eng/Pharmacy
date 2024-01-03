from django.shortcuts import render, redirect
from pharmacy.utils import generate_random_number
from .forms import CompanyApplicationRegisterForm
from .forms import CompanyAccountActivationForm
from .forms import CompanyAdminRegisterForm
from .models import CompanyApplication,Company
from django.contrib import messages
from user.models import AccountTypes ,User, UserProfile


################### - Company Application - ################# 

def company_application_add_view(request):
    form = CompanyApplicationRegisterForm()

    context = {"form": form}

    if request.method == "POST":
        form = CompanyApplicationRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save()
            code = generate_random_number()
            print("code is : " + str(code))
            application.activation_code = code
            application.save()

            messages.info(request, "Application is submitted successfully!")
            # return redirect('user:home')
        else:
            messages.error(request,"Failed To Submit Application!")
    else:
        form = CompanyApplicationRegisterForm()

    context = { "form": form }
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
                
                name = companyApplication.name
                phone = companyApplication.phone
                email = companyApplication.email
                location = companyApplication.location
                logo = companyApplication.location
                activation_code = companyApplication.activation_code

                company = Company.objects.get_or_create(
                    name = name,
                    phone = phone,
                    email = email,
                    location = location,
                    logo = logo,
                    activation_code = activation_code
                )

                if companyApplication.status != "APPROVED":
                    companyApplication.status = "APPROVED"
                    companyApplication.save()

                messages.info(request, "Company account activated successfully!")
                return redirect('company:company-admin-user-register', company_id = company.id)
            else:
                messages.error(request,"Failed To Activate Company!")
                form.errors['activation_code'] = ['You have submitted a Wrong code!'] 
        else:
            messages.error(request,"Failed To Submit Application!")

    context = { "form": form }
    return render(request, 'company/activation/index.html', context=context)


def company_admin_user_register_view(request, company_id):
    company = Company.objects.get(pk = company_id)

    form = CompanyAdminRegisterForm()
    context = { "form": form }

    if request.method == "POST":
        form = CompanyAdminRegisterForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            password2 = form.cleaned_data.get('password2')

            user = User(
               first_name = first_name,
               last_name = last_name,
               phone = phone,
               email = email,
            )
            user.account_type = AccountTypes.COMPANY_ADMIN
            user.set_password(str(password2))
            user.save()

            UserProfile.objects.get_or_create(
                user = user,
                company = company,
                user_role = AccountTypes.COMPANY_ADMIN
            )

            messages.info(request, "Company admin account created successfully!")
            return redirect('user:home')
        else:
            messages.error(request,"Failed to create company admin account!")
            
    return render(request, 'company/application/new/index.html', context=context)
    

def company_application_list_view(request):
    data = CompanyApplication.objects.all()

    context = { "data" : data }
    
    return render(request, 'company/new/index.html', context = context)


def company_application_detail_view(request, pk):
    data = CompanyApplication.objects.all(pk = pk)

    context = { "data" : data }
    
    return render(request, 'company/new/index.html', context = context)


def company_application_edit_view(request, pk):
    data = CompanyApplication.objects.all(pk = pk)

    context = { "data" : data }
    
    return render(request, 'company/new/index.html', context = context)


def company_application_delete_view(request, pk):
    data = CompanyApplication.objects.all(pk = pk)

    context = { "data" : data }
    
    return render(request, 'company/new/index.html', context = context)


###################### - Company - ####################

def company_list_view(request):
    data = Company.objects.all()

    context = { "data" : data }
    
    return render(request, 'company/new/index.html', context = context)


def company_detail_view(request, pk):
    data = Company.objects.all(pk = pk)

    context = { "data" : data }
    
    return render(request, 'company/new/index.html', context = context)


def company_edit_view(request, pk):
    data = Company.objects.all(pk = pk)

    context = { "data" : data }
    
    return render(request, 'company/new/index.html', context = context)


def company_delete_view(request, pk):
    data = Company.objects.all(pk = pk)

    context = { "data" : data }
    
    return render(request, 'company/new/index.html', context = context)