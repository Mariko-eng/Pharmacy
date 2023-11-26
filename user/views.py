from django.shortcuts import render
from django import forms
from .forms import NameForm


def index(request):
    form = NameForm()
    context = {
        'form': form
    }
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)

        # Check if the name is "Mark" and add a custom error if true
        if form.data.get('name', '').lower() == 'mark':
            form.add_error('name', forms.ValidationError("Bad name: 'Mark' is not allowed."))

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print("Valid")
            context['form'] = form
        else:
            print("Invalid")
            # for field, errors in form.errors.items():
            #     form[field].field.widget.attrs['class'] += ' is-invalid'
            #     print(form[field])
            context['form'] = form

    return render(request, "user/index.html", context=context)
