from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import CompanyForm
from .models import Company, User

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
def company_view(request):
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
