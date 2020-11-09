from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('registrationAgent/',views.RegistrationAgentView.as_view(),name='registrationAgent'),
    path('registrationCustomer/',views.RegistrationCustomerView.as_view(),name='registrationCustomer'),
    path('loginCustomer/',views.LoginCustomerView.as_view(),name='loginCustomer'),
    path('loginAgent/',views.LoginAgentView.as_view(),name='loginAgent'),
]
