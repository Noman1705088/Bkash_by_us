from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'services'

urlpatterns = [
    path('sendMoney/',views.SendMoneyView.as_view(),name='sendMoney'),
    path('cashIn/',views.CashInView.as_view(),name='cashIn'),
    path('cashOut/',views.CashOutView.as_view(),name='cashOut'),
    path('history/',views.HistoryView.as_view(),name='history'),
]
