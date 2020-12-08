from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from .models import SendMoney,CashIn,CashOut,HistoryOf,PayBill, MerchantPayment,MobileRecharge
from dashboard.models import execute_sql
from django.http import Http404


class SendMoneyView(View):
    def get(self, request):
        if request.session.get('CUSTOMER'):
            return render(request, 'services/sendMoney.html')

    def post(self, request):
        reciver_mobile_no = request.POST.get('to_mobile_no')
        sender_id = request.session.get('CUSTOMER')
        amount = int(request.POST.get('amount'))

        trans_failed = False
        send_money_trans = SendMoney(
            sender_id, reciver_mobile_no, amount, request.POST.get('password'))
        if send_money_trans.validMobileNo() and send_money_trans.hasEnoughMoney() and send_money_trans.isCorrectPass():
            send_money_trans.doTransiction()
            return redirect('services:history')
        else:
            trans_failed = True
            return render(request, 'services/sendMoney.html', {'message': trans_failed})

        return render(request, 'services/sendMoney.html', {'message': trans_failed})


class CashInView(View):
    def get(self, request):
        if request.session.get('AGENT'):
            return render(request, 'services/cashIn.html')

    def post(self, request):
        reciver_mobile_no = request.POST.get('to_mobile_no')
        sender_id = request.session.get('AGENT')
        amount = int(request.POST.get('amount'))

        trans_failed = False
        cash_in_trans = CashIn(sender_id, reciver_mobile_no,
                               amount, request.POST.get('password'))
        if cash_in_trans.validMobileNo() and cash_in_trans.hasEnoughMoney() and cash_in_trans.isCorrectPass():
            cash_in_trans.doTransiction()
            return redirect('services:history')
        else:
            trans_failed = True
            return render(request, 'services/cashIn.html', {'message': trans_failed})

        return render(request, 'services/cashIn.html', {'message': trans_failed})


class CashOutView(View):
    def get(self, request):
        if request.session.get('CUSTOMER'):
            return render(request, 'services/cashOut.html')

    def post(self, request):
        reciver_mobile_no = request.POST.get('to_mobile_no')
        sender_id = request.session.get('CUSTOMER')
        amount = int(request.POST.get('amount'))

        trans_failed = False
        cash_out_trans = CashOut(
            sender_id, reciver_mobile_no, amount, request.POST.get('password'))
        if cash_out_trans.validMobileNo() and cash_out_trans.hasEnoughMoney() and cash_out_trans.isCorrectPass():
            cash_out_trans.doTransiction()
            return redirect('services:history')
        else:
            trans_failed = True
            return render(request, 'services/cashOut.html', {'message': trans_failed})

        return render(request, 'services/cashOut.html', {'message': trans_failed})



class PayBillView(View):
    def get(self,request,service_id=0):
        if (request.session.get('CUSTOMER') or request.session.get('AGENT')) and service_id==0:
            return render(request,'services/payBill.html')
        elif request.session.get('CUSTOMER') or request.session.get('AGENT'):
            context = PayBill().serviceOfID(service_id)
            context['PHOTO'] = request.COOKIES.get('PHOTO')
            return render(request,'services/payBillForm.html',context)
        else:
            return Http404('Wrong Info')
    def post(self,request,service_id=0):
        if (request.session.get('CUSTOMER') or request.session.get('AGENT')) and service_id==0:
            serviceChoice = request.POST.get('choice')
            services = PayBill()
            context = services.servicesOfType(serviceChoice)
            return render(request,'services/payBill.html',context)
        elif request.session.get('CUSTOMER') or request.session.get('AGENT'):
            if request.session.get('CUSTOMER'):
                user_id = request.session.get('CUSTOMER')
                billing_id = request.POST.get('billing_id')
                amount = request.POST.get('amount')
                password = request.POST.get('password')

                if PayBill().isCorrectPass(True,user_id,password) and PayBill().hasEnoughMoney(True,user_id,amount):
                    PayBill().doTransictionCustomer(service_id,user_id,amount,billing_id)
                    return redirect('services:history')
            elif request.session.get('AGENT'):
                user_id = request.session.get('AGENT')
                billing_id = request.POST.get('billing_id')
                amount = int(request.POST.get('amount'))
                password = request.POST.get('password')

                if PayBill().isCorrectPass(False,user_id,password) and PayBill().hasEnoughMoney(False,user_id,amount):
                    PayBill().doTransictionAgent(service_id,user_id,amount,billing_id)
                    return redirect('services:history')
        else:
            return Http404('Wrong Info')               
                


class HistoryView(View):
    def get(self, request):
        sender = 0
        if request.session.get('CUSTOMER'):
            sender= 'USER_' + str(request.session.get('CUSTOMER'))
            sql='SELECT CUSTOMER_BALANCE FROM CUSTOMER WHERE CUSTOMER_ID=:cust'
            balance = execute_sql(sql,[request.session.get('CUSTOMER')],False,True)[0][0]

            context = {'NAME': request.COOKIES.get('NAME'), 'PHOTO': request.COOKIES.get('PHOTO'),
                       'MOBILE': request.COOKIES.get('MOBILE'), 'TYPE': 'customer', 'BALANCE': balance}
        elif request.session.get('AGENT'):
            sender= 'USER_' + str(request.session.get('AGENT'))
            sql='SELECT AGENT_BALANCE FROM AGENT WHERE AGENT_ID=:agent'
            balance = execute_sql(sql,[request.session.get('AGENT')],False,True)[0][0]

            context = {'NAME': request.COOKIES.get('NAME'), 'PHOTO': request.COOKIES.get('PHOTO'),
                       'MOBILE': request.COOKIES.get('MOBILE'), 'TYPE': 'agent', 'BALANCE': balance}
        elif request.session.get('MERCHANT'):
            sender = request.session.get('MERCHANT')
            context = {'NAME': request.COOKIES.get('NAME'), 'PHOTO': request.COOKIES.get('PHOTO'),\
                       'TRADE_LICENSE_NO': request.COOKIES.get('TRADE_LICENSE_NO'), 'TYPE': 'merchant',\
                            'HEAD_OFFICE_LOCATION': request.COOKIES.get('HEAD_OFFICE_LOCATION'),\
                                 'BRANCH': request.COOKIES.get('BRANCH_NAME'), 'OFFER_PERCENT': request.COOKIES.get('OFFER_PERCENT')}

            sql = 'SELECT BRANCH_NAME,BRANCH_ID FROM BRANCH WHERE BRANCH_MERCHANT_ID=:id'
            ans = execute_sql(sql,[sender],False,True)
            cont_mar_his = ans
            i = 0
            for x in ans:
                cont_mar_his[i] = {'NAME_BRANCH':x[0],'BRANCH_HIS':HistoryOf('MERC_'+str(x[1])).getHistory()}
                i = i+1
            context['HISTORY'] = cont_mar_his
            return render(request, 'services/historyMerchant.html', context)
        else:
            return Http404('Not verified user')

        history = HistoryOf(sender)
        context['HISTORY'] = history.getHistory()

        return render(request, 'services/history.html', context)


class MerchantPaymentView(View):
    def get(self, request):
        return render(request, 'services/merchantPayment.html')

    def post(self, request):
        if request.session.get('CUSTOMER'):
            sender_id = request.session.get('CUSTOMER')
            sender_type = "customer"
        elif request.session.get('AGENT'):
            sender_id = request.session.get('AGENT')
            sender_type = "agent"

        merchant_mobile_no = request.POST.get('merchant_mobile_no')
        amount = int(request.POST.get('amount'))
        password = request.POST.get('password')

        merchant_payment_trans = MerchantPayment(
            sender_id, merchant_mobile_no, amount, password, sender_type)
        merchant_payment_failed = False
        if merchant_payment_trans.valid_merchant_mobile_no() and merchant_payment_trans.hasEnoughMoney() and merchant_payment_trans.is_correct_password():
            merchant_payment_trans.do_payment_transaction()
            return redirect('services:history')
        else:
            merchant_payment_failed = True
            return render(request, 'services/merchantPayment.html', {'message': merchant_payment_failed})

        return render(request, 'services/merchantPayment.html', {'message': merchant_payment_failed})
class MobileRechargeView(View):
    def get(self,request):
        return render(request,'services/rechargeMobile.html')
    def post(self,request):
        if request.session.get('CUSTOMER'):
            sender_id = request.session.get('CUSTOMER')
            sender_type = "customer"
        elif request.session.get('AGENT'):
            sender_id = request.session.get('AGENT')
            sender_type = "agent"

        receiver_mobile_no = request.POST.get('to_mobile_no')
        recharge_amount = int(request.POST.get('amount'))
        password = request.POST.get('password')

        mobile_recharge_trans = MobileRecharge(sender_id,receiver_mobile_no,recharge_amount,password,sender_type)
        if mobile_recharge_trans.isOperatorAvailable() and mobile_recharge_trans.hasEnoughMoney() and mobile_recharge_trans.is_correct_password():
            mobile_recharge_trans.make_recharge()
            return redirect('services:history')
        else:
            mobile_recharge_failed = True;
            return render(request, 'services/rechargeMobile.html', {'message': mobile_recharge_failed})


