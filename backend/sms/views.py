from django.shortcuts import render

def index(request):
    return render(request, 'home.html')

def issued(request):
    return render(request, 'Issued.html')