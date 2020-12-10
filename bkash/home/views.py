from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from .models import UserProfile, UpdateUser, AdminProfile, MerchantProfile, Branch, Offer, AllCustomerInfo, AllAgentInfo, AllMerchantInfo, AllOperatorInfo, AllServiceProviderInfo
from django.core.files.storage import FileSystemStorage
from dashboard.models import execute_sql,connection
import os
# Create your views here.


class HomeView(View):
    def get(self, request):
        if request.session.get('CUSTOMER'):
            if not (request.COOKIES.get('NAME') and request.COOKIES.get('PHOTO') and request.COOKIES.get('MOBILE')):
                user = UserProfile(request.session.get('CUSTOMER'))
                context = user.getProfile()
                context['TYPE'] = 'customer'
                sql = 'SELECT CUSTOMER_BALANCE FROM CUSTOMER WHERE CUSTOMER_ID=:cust'
                balance = execute_sql(
                    sql, [request.session.get('CUSTOMER')], False, True,connection)[0][0]
                context['BALANCE'] = balance

                context['MERCHANT'] = getMerchant()

                resp = render(request, 'home/user_home.html', context)
                resp.set_cookie('NAME', context['NAME'])
                resp.set_cookie('MOBILE', context['MOBILE'])
                resp.set_cookie('PHOTO', context['PHOTO'])
                return resp

            sql = 'SELECT CUSTOMER_BALANCE FROM CUSTOMER WHERE CUSTOMER_ID=:cust'
            balance = execute_sql(
                sql, [request.session.get('CUSTOMER')], False, True,connection)[0][0]

            context = {'NAME': request.COOKIES.get('NAME'), 'PHOTO': request.COOKIES.get('PHOTO'),
                       'MOBILE': request.COOKIES.get('MOBILE'), 'TYPE': 'customer', 'BALANCE': balance}
            context['MERCHANT'] = getMerchant()
            return render(request, 'home/user_home.html', context)

        elif request.session.get('AGENT'):
            if not (request.COOKIES.get('NAME') and request.COOKIES.get('PHOTO') and request.COOKIES.get('MOBILE')):
                user = UserProfile(request.session.get('AGENT'))
                context = user.getProfile()
                context['TYPE'] = 'agent'
                sql = 'SELECT AGENT_BALANCE FROM AGENT WHERE AGENT_ID=:agent'
                balance = execute_sql(
                    sql, [request.session.get('AGENT')], False, True,connection)[0][0]
                context['BALANCE'] = balance
                context['MERCHANT'] = getMerchant()
                resp = render(request, 'home/user_home.html', context)
                resp.set_cookie('NAME', context['NAME'])
                resp.set_cookie('MOBILE', context['MOBILE'])
                resp.set_cookie('PHOTO', context['PHOTO'])
                return resp

            sql = 'SELECT AGENT_BALANCE FROM AGENT WHERE AGENT_ID=:agent'
            balance = execute_sql(
                sql, [request.session.get('AGENT')], False, True,connection)[0][0]

            context = {'NAME': request.COOKIES.get('NAME'), 'PHOTO': request.COOKIES.get('PHOTO'),
                       'MOBILE': request.COOKIES.get('MOBILE'), 'TYPE': 'agent', 'BALANCE': balance}
            context['MERCHANT'] = getMerchant()
            return render(request, 'home/user_home.html', context)

        elif request.session.get('ADMIN'):
            #context = {'NAME':request.COOKIES.get('NAME'),'CUSTOMER':request.COOKIES.get('CUSTOMER')}
            user = AdminProfile(request.session.get('ADMIN'))
            context = user.getProfile()
            return render(request, 'home/admin_home.html', context)

        elif request.session.get('MERCHANT'):
            if not (request.COOKIES.get('NAME') and request.COOKIES.get('PHOTO') and request.COOKIES.get('TRADE_LICENSE_NO') and request.COOKIES.get('HEAD_OFFICE_LOCATION') and request.COOKIES.get('BRANCH') and request.cookies.get('OFFER_PERCENT')):
                merchant = MerchantProfile(request.session.get('MERCHANT'))
                context = merchant.getProfile()
                context['TYPE'] = 'merchant'
                resp = render(request, 'home/merchant_home.html', context)
                resp.set_cookie('NAME', context['NAME'])
                resp.set_cookie('PHOTO', context['PHOTO'])
                resp.set_cookie('TRADE_LICENSE_NO',
                                context['TRADE_LICENSE_NO'])
                resp.set_cookie('HEAD_OFFICE_LOCATION',
                                context['HEAD_OFFICE_LOCATION'])
                resp.set_cookie('BRANCH_NAME', context['BRANCH'])
                resp.set_cookie('OFFER_PERCENT', context['OFFER_PERCENT'])
                return resp

            context = {'NAME': request.COOKIES.get('NAME'), 'PHOTO': request.COOKIES.get('PHOTO'),
                       'TRADE_LICENSE_NO': request.COOKIES.get('TRADE_LICENSE_NO'), 'TYPE': 'merchant',
                       'HEAD_OFFICE_LOCATION': request.COOKIES.get('HEAD_OFFICE_LOCATION'),
                       'BRANCH': request.COOKIES.get('BRANCH_NAME'), 'OFFER_PERCENT': request.COOKIES.get('OFFER_PERCENT')}
            return render(request, 'home/merchant_home.html', context)

        return render(request, 'home/home.html')

    def post(self, request):
        if request.session.get('ADMIN'):
            admin_id = request.session.get('ADMIN')
            if request.POST.get('agent_mobile_no') and request.POST.get('add_money_amount'):
                agent_number = request.POST.get('agent_mobile_no')
                amount = request.POST.get('add_money_amount')
                admin = AdminProfile(admin_id)
                if admin.addMoney(agent_number, amount):
                    add_money_successful = True
                    context = admin.getProfile()
                    context['add_money_successful'] = add_money_successful
                    return render(request, 'home/admin_home.html', context)
                else:
                    add_money_failed = True
                    context = admin.getProfile()
                    context['add_money_failed'] = add_money_failed
                    return render(request, 'home/admin_home.html', context)
            else:
                for name, key in request.POST.items():
                    if name[0:4] == 'CUST':
                        if int(key) > 0:
                            sql = 'UPDATE CUSTOMER SET APPROVED_BY=:admin WHERE CUSTOMER_ID=:cust'
                            list = [request.session.get('ADMIN'), key]
                            execute_sql(sql, list, True, False,connection)
                        elif int(key) < 0:
                            sql = 'DELETE CUSTOMER WHERE CUSTOMER_ID=:cust'
                            list = [-int(key)]
                            execute_sql(sql, list, True, False,connection)
                            sql = 'DELETE USERS WHERE USER_ID=:user'
                            execute_sql(sql, list, True, False,connection)
                    elif name[0:4] == 'AGEN':
                        if int(key) > 0:
                            sql = 'UPDATE AGENT SET APPROVED_BY=:admin WHERE AGENT_ID=:agent'
                            list = [request.session.get('ADMIN'), key]
                            execute_sql(sql, list, True, False,connection)
                            sql = 'UPDATE AGENT SET AGENT_BALANCE=5000 WHERE AGENT_ID=:agent'
                            list = [key]
                            execute_sql(sql, list, True, False,connection)
                        elif int(key) < 0:
                            sql = 'DELETE AGENT WHERE AGENT_ID=:admin'
                            list = [-int(key)]
                            execute_sql(sql, list, True, False,connection)
                            sql = 'DELETE USERS WHERE USER_ID=:user'
                            execute_sql(sql, list, True, False,connection)
                    elif name[0:4] == 'ADMI':
                        if int(key) > 0:
                            sql = 'UPDATE ADMIN SET APPROVED_BY=:admin WHERE ADMIN_ID=:admin'
                            list = [request.session.get('ADMIN'), key]
                            execute_sql(sql, list, True, False,connection)
                        elif int(key) < 0:
                            sql = 'DELETE ADMIN WHERE ADMIN_ID=:admin'
                            list = [-int(key)]
                            execute_sql(sql, list, True, False,connection)
                    elif name[0:4] == 'MERC':
                        if int(key) > 0:
                            sql = 'UPDATE MERCHANTS SET APPROVED_BY=:admin WHERE MERCHANT_ID=:merchant'
                            list = [request.session.get('ADMIN'), key]
                            execute_sql(sql, list, True, False,connection)
                        elif int(key) < 0:
                            sql = 'DELETE MERCHANTS WHERE MERCHANT_ID=:merchant'
                            list = [-int(key)]
                            execute_sql(sql, list, True, False,connection)
                    elif name[0:4] == 'SERV':
                        if int(key) > 0:
                            sql = 'UPDATE UTILITY_SERVICE SET APPROVED_BY=:admin WHERE SERVICE_ID=:service'
                            list = [request.session.get('ADMIN'), key]
                            execute_sql(sql, list, True, False,connection)
                        elif int(key) < 0:
                            sql = 'DELETE UTILITY_SERVICE WHERE SERVICE_ID=:service'
                            list = [-int(key)]
                            execute_sql(sql, list, True, False,connection)
                    elif name[0:4] == 'OPER':
                        if int(key) > 0:
                            sql = 'UPDATE MOBILE_OPERATOR SET APPROVED_BY=:admin WHERE OPERATOR_ID=:operator'
                            list = [request.session.get('ADMIN'), key]
                            execute_sql(sql, list, True, False,connection)
                        elif int(key) < 0:
                            sql = 'DELETE MOBILE_OPERATOR WHERE OPERATOR_ID=:operator'
                            list = [-int(key)]
                            execute_sql(sql, list, True, False,connection)

                return redirect('home:home')

        elif request.session.get('MERCHANT'):
            offer_perc = request.POST.get('offer')
            offer = Offer(offer_perc)
            offer_id = offer.getOfferId()
            sql = 'UPDATE MERCHANTS SET OFFER_ID =: offer_id WHERE MERCHANT_ID =:merchant'
            list = [offer_id, request.session.get('MERCHANT')]
            execute_sql(sql, list, True, False,connection)
            return redirect('home:home')


class LogoutView(View):
    def get(self, request):
        if request.session.get('CUSTOMER'):
            del(request.session['CUSTOMER'])
            resp = redirect('home:home')
            resp.delete_cookie('NAME')
            resp.delete_cookie('MOBILE')
            resp.delete_cookie('PHOTO')
            return resp
        if request.session.get('AGENT'):
            del(request.session['AGENT'])
            resp = redirect('home:home')
            resp.delete_cookie('NAME')
            resp.delete_cookie('MOBILE')
            resp.delete_cookie('PHOTO')
            return resp
        if request.session.get('ADMIN'):
            del(request.session['ADMIN'])
            resp = redirect('home:home')
            resp.delete_cookie('NAME')
            return resp
        if request.session.get('MERCHANT'):
            del(request.session['MERCHANT'])
            resp = redirect('home:home')
            resp.delete_cookie('NAME')
            resp.delete_cookie('PHOTO')
            resp.delete_cookie('TRADE_LICENSE_NO')
            resp.delete_cookie('HEAD_OFFICE_LOCATION')
            resp.delete_cookie('BRANCH')
            resp.delete_cookie('OFFER_PERCENT')
            return resp
        return redirect('home:home')


class UpdateUserView(View):
    def get(self, request):
        if request.session.get('CUSTOMER') or request.session.get('AGENT'):
            id = request.session.get('AGENT')
            if request.session.get('CUSTOMER'):
                id = request.session.get('CUSTOMER')

            user = UpdateUser(id)
            context = user.showForUpdate()
            return render(request, 'home/updateUser.html', context)

    def post(self, request):
        if request.session.get('CUSTOMER') or request.session.get('AGENT'):
            id = request.session.get('AGENT')
            if request.session.get('CUSTOMER'):
                id = request.session.get('CUSTOMER')

            user = UpdateUser(id)
            context = user.showForUpdate()
            path = 'media\\'+context['PHOTO']

            if request.FILES.get("img"):
                if os.path.isfile(path):
                    os.remove(path)

                image = request.FILES.get("img")
                fs = FileSystemStorage()
                filename = fs.save(context['PHOTO'], image)
                return redirect('home:home')
            else:
                resp = user.update(request.POST.get('username'), request.POST.get('father_name'),
                                   request.POST.get('mother_name'), request.POST.get(
                                       'gender'), request.POST.get('dob'),
                                   request.POST.get('nid_no'), request.POST.get('mobile_no'), request.POST.get('password'))
                return resp


class UserInfoView(View):
    def get(self, request):
        if request.session.get('CUSTOMER') or request.session.get('AGENT'):
            id = request.session.get('AGENT')
            if request.session.get('CUSTOMER'):
                id = request.session.get('CUSTOMER')

            user = UpdateUser(id)
            context = user.showForUpdate()
            return render(request, 'home/userInfo.html', context)


class addBranchView(View):
    def get(self, request):
        if(request.session.get('MERCHANT')):
            id = request.session.get('MERCHANT')
            merchant = MerchantProfile(id)
            context = merchant.getProfile()
            return render(request, 'home/merchantBrachAdd.html', context)

    def post(self, request):
        if(request.session.get('MERCHANT')):
            id = request.session.get('MERCHANT')
            branch = Branch(request.POST.get('branchname'),
                            request.POST.get('mobileno'), id)
            branch_name_exists = True
            if branch.is_a_new_branch():
                branch.insert()
                return redirect('home:home')
            else:
                branch_name_exists = True

            merchant = MerchantProfile(id)
            context = merchant.getProfile()
            context['message'] = branch_name_exists
            return render(request, "home/merchantBrachAdd.html", context)


class customerInfoView(View):
    def get(self, request):
        customer = AllCustomerInfo()
        context = customer.getInfo()
        return render(request, 'home/admin_customer_info.html', context)


class agentInfoView(View):
    def get(self, request):
        agent = AllAgentInfo()
        context = agent.getInfo()
        return render(request, 'home/admin_agent_info.html', context)


class merchantInfoView(View):
    def get(self, request):
        merchant = AllMerchantInfo()
        context = merchant.getInfo()
        return render(request, 'home/admin_merchant_info.html', context)


class operatorInfoView(View):
    def get(self, request):
        operator = AllOperatorInfo()
        context = operator.getInfo()
        return render(request, 'home/admin_operator_info.html', context)


class serviceProviderInfoView(View):
    def get(self, request):
        service = AllServiceProviderInfo()
        context = service.getInfo()
        return render(request, 'home/admin_service_info.html', context)


def getMerchant():
    sql = 'SELECT COUNT(*) FROM MERCHANTS M,OFFERS O WHERE M.OFFER_ID = O.OFFER_ID AND O.DISCOUNT_PERCENT>0'
    if execute_sql(sql, [], False, True,connection)[0][0] != 0:
        sql = 'SELECT M.MERCHANT_NAME,M.MERCHANT_LOGO_IMAGE,O.DISCOUNT_PERCENT FROM MERCHANTS M,OFFERS O WHERE M.OFFER_ID = O.OFFER_ID AND O.DISCOUNT_PERCENT>0 ORDER BY O.DISCOUNT_PERCENT DESC'
        merchant_list = execute_sql(sql, [], False, True,connection)
        cont_merchant = merchant_list
        i = 0
        for x in merchant_list:
            cont_merchant[i] = {'merchant_name': x[0],
                                'merchant_photo': x[1], 'discount_percent': x[2]}
            i = i+1
        return cont_merchant
    else:
        return None
