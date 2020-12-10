from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('updateUser/', views.UpdateUserView.as_view(), name='updateUser'),
    path('userInfo/', views.UserInfoView.as_view(), name='userInfo'),
    path('addBranch/', views.addBranchView.as_view(), name='addBranch'),
    path('customerInfo/', views.customerInfoView.as_view(), name='customerInfo'),
    path('agentInfo/', views.agentInfoView.as_view(), name='agentInfo'),
    path('merchantInfo/', views.merchantInfoView.as_view(), name='merchantInfo'),
    path('operatorInfo/', views.operatorInfoView.as_view(), name='operatorInfo'),
    path('serviceInfo/', views.serviceProviderInfoView.as_view(), name='serviceInfo')
]
