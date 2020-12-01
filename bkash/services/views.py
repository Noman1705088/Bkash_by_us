from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from .models import SendMoney,CashIn,CashOut,HistoryOf
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
        send_money_trans = SendMoney(sender_id,reciver_mobile_no,amount)
        if send_money_trans.validMobileNo() and send_money_trans.hasEnoughMoney():
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
        cash_in_trans = CashIn(sender_id,reciver_mobile_no,amount)
        if cash_in_trans.validMobileNo() and cash_in_trans.hasEnoughMoney():
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
        cash_out_trans = CashOut(sender_id,reciver_mobile_no,amount)
        if cash_out_trans.validMobileNo() and cash_out_trans.hasEnoughMoney():
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
            context = {'NAME':request.COOKIES.get('NAME'),'PHOTO':request.COOKIES.get('PHOTO'),\
                'MOBILE':request.COOKIES.get('MOBILE'),'TYPE':'customer'}
        elif request.session.get('AGENT'):
            sender= 'AGEN_' + str(request.session.get('AGENT'))
            context = {'NAME':request.COOKIES.get('NAME'),'PHOTO':request.COOKIES.get('PHOTO'),\
                'MOBILE':request.COOKIES.get('MOBILE'),'TYPE':'agent'}
        else:
            return Http404('Not verified user')

        history = HistoryOf(sender)
        context['HISTORY'] = history.getHistory()

        return render(request,'services/history.html',context)

         
