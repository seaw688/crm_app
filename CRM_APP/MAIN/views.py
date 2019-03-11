from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect


class IndexView(View):
    def get(self, request, *args, **kwargs):

        return render(request,'default.html')
