from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.core.files.storage import FileSystemStorage
import os
from .models import USERS,Login,execute_sql,Agent,Customer
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
            else:
                mobile_no_already_used=True
        return render(request,"dashboard/registrationCustomerNew.html",{'message':mobile_no_already_used})



class LoginView(View):
    def get(self,request):
        return render(request,"dashboard/loginNew.html")
    def post(self,request):
        user = Login(request.POST.get('mobile_no'),request.POST.get('password'))
        logged_in=False
        if user.is_valid_user():
            logged_in=True
            #return render(request,"dashboard/index.html",{'logged_in':logged_in})
            request.session['mobile_no'] = request.POST.get('mobile_no')
            return redirect('home:user_home')

        user_id=user.user_id(logged_in)

        return render(request,"dashboard/loginNew.html",{'message':logged_in})