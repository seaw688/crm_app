from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from MAIN.models import Task,Project

class IndexView(View):
    def get(self, request, *args, **kwargs):

        return render(request,'default.html')

class TestView(View):
    def get(self, request, *args, **kwargs):
        p=Project.objects.first()
        s = p.project_tasks.all()
        print(s)
        return HttpResponse('ok')