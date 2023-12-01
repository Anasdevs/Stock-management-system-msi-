from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('issued/', views.issued, name='issued'),
    path('sidebar/', views.sidebar, name='sidebar'),
    path('reports/', views.reports, name="reports"),
]