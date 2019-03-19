from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView,DetailView
from django.shortcuts import render, redirect
from MAIN.models import Task, Project
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from MAIN.utils import group_required

class IndexView(View):
    def get(self, request, *args, **kwargs):
        print(request.user.get_all_permissions())
        if request.user.has_perm('MAIN.add_project'):
            return HttpResponse('ok')
        else:
            return HttpResponse('not ok')
        # return render(request,'default.html')


@method_decorator(login_required, name='dispatch')
#@method_decorator(group_required(('ADMIN'), raise_exception=True), name='dispatch')
class ProjectsView(ListView):
    model = Project
    template_name = "projects.html"
    context_object_name = 'projects'


@method_decorator(login_required, name='dispatch')
#@method_decorator(group_required(('ADMIN'), raise_exception=True), name='dispatch')
class ProjectsDetailView(DetailView):
    model = Project
    template_name = "project-detail.html"
    context_object_name = 'project'

import django_filters


class TaskFilter(django_filters.FilterSet):

    class Meta:
        model = Task
        fields = ['priority',]

@method_decorator(login_required, name='dispatch')
#@method_decorator(group_required(('ADMIN'), raise_exception=True), name='dispatch')
class TasksView(ListView):
    model = Task
    template_name = "tasks.html"
    context_object_name = 'tasks'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TaskFilter(self.request.GET,queryset=self.get_queryset())
        return context

