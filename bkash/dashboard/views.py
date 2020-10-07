from django.shortcuts import render,HttpResponse
from django.views import View
from django.core.files.storage import FileSystemStorage
import os
from .models import USERS,execute_sql
# Create your views here.

class RegistrationView(View):
    def get(self,request):
        return render(request,"dashboard/registration.html")
    def post(self,request):
        if request.FILES.get("img"):
            image= request.FILES.get("img")
            fs = FileSystemStorage()
            user_id = int(execute_sql('select max(user_id) from users',[],False,True)[0][0]) + 1
            filename = fs.save(str(user_id)+'.jpg', image)
            uploaded_file_url = fs.url(filename)
            #filename = fs.save(image.name, image)
            #uploaded_file_url = fs.url(filename)
            #filename, file_extension = os.path.splitext(uploaded_file_url)

            #user_id = int(execute_sql('SELECT MAX(USER_ID) FROM USERS;',[],False,True)) + 1
            #imagepath = "media\\"+str(user_id)+file_extention
            #os.rename(uploaded_file_url,imagepath)

            user=USERS(uploaded_file_url,request.POST.get("username"),request.POST.get("father_name"),request.POST.get("mother_name"),\
                request.POST.get("gender"),request.POST.get("dob"),request.POST.get("nid_no"),request.POST.get("mobile_no"),
                request.POST.get("password"))

            user.insert()
        return render(request,"dashboard/registration.html")

class LoginView(View):
    def get(self,request):
        return render(request,"dashboard/login.html")
    def post(self,request):
        return render(request,"dashboard/login.html")