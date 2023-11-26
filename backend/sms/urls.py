from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('assigned/', views.assigned, name='assigned'),
  
]