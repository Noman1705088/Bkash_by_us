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
                sql='SELECT CUSTOMER_BALANCE FROM CUSTOMER WHERE CUSTOMER_ID=:cust'
                balance = execute_sql(sql,[request.session.get('CUSTOMER')],False,True)[0][0]
                context['BALANCE']=balance
                               
                resp = render(request,'home/user_home.html',context)
                resp.set_cookie('NAME',context['NAME'])
                resp.set_cookie('MOBILE',context['MOBILE'])
                resp.set_cookie('PHOTO',context['PHOTO'])
                return resp 
                          
            sql='SELECT CUSTOMER_BALANCE FROM CUSTOMER WHERE CUSTOMER_ID=:cust'
            balance = execute_sql(sql,[request.session.get('CUSTOMER')],False,True)[0][0]

            context = {'NAME':request.COOKIES.get('NAME'),'PHOTO':request.COOKIES.get('PHOTO'),\
                'MOBILE':request.COOKIES.get('MOBILE'),'TYPE':'customer','BALANCE':balance}
            return render(request,'home/user_home.html',context)
        elif request.session.get('AGENT'):
            if not (request.COOKIES.get('NAME') and request.COOKIES.get('PHOTO') and request.COOKIES.get('MOBILE')):
                user = UserProfile(request.session.get('AGENT'))
                context = user.getProfile()    
                context['TYPE'] = 'agent'
                sql='SELECT AGENT_BALANCE FROM AGENT WHERE AGENT_ID=:agent'
                balance = execute_sql(sql,[request.session.get('AGENT')],False,True)[0][0]
                context['BALANCE']=balance
                            
                resp = render(request,'home/user_home.html',context)
                resp.set_cookie('NAME',context['NAME'])
                resp.set_cookie('MOBILE',context['MOBILE'])
                resp.set_cookie('PHOTO',context['PHOTO'])
                return resp           

            sql='SELECT AGENT_BALANCE FROM AGENT WHERE AGENT_ID=:agent'
            balance = execute_sql(sql,[request.session.get('AGENT')],False,True)[0][0]

            context = {'NAME':request.COOKIES.get('NAME'),'PHOTO':request.COOKIES.get('PHOTO'),\
                'MOBILE':request.COOKIES.get('MOBILE'),'TYPE':'agent','BALANCE':balance}
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
                    if int(key)>0:
                        sql = 'UPDATE CUSTOMER SET APPROVED_BY=:admin WHERE CUSTOMER_ID=:cust'
                        list=[request.session.get('ADMIN'),key]
                        execute_sql(sql,list,True,False)
                    elif int(key)<0:
                        sql = 'DELETE CUSTOMER WHERE CUSTOMER_ID=:cust'
                        list=[-int(key)]
                        execute_sql(sql,list,True,False)  
                        sql = 'DELETE USERS WHERE USER_ID=:user'
                        execute_sql(sql,list,True,False)                        
                elif name[0:4] == 'AGEN':
                    if int(key)>0:
                        sql = 'UPDATE AGENT SET APPROVED_BY=:admin WHERE AGENT_ID=:agent'
                        list=[request.session.get('ADMIN'),key]
                        execute_sql(sql,list,True,False)
                        sql = 'UPDATE AGENT SET AGENT_BALANCE=5000 WHERE AGENT_ID=:agent'
                        list=[key]
                        execute_sql(sql,list,True,False)
                    elif int(key)<0:
                        sql = 'DELETE AGENT WHERE AGENT_ID=:admin'
                        list=[-int(key)]
                        execute_sql(sql,list,True,False)  
                        sql = 'DELETE USERS WHERE USER_ID=:user'
                        execute_sql(sql,list,True,False)   
                elif name[0:4] == 'ADMI':
                    if int(key)>0:
                        sql = 'UPDATE ADMIN SET APPROVED_BY=:admin WHERE ADMIN_ID=:admin'
                        list=[request.session.get('ADMIN'),key]
                        execute_sql(sql,list,True,False)
                    elif int(key)<0:
                        sql = 'DELETE ADMIN WHERE ADMIN_ID=:admin'
                        list=[-int(key)]
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
                return redirect('home:home')
            else:
                resp = user.update(request.POST.get('username'),request.POST.get('father_name'),\
                    request.POST.get('mother_name'),request.POST.get('gender'),request.POST.get('dob'),\
                        request.POST.get('nid_no'),request.POST.get('mobile_no'),request.POST.get('password'))
                return resp

class UserInfoView(View):
    def get(self,request):
        if request.session.get('CUSTOMER') or request.session.get('AGENT'):
            id= request.session.get('AGENT')
            if request.session.get('CUSTOMER'): 
               id= request.session.get('CUSTOMER')

            user= UpdateUser(id)
            context = user.showForUpdate()
            return render(request,'home/userInfo.html',context)        
