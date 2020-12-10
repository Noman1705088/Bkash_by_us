from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.core.files.storage import FileSystemStorage
import os
from .models import USERS, LoginAgent, LoginCustomer, execute_sql, Agent, Customer, Admin, LoginAdmin, Merchant, LoginMerchant, ServiceProvider, MobileOperator
# Create your views here.
# Create your views here.


class RegistrationAgentView(View):
    def get(self, request):
        return render(request, "dashboard/registrationAgentNew.html")

    def post(self, request):
        if request.FILES.get("img"):
            if not execute_sql('select max(user_id) from users', [], False, True)[0][0]:
                user_id = 1
            else:
                user_id = int(execute_sql(
                    'select max(user_id) from users', [], False, True)[0][0]) + 1

            imagename = 'user_'+str(user_id)+'.jpg'

            user = USERS(imagename, request.POST.get("username"), request.POST.get("father_name"), request.POST.get("mother_name"),
                         request.POST.get("gender"), request.POST.get(
                             "dob"), request.POST.get("nid_no"), request.POST.get("mobile_no"),
                         request.POST.get("password"))

            bank_acc = request.POST.get('bank_acc')
            balance = 0
            agent = Agent(user_id, bank_acc, balance)

            mobile_no_already_used = False
            if user.is_a_new_user():
                user.insert()
                agent.insert()
                image = request.FILES.get("img")
                fs = FileSystemStorage()
                filename = fs.save(imagename, image)
                return redirect('home:home')
            else:
                mobile_no_already_used = True
        return render(request, "dashboard/registrationAgentNew.html", {'message': mobile_no_already_used})


class RegistrationCustomerView(View):
    def get(self, request):
        return render(request, "dashboard/registrationCustomerNew.html")

    def post(self, request):
        if request.FILES.get("img"):
            if not execute_sql('select max(user_id) from users', [], False, True)[0][0]:
                user_id = 1
            else:
                user_id = int(execute_sql(
                    'select max(user_id) from users', [], False, True)[0][0]) + 1

            imagename = 'user_'+str(user_id)+'.jpg'

            user = USERS(imagename, request.POST.get("username"), request.POST.get("father_name"), request.POST.get("mother_name"),
                         request.POST.get("gender"), request.POST.get(
                             "dob"), request.POST.get("nid_no"), request.POST.get("mobile_no"),
                         request.POST.get("password"))

            balance = 0
            customer = Customer(user_id, balance)

            mobile_no_already_used = False
            if user.is_a_new_user():
                user.insert()
                customer.insert()
                image = request.FILES.get("img")
                fs = FileSystemStorage()
                filename = fs.save(imagename, image)
                return redirect('home:home')
            else:
                mobile_no_already_used = True
        return render(request, "dashboard/registrationCustomerNew.html", {'message': mobile_no_already_used})


class RegistrationAdminView(View):
    def get(self, request):
        return render(request, "dashboard/registrationAdmin.html")

    def post(self, request):
        admin_name = request.POST.get('username')
        admin_pass = request.POST.get('password')

        admin = Admin(admin_name, admin_pass)

        user_name_exists = True
        if admin.uniqueName():
            user_name_exists = False
            admin.insert()
            return redirect('home:home')
        else:
            user_name_exists = True
        return render(request, "dashboard/registrationAdmin.html", {'message': user_name_exists})


class RegistrationMerchantView(View):
    def get(self, request):
        return render(request, "dashboard/registrationMerchant.html")

    def post(self, request):
        if request.FILES.get("img"):
            if not execute_sql('select max(merchant_id) from merchants', [], False, True)[0][0]:
                merchant_id = 1
            else:
                merchant_id = int(execute_sql(
                    'select max(merchant_id) from merchants', [], False, True)[0][0]) + 1

            imagename = 'merchant_'+str(merchant_id)+'.jpg'

            merchant = Merchant(merchant_id, imagename, request.POST.get(
                "merchantname"), request.POST.get("trade_license_no"), request.POST.get("head_office_loc"), request.POST.get("password"))
            merchant_name_exists = True
            if merchant.uniqueMerchantName():
                merchant.insert()
                image = request.FILES.get("img")
                fs = FileSystemStorage()
                filename = fs.save(imagename, image)
                return redirect('home:home')
            else:
                merchant_name_exists = True
        return render(request, "dashboard/registrationMerchant.html", {'message': merchant_name_exists})


class RegistrationServiceProviderView(View):
    def get(self, request):
        return render(request, "dashboard/registrationServiceProvider.html")

    def post(self, request):
        if request.FILES.get("img"):
            if not execute_sql('SELECT MAX(SERVICE_ID) FROM UTILITY_SERVICE', [], False, True)[0][0]:
                service_id = 1
            else:
                service_id = int(execute_sql(
                    'SELECT MAX(SERVICE_ID) FROM UTILITY_SERVICE', [], False, True)[0][0]) + 1

            imagename = 'service_'+str(service_id)+'.jpg'
            service = ServiceProvider(imagename, request.POST.get('servicename'), request.POST.get('servicetype'),
                                      request.POST.get('bank_acc'))

            service_exists = False
            if service.uniqueServiceProvider():
                service.insert()
                image = request.FILES.get("img")
                fs = FileSystemStorage()
                filename = fs.save(imagename, image)
                return redirect('home:home')
            else:
                service_exists = True

        return render(request, "dashboard/registrationServiceProvider.html", {'message': service_exists})


class RegistrationOperatorView(View):
    def get(self, request):
        return render(request, "dashboard/registrationOperator.html")

    def post(self, request):
        operator_name = request.POST.get("operator_name")
        #operator_name = operator_name.upper()
        operator_digit = int(request.POST.get("operator_digit"))
        operator_bank_ac = request.POST.get("bank_acc")

        operator = MobileOperator(
            operator_name, operator_digit, operator_bank_ac)

        if operator.is_selected_digit_available() and operator.is_name_available():
            operator.insert()
            return redirect('home:home')
        else:
            operator_exists = True
            return render(request, "dashboard/registrationOperator.html", {'message': operator_exists})


class LoginCustomerView(View):
    def get(self, request):
        return render(request, "dashboard/loginCustomerNew.html")

    def post(self, request):
        user = LoginCustomer(request.POST.get('mobile_no'),
                             request.POST.get('password'))
        logged_in_failed = True
        if user.is_valid_user():
            if request.session.get('AGENT'):
                del(request.session['AGENT'])
            if request.session.get('ADMIN'):
                del(request.session['ADMIN'])
            if request.session.get('MERCHANT'):
                del(request.session['MERCHANT'])
            logged_in_failed = False
            request.session['CUSTOMER'] = user.user_id()
            return redirect('home:home')
        return render(request, "dashboard/loginCustomerNew.html", {'message': logged_in_failed})


class LoginAgentView(View):
    def get(self, request):
        return render(request, "dashboard/loginAgentNew.html")

    def post(self, request):
        user = LoginAgent(request.POST.get('mobile_no'),
                          request.POST.get('password'))
        logged_in_failed = True
        if user.is_valid_user():
            if request.session.get('CUSTOMER'):
                del(request.session['CUSTOMER'])
            if request.session.get('ADMIN'):
                del(request.session['ADMIN'])
            if request.session.get('MERCHANT'):
                del(request.session['MERCHANT'])
            logged_in_failed = False
            request.session['AGENT'] = user.user_id()
            return redirect('home:home')
        return render(request, "dashboard/loginAgentNew.html", {'message': logged_in_failed})


class LoginAdminView(View):
    def get(self, request):
        return render(request, "dashboard/loginAdmin.html")

    def post(self, request):
        user = LoginAdmin(request.POST.get('admin_name'),
                          request.POST.get('password'))
        logged_in_failed = True
        if user.is_valid_user():
            if request.session.get('CUSTOMER'):
                del(request.session['CUSTOMER'])
            if request.session.get('AGENT'):
                del(request.session['AGENT'])
            if request.session.get('MERCHANT'):
                del(request.session['MERCHANT'])
            logged_in_failed = False
            request.session['ADMIN'] = user.user_id()
            return redirect('home:home')
        return render(request, "dashboard/loginAdmin.html", {'message': logged_in_failed})


class LoginMerchantView(View):
    def get(self, request):
        return render(request, "dashboard/loginMerchant.html")

    def post(self, request):
        user = LoginMerchant(request.POST.get('merchant_name'),
                             request.POST.get('password'))
        logged_in_failed = True
        if user.is_a_valid_Merchant():
            if request.session.get('CUSTOMER'):
                del(request.session['CUSTOMER'])
            if request.session.get('AGENT'):
                del(request.session['AGENT'])
            if request.session.get('ADMIN'):
                del(request.session['ADMIN'])
            logged_in_failed = False
            request.session['MERCHANT'] = user.merchant_id()
            return redirect('home:home')
        return render(request, "dashboard/loginMerchant.html", {'message': logged_in_failed})
