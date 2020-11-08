from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'home'

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('user_home/',views.User_homeView.as_view(),name='user_home'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
]
