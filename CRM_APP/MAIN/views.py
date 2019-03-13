from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, redirect
from MAIN.models import Task,Project
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required,login_required

class IndexView(View):
    def get(self, request, *args, **kwargs):

        return render(request,'default.html')

@method_decorator(permission_required('project.add_project'),name='dispatch')
@method_decorator(login_required,name='dispatch')

class ProjectsView(ListView):
    model = Project
    template_name = "test.html"
    context_object_name = 'projects'