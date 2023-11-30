from django.shortcuts import render
from django.http import request
from .forms import IssuedForm 
from .models import IssuedItem

def index(request):
    return render(request, 'home.html')

def issued(request):
    return render(request, 'Issued.html')

def sidebar(request):
    return render(request, 'sidebar.html')

def reports(request):
    return render(request, 'reports.html')

# from django.shortcuts import render, redirect 

def purchase(request):
    # Use lowercase variable names for consistency
    issued_items = IssuedItem.objects.all()
    
    # Use the form class, not an instance, and fix the indentation
    form = IssuedForm()

    if request.method == 'POST':
        form = IssuedForm(request.POST)
        if form.is_valid():
            form.save()
            return ('success_page')  # Redirect to a success page or another URL

    # Use an empty dictionary for an empty form, not an empty tuple
    context = {'issued_items': issued_items, 'form': form}
    return render(request, 'purchase.html', context)
