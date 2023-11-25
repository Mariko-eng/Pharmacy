from django.shortcuts import render


def index(request):
    context = {}
    return render(request, "user/index.html", context=context)
