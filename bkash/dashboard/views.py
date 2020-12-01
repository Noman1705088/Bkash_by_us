from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.core.files.storage import FileSystemStorage
import os
from .models import USERS,LoginAgent,LoginCustomer,execute_sql,Agent,Customer,Admin,LoginAdmin
# Create your views here.

class RegistrationAgentView(View):
    def get(self,request):
        return render(request,"dashboard/registrationAgentNew.html")
    def post(self,request):
        if request.FILES.get("img"):
            if not execute_sql('select max(user_id) from users',[],False,True)[0][0]:
                user_id=1
            else:
                user_id = int(execute_sql('select max(user_id) from users',[],False,True)[0][0]) + 1
                
            imagename= 'user_'+str(user_id)+'.jpg'

            user=USERS(imagename,request.POST.get("username"),request.POST.get("father_name"),request.POST.get("mother_name"),\
                request.POST.get("gender"),request.POST.get("dob"),request.POST.get("nid_no"),request.POST.get("mobile_no"),
                request.POST.get("password"))

            bank_acc = request.POST.get('bank_acc')
            balance = 0
            agent = Agent(user_id,bank_acc,balance)

            mobile_no_already_used=False
            if user.is_a_new_user():
                user.insert()
                agent.insert()
                image= request.FILES.get("img")
                fs = FileSystemStorage()
                filename = fs.save(imagename, image)
                return redirect('home:home')
            else:
                mobile_no_already_used=True
        return render(request,"dashboard/registrationAgentNew.html",{'message':mobile_no_already_used})

class RegistrationCustomerView(View):
    def get(self,request):
        return render(request,"dashboard/registrationCustomerNew.html")
    def post(self,request):
        if request.FILES.get("img"):
            if not execute_sql('select max(user_id) from users',[],False,True)[0][0]:
                user_id=1
            else:
                user_id = int(execute_sql('select max(user_id) from users',[],False,True)[0][0]) + 1
                
            imagename= 'user_'+str(user_id)+'.jpg'

            user=USERS(imagename,request.POST.get("username"),request.POST.get("father_name"),request.POST.get("mother_name"),\
                request.POST.get("gender"),request.POST.get("dob"),request.POST.get("nid_no"),request.POST.get("mobile_no"),
                request.POST.get("password"))

            balance = 0
            customer = Customer(user_id,balance)

            mobile_no_already_used=False
            if user.is_a_new_user():
                user.insert()
                customer.insert()
                image= request.FILES.get("img")
                fs = FileSystemStorage()
                filename = fs.save(imagename, image)
                return redirect('home:home')
            else:
                mobile_no_already_used=True
        return render(request,"dashboard/registrationCustomerNew.html",{'message':mobile_no_already_used})

class RegistrationAdminView(View):
    def get(self,request):
        return render(request,"dashboard/registrationAdmin.html")
    def post(self,request):
        admin_name=request.POST.get('username')
        admin_pass=request.POST.get('password')

        admin = Admin(admin_name,admin_pass)

        user_name_exists=True
        if admin.uniqueName():
            user_name_exists = False
            admin.insert()
            return redirect('home:home')
        else:
            user_name_exists=True
        return render(request,"dashboard/registrationAdmin.html",{'message':user_name_exists})

class LoginCustomerView(View):
    def get(self,request):
        return render(request,"dashboard/loginCustomerNew.html")
    def post(self,request):
        user = LoginCustomer(request.POST.get('mobile_no'),request.POST.get('password'))
        logged_in_failed=True
        if user.is_valid_user():
            if request.session.get('AGENT'):
                del(request.session['AGENT'])
            if request.session.get('ADMIN'):
                del(request.session['ADMIN'])
            logged_in_failed=False
            request.session['CUSTOMER'] = user.user_id()
            return redirect('home:home')
        return render(request,"dashboard/loginCustomerNew.html",{'message':logged_in_failed})

class LoginAgentView(View):
    def get(self,request):
        return render(request,"dashboard/loginAgentNew.html")
    def post(self,request):
        user = LoginAgent(request.POST.get('mobile_no'),request.POST.get('password'))
        logged_in_failed=True
        if user.is_valid_user():
            if request.session.get('CUSTOMER'):
                del(request.session['CUSTOMER'])
            if request.session.get('ADMIN'):
                del(request.session['ADMIN'])
            logged_in_failed=False
            request.session['AGENT'] = user.user_id()
            return redirect('home:home')
        return render(request,"dashboard/loginAgentNew.html",{'message':logged_in_failed})

class LoginAdminView(View):
    def get(self,request):
        return render(request,"dashboard/loginAdmin.html")
    def post(self,request):
        user = LoginAdmin(request.POST.get('admin_name'),request.POST.get('password'))
        logged_in_failed=True
        if user.is_valid_user():
            if request.session.get('CUSTOMER'):
                del(request.session['CUSTOMER'])
            if request.session.get('AGENT'):
                del(request.session['AGENT'])            
            logged_in_failed=False
            request.session['ADMIN'] = user.user_id()
            return redirect('home:home')
        return render(request,"dashboard/loginAdmin.html",{'message':logged_in_failed})