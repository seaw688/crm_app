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



class StatusSelectWidget(widgets.Select):
    option_style = (
    {'name': 'TO-DO', 'attr_name': 'class', 'value': """btn-outline-info"""},
    {'name': 'IN-PROGRESS', 'attr_name': 'class', 'value': """btn-outline-primary"""},
    {'name': 'DONE', 'attr_name': 'class', 'value': """btn-outline-secondary"""},
    {'name': 'CLOSED', 'attr_name': 'class', 'value': """btn-outline-dark"""},
                   )

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(StatusSelectWidget, self).create_option(name, value, label, selected, index, subindex=None,
                                                                attrs=None)

        for x in self.option_style:
            if option['value'] == x['name']:
                option['attrs'][x['attr_name']] = x['value']
        return option




class ExecutorSelectWidget(widgets.Select):
    template_name = 'widgets/executer-dropdown.html'
    option_template_name = 'widgets/executer-dropdown-options.html'

    def __init__(self, attrs=None, choices=(),current_user=None):
        super().__init__(attrs)
        self.choices = list(choices)
        self.current_user = current_user

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(ExecutorSelectWidget, self).create_option(name, value, label, selected, index, subindex=None, attrs=None)
        user = self.current_user
        return option

    def optgroups(self, name, value, attrs=None):
        """Return a list of optgroups for this widget."""
        groups = []
        has_selected = False


        for index, (option_value, option_label) in enumerate(self.choices):
            if option_value is None:
                option_value = ''

            subgroup = []
            if isinstance(option_label, (list, tuple)):
                group_name = option_value
                subindex = 0
                choices = option_label
            else:
                group_name = None
                subindex = None
                choices = [(option_value, option_label)]
            groups.append((group_name, subgroup, index))

            for subvalue, sublabel in choices:
                selected = (
                    str(subvalue) in value and
                    (not has_selected or self.allow_multiple_selected)
                )
                has_selected |= selected
                subgroup.append(self.create_option(
                    name, subvalue, sublabel, selected, index,
                    subindex=subindex, attrs=attrs,
                ))
                if subindex is not None:
                    subindex += 1
        return groups


    def make_option(self,name,value,label,index,user=None):


        return {
            'name': name,
            'value': value,
            'label': label,
            'index': index,
            'type': self.input_type,
            'template_name': self.option_template_name,
            'wrap_label': True,
            'user':user
        }

    def custome_options_set(self, name, value, attrs=None):
        options_set = []

        for index, (option_value, option_label) in enumerate(self.choices):

            print(option_value,option_label)
            if option_value == self.current_user.pk:
                break
            user = None

            if option_value != None and option_value != "":
                user=UserModel.objects.get(pk=option_value)
            else:
                option_label = 'Any executer'

            option = self.make_option(name=name,
                                      value=option_value,
                                      label=option_label,
                                      index = index,
                                      user=user)
            options_set.append(option)

        return options_set


    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['current_user'] = self.current_user
        context['widget']['options'] = self.custome_options_set(name, context['widget']['value'], attrs)
        return context



class TaskFilter(django_filters.FilterSet):

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data=data,queryset=queryset,request=request,prefix=prefix)
        self.filters['executor'].extra['widget'].current_user = self.request.user

    #
    # status = django_filters.ChoiceFilter(choices=TASK_STATUSES,
    #                                      empty_label='Any status',
    #                                      widget=StatusSelectWidget(
    #                                      attrs={"class": 'selectpicker', 'data-width': 'fit'}))


    executor = django_filters.ModelChoiceFilter(queryset=UserModel.objects.all(),
                                                widget=ExecutorSelectWidget(choices=(1,2,3),attrs={"class": 'selectpicker',
                                                                                   "data-width": 'auto',
                                                                                   "data-live-search": 'true'}))

    class Meta:
        model = Task
        #fields = ['priority', 'project', 'executor', 'kind', 'status']
        #fields = ['executor']
        fields = ""





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
        # print(x.filters['executor'].extra['widget'].choices)
        # print(x.filters['executor'].field.widget.choices)

        context['filter'] = x
        return context
