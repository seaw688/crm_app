from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from MAIN.models import Task, Project
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from MAIN.utils import group_required

from django.forms import widgets
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class IndexView(View):
    def get(self, request, *args, **kwargs):
        print(request.user.get_all_permissions())
        if request.user.has_perm('MAIN.add_project'):
            return HttpResponse('ok')
        else:
            return HttpResponse('not ok')
        # return render(request,'default.html')


# @method_decorator(login_required, name='dispatch')
# @method_decorator(group_required(('ADMIN'), raise_exception=True), name='dispatch')
class ProjectsView(ListView):
    model = Project
    template_name = "projects.html"
    context_object_name = 'projects'


@method_decorator(login_required, name='dispatch')
# @method_decorator(group_required(('ADMIN'), raise_exception=True), name='dispatch')
class ProjectsDetailView(DetailView):
    model = Project
    template_name = "project-detail.html"
    context_object_name = 'project'


import django_filters

TASK_STATUSES = (
    ("TO-DO", "To do"),
    ("IN-PROGRESS", "In progress"),
    ("DONE", "Task done"),
    ("CLOSED", "Closed"),
)

TASK_STATUSES_STYLE = (
    {'name': 'TO-DO', 'attr_name': 'class', 'value': """btn-outline-info"""},
    {'name': 'IN-PROGRESS', 'attr_name': 'class', 'value': """btn-outline-primary"""},
    {'name': 'DONE', 'attr_name': 'class', 'value': """btn-outline-secondary"""},
    {'name': 'CLOSED', 'attr_name': 'class', 'value': """btn-outline-dark"""},

)


class StatusSelectWidget(widgets.Select):
    option_style = TASK_STATUSES_STYLE

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(StatusSelectWidget, self).create_option(name, value, label, selected, index, subindex=None,
                                                                attrs=None)

        for x in self.option_style:
            if option['value'] == x['name']:
                option['attrs'][x['attr_name']] = x['value']
        return option




class ExecutorSelectWidget(widgets.Select):

    def __init__(self, attrs=None, choices=(),user=None):
        super().__init__(attrs)
        # choices can be any iterable, but we may need to render this widget
        # multiple times. Thus, collapse it into a list so it can be consumed
        # more than once.
        self.choices = list(choices)


    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(ExecutorSelectWidget, self).create_option(name, value, label, selected, index, subindex=None,
                                                                attrs=None)
        return option



class TaskFilter(django_filters.FilterSet):

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data=data,queryset=queryset,request=request,prefix=prefix)
        self.filters['executor'].extra['widget'].test='test'


    status = django_filters.ChoiceFilter(choices=TASK_STATUSES,
                                         empty_label='Any status',
                                         widget=StatusSelectWidget(
                                         attrs={"class": 'selectpicker', 'data-width': 'fit'}))


    executor = django_filters.ModelChoiceFilter(queryset=UserModel.objects.all(),widget=ExecutorSelectWidget(attrs={'class':'selectpicker'}))

    class Meta:
        model = Task
        fields = ['priority', 'project', 'executor', 'kind', 'status']







# @method_decorator(login_required, name='dispatch')
# @method_decorator(group_required(('ADMIN'), raise_exception=True), name='dispatch')
class TasksView(ListView):

    model = Task
    template_name = "tasks.html"
    context_object_name = 'tasks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        x = TaskFilter(self.request.GET, queryset=queryset, request=self.request)
        context['filter'] = x
        return context
