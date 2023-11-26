from django.shortcuts import render

def index(request):
    return render(request, 'home.html')

def assigned(request):
    return render(request, 'Assigned.html')