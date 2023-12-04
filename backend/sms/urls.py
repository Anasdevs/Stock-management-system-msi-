from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('issued/', views.issued, name='issued'),
    path('reports/', views.reports, name="reports"),
    path('dashboard/', views.dashboard, name="dashboard")
]