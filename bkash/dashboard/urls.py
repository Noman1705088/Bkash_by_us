from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('registration/',views.RegistrationView.as_view(),name='registration'),
    path('login/',views.LoginView.as_view(),name='login'),
]
