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
]
