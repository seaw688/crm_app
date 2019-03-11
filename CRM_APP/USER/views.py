from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth import logout

class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/index/')
        form  = AuthenticationForm
        return render(request,'login.html',context={'form':form})

    def post(self,request, *args, **kwargs):
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
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
        return render(request,'sign-up.html')

