from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect

class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
            #return redirect()
        form  = AuthenticationForm
        return render(request,'login.html',context={'form':form})

    def post(self,request, *args, **kwargs):
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            return HttpResponse('ok')
        return render(request, 'login.html', context={'form': form})
