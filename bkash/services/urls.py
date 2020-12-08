from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'services'

urlpatterns = [
    path('sendMoney/',views.SendMoneyView.as_view(),name='sendMoney'),
    path('cashIn/',views.CashInView.as_view(),name='cashIn'),
    path('cashOut/',views.CashOutView.as_view(),name='cashOut'),
    path('payBill/',views.PayBillView.as_view(),name='payBill'),
    path('payBill/<int:service_id>/',views.PayBillView.as_view(),name='payBill'),
    path('history/',views.HistoryView.as_view(),name='history'),
    path('payment/', views.MerchantPaymentView.as_view(), name='merchantpayment'),
    path('recharge/', views.MobileRechargeView.as_view(), name='mobileRecharge')
]
