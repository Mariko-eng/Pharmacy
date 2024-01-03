from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse,HttpResponseServerError
from django.contrib.auth.models import Group, Permission
from .models import User, AccountTypes
from .models import Company


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

    if request.user.account_type == AccountTypes.APP_ADMIN:
        return render(request, "dashboard/super/index.html", context={})
    
    if request.user.account_type == AccountTypes.COMPANY_ADMIN:
        return render(request, "dashboard/super/index.html", context={})
    
    if request.user.account_type == AccountTypes.STORE_MANAGER:
        return render(request, "dashboard/super/index.html", context={})
    
    if request.user.account_type == AccountTypes.CASHIER:
        return render(request, "dashboard/super/index.html", context={})
    
    return HttpResponseRedirect('Page Not Found!')



