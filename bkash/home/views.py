from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from .models import UserProfile,UpdateUser,AdminProfile
from django.core.files.storage import FileSystemStorage
from dashboard.models import execute_sql
import os
# Create your views here.

class HomeView(View):
    def get(self,request):
        if request.session.get('CUSTOMER'):
            if not (request.COOKIES.get('NAME') and request.COOKIES.get('PHOTO') and request.COOKIES.get('MOBILE')):
                user = UserProfile(request.session.get('CUSTOMER'))
                context = user.getProfile()
                context['TYPE'] = 'customer'               
                resp = render(request,'home/user_home.html',context)
                resp.set_cookie('NAME',context['NAME'])
                resp.set_cookie('MOBILE',context['MOBILE'])
                resp.set_cookie('PHOTO',context['PHOTO'])
                return resp           

            context = {'NAME':request.COOKIES.get('NAME'),'PHOTO':request.COOKIES.get('PHOTO'),\
                'MOBILE':request.COOKIES.get('MOBILE'),'TYPE':'customer'}
            return render(request,'home/user_home.html',context)
        elif request.session.get('AGENT'):
            if not (request.COOKIES.get('NAME') and request.COOKIES.get('PHOTO') and request.COOKIES.get('MOBILE')):
                user = UserProfile(request.session.get('AGENT'))
                context = user.getProfile()    
                context['TYPE'] = 'agent'            
                resp = render(request,'home/user_home.html',context)
                resp.set_cookie('NAME',context['NAME'])
                resp.set_cookie('MOBILE',context['MOBILE'])
                resp.set_cookie('PHOTO',context['PHOTO'])
                return resp           

            context = {'NAME':request.COOKIES.get('NAME'),'PHOTO':request.COOKIES.get('PHOTO'),\
                'MOBILE':request.COOKIES.get('MOBILE'),'TYPE':'agent'}
            return render(request,'home/user_home.html',context)
        elif request.session.get('ADMIN'):         
            #context = {'NAME':request.COOKIES.get('NAME'),'CUSTOMER':request.COOKIES.get('CUSTOMER')}
            user = AdminProfile(request.session.get('ADMIN'))
            context = user.getProfile()
            return render(request,'home/admin_home.html',context)

        return render(request,'home/home.html')

    def post(self,request):
        if request.session.get('ADMIN'):
            for name,key in request.POST.items():
                if name[0:4] == 'CUST':
                    sql = 'UPDATE CUSTOMER SET APPROVED_BY=:admin WHERE CUSTOMER_ID=:cust'
                    list=[request.session.get('ADMIN'),key]
                    execute_sql(sql,list,True,False)
                elif name[0:4] == 'AGEN':
                    sql = 'UPDATE AGENT SET APPROVED_BY=:admin WHERE AGENT_ID=:agent'
                    list=[request.session.get('ADMIN'),key]
                    execute_sql(sql,list,True,False)
                elif name[0:4] == 'ADMI':
                    sql = 'UPDATE ADMIN SET APPROVED_BY=:admin WHERE ADMIN_ID=:admin'
                    list=[request.session.get('ADMIN'),key]
                    execute_sql(sql,list,True,False)

            return redirect('home:home')


class LogoutView(View):
    def get(self,request):
        if request.session.get('CUSTOMER'):
            del(request.session['CUSTOMER'])
            resp=redirect('home:home')
            resp.delete_cookie('NAME')
            resp.delete_cookie('MOBILE')
            resp.delete_cookie('PHOTO')
            return resp
        if request.session.get('AGENT'):
            del(request.session['AGENT'])
            resp=redirect('home:home')
            resp.delete_cookie('NAME')
            resp.delete_cookie('MOBILE')
            resp.delete_cookie('PHOTO')
            return resp
        if request.session.get('ADMIN'):
            del(request.session['ADMIN'])
            resp=redirect('home:home')
            resp.delete_cookie('NAME')
            return resp
        return redirect('home:home')

class UpdateUserView(View):
    def get(self,request):
        if request.session.get('CUSTOMER') or request.session.get('AGENT'):
            id= request.session.get('AGENT')
            if request.session.get('CUSTOMER'): 
               id= request.session.get('CUSTOMER')

            user= UpdateUser(id)
            context = user.showForUpdate()
            return render(request,'home/updateUser.html',context)
    def post(self,request):
        if request.session.get('CUSTOMER') or request.session.get('AGENT'):
            id= request.session.get('AGENT')
            if request.session.get('CUSTOMER'):
               id= request.session.get('CUSTOMER')

            user= UpdateUser(id)
            context= user.showForUpdate()
            path = 'media\\'+context['PHOTO']

            if request.FILES.get("img"):
                if os.path.isfile(path):
                    os.remove(path)

                image= request.FILES.get("img")
                fs = FileSystemStorage()
                filename = fs.save(context['PHOTO'], image)

            else:
                user.update(request.POST.get('username'),request.POST.get('father_name'),\
                    request.POST.get('mother_name'),request.POST.get('gender'),request.POST.get('dob'),\
                        request.POST.get('nid_no'),request.POST.get('mobile_no'),request.POST.get('password'))
            return redirect('home:logout')
