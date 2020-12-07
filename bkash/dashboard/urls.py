from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('registrationAgent/', views.RegistrationAgentView.as_view(),
         name='registrationAgent'),
    path('registrationCustomer/', views.RegistrationCustomerView.as_view(),
         name='registrationCustomer'),
    path('registrationAdmin/', views.RegistrationAdminView.as_view(),
         name='registrationAdmin'),
    path('registrationMerchant/', views.RegistrationMerchantView.as_view(),
         name='registrationMerchant'),
     path('registrationServiceProvider/',views.RegistrationServiceProviderView.as_view(),
          name='registrationServiceProvider'),
    path('registrationOperator/', views.RegistrationOperatorView.as_view(),
         name='registrationOperator'),
    path('loginCustomer/', views.LoginCustomerView.as_view(), name='loginCustomer'),
    path('loginAgent/', views.LoginAgentView.as_view(), name='loginAgent'),
    path('loginAdmin/', views.LoginAdminView.as_view(), name='loginAdmin'),
    path('loginMerchant/', views.LoginMerchantView.as_view(), name='loginMerchant'),
]
