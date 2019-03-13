from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout,login
from USER.forms import SignUpForm

class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/index/')
        form  = AuthenticationForm
        return render(request,'login.html',context={'form':form})

    def post(self,request, *args, **kwargs):
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            return redirect('/index/')
        return render(request, 'login.html', context={'form': form})

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return redirect('login_page')
        else:
            return redirect('/index/')


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm
        return render(request,'sign-up.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save(commit=True,group='ADMIN_GROUP')
            return redirect('login_page')
        return render(request, 'sign-up.html', context={'form': form})

