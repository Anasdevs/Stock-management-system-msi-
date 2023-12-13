from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('purchase/', views.index, name='index'),
    path('issued/', views.issued, name='issued'),
    path('profile/',views.profile, name='profile'),
]