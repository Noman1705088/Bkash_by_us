from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from .models import SendMoney,CashIn,CashOut,HistoryOf
from dashboard.models import execute_sql
from django.http import Http404

class SendMoneyView(View):
    def get(self,request):
        if request.session.get('CUSTOMER'):
            return render(request,'services/sendMoney.html')
    def post(self,request):
        reciver_mobile_no = request.POST.get('to_mobile_no')
        sender_id = request.session.get('CUSTOMER')
        amount = int(request.POST.get('amount'))

        trans_failed = False
        send_money_trans = SendMoney(sender_id,reciver_mobile_no,amount,request.POST.get('password'))
        if send_money_trans.validMobileNo() and send_money_trans.hasEnoughMoney() and send_money_trans.isCorrectPass():
            send_money_trans.doTransiction()
        else:
            trans_failed = True
            return render(request,'services/sendMoney.html',{'message':trans_failed})

        return render(request,'services/sendMoney.html',{'message':trans_failed})

class CashInView(View):
    def get(self,request):
        if request.session.get('AGENT'):
            return render(request,'services/cashIn.html')
    def post(self,request):
        reciver_mobile_no = request.POST.get('to_mobile_no')
        sender_id = request.session.get('AGENT')
        amount = int(request.POST.get('amount')) 

        trans_failed = False   
        cash_in_trans = CashIn(sender_id,reciver_mobile_no,amount,request.POST.get('password'))
        if cash_in_trans.validMobileNo() and cash_in_trans.hasEnoughMoney() and cash_in_trans.isCorrectPass():
            cash_in_trans.doTransiction()
        else:
            trans_failed = True
            return render(request,'services/cashIn.html',{'message':trans_failed})

        return render(request,'services/cashIn.html',{'message':trans_failed})

class CashOutView(View):
    def get(self,request):
        if request.session.get('CUSTOMER'):
            return render(request,'services/cashOut.html')
    def post(self,request):
        reciver_mobile_no = request.POST.get('to_mobile_no')
        sender_id = request.session.get('CUSTOMER')
        amount = int(request.POST.get('amount')) 

        trans_failed = False   
        cash_out_trans = CashOut(sender_id,reciver_mobile_no,amount,request.POST.get('password'))
        if cash_out_trans.validMobileNo() and cash_out_trans.hasEnoughMoney() and cash_out_trans.isCorrectPass():
            cash_out_trans.doTransiction()
        else:
            trans_failed = True
            return render(request,'services/cashOut.html',{'message':trans_failed})

        return render(request,'services/cashOut.html',{'message':trans_failed})

class HistoryView(View):
    def get(self,request):
        sender = 0
        if request.session.get('CUSTOMER'):
            sender= 'CUST_' + str(request.session.get('CUSTOMER'))
            sql='SELECT CUSTOMER_BALANCE FROM CUSTOMER WHERE CUSTOMER_ID=:cust'
            balance = execute_sql(sql,[request.session.get('CUSTOMER')],False,True)[0][0]

            context = {'NAME':request.COOKIES.get('NAME'),'PHOTO':request.COOKIES.get('PHOTO'),\
                'MOBILE':request.COOKIES.get('MOBILE'),'TYPE':'customer','BALANCE':balance}
        elif request.session.get('AGENT'):
            sender= 'AGEN_' + str(request.session.get('AGENT'))
            sql='SELECT AGENT_BALANCE FROM AGENT WHERE AGENT_ID=:agent'
            balance = execute_sql(sql,[request.session.get('AGENT')],False,True)[0][0]

            context = {'NAME':request.COOKIES.get('NAME'),'PHOTO':request.COOKIES.get('PHOTO'),\
                'MOBILE':request.COOKIES.get('MOBILE'),'TYPE':'agent','BALANCE':balance}
        else:
            return Http404('Not verified user')

        history = HistoryOf(sender)
        context['HISTORY'] = history.getHistory()

        return render(request,'services/history.html',context)

         
