from django.shortcuts import render
from django.http import request

def index(request):
    return render(request, 'home.html')

def issued(request):
    return render(request, 'Issued.html')

def sidebar(request):
    return render(request, 'sidebar.html')