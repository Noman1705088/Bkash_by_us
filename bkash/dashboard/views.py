from django.shortcuts import render,HttpResponse
from django.views import View
from django.core.files.storage import FileSystemStorage
import os
from .models import USERS,Login,execute_sql
# Create your views here.

class RegistrationView(View):
    def get(self,request):
        return render(request,"dashboard/registration.html")
    def post(self,request):
        if request.FILES.get("img"):
            user_id = int(execute_sql('select max(user_id) from users',[],False,True)[0][0]) + 1
            imagename= 'user_'+str(user_id)+'.jpg'

            user=USERS(imagename,request.POST.get("username"),request.POST.get("father_name"),request.POST.get("mother_name"),\
                request.POST.get("gender"),request.POST.get("dob"),request.POST.get("nid_no"),request.POST.get("mobile_no"),
                request.POST.get("password"))

            mobile_no_already_used=False
            if user.is_a_new_user():
                user.insert()
                image= request.FILES.get("img")
                fs = FileSystemStorage()
                filename = fs.save(imagename, image)
            else:
                mobile_no_already_used=True

        return render(request,"dashboard/registration.html",{'message':mobile_no_already_used})

class LoginView(View):
    def get(self,request):
        return render(request,"dashboard/login.html")
    def post(self,request):
        user = Login(request.POST.get('mobile_no'),request.POST.get('password'))

        logged_in=False
        if user.is_valid_user():
            logged_in=True

        return render(request,"dashboard/login.html",{'message':logged_in})