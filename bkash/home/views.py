from django.shortcuts import render,HttpResponse,redirect
from django.views import View

# Create your views here.

class HomeView(View):
    def get(self,request):
        if request.session.get('mobile_no'):
            return render(request,'home/user_home.html',{'mobile_no':request.session.get('mobile_no')})
        return render(request,'home/home.html')

class User_homeView(View):
    def get(self,request):
        if request.session.get('mobile_no'):
            return render(request,'home/user_home.html',{'mobile_no':request.session.get('mobile_no')})
        return render(request,'home/home.html')

class LogoutView(View):
    def get(self,request):
        if request.session.get('mobile_no'):
            del(request.session['mobile_no'])
            return render(request,'home/home.html')#redirect('home:user_home')
        return redirect('home:home')
