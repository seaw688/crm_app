from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from django.shortcuts import render, redirect
from MAIN.models import Task, Project, TimeLog
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from MAIN.utils import group_required

from django.forms import widgets
from django.contrib.auth import get_user_model
import django_filters

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



# @method_decorator(login_required, name='dispatch')
# @method_decorator(group_required(('ADMIN'), raise_exception=True), name='dispatch')
class ProjectsDetailView(DetailView):
    model = Project
    template_name = "project-detail.html"
    context_object_name = 'project'



#
# TASK_STATUSES = (
#     ("TO-DO", "To do"),
#     ("IN-PROGRESS", "In progress"),
#     ("DONE", "Task done"),
#     ("CLOSED", "Closed"),
# )
#
#
#
# class StatusSelectWidget(widgets.Select):
#     option_style = (
#     {'name': 'TO-DO', 'attr_name': 'class', 'value': """btn-outline-info"""},
#     {'name': 'IN-PROGRESS', 'attr_name': 'class', 'value': """btn-outline-primary"""},
#     {'name': 'DONE', 'attr_name': 'class', 'value': """btn-outline-secondary"""},
#     {'name': 'CLOSED', 'attr_name': 'class', 'value': """btn-outline-dark"""},
#                    )
#
#     def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
#         option = super(StatusSelectWidget, self).create_option(name, value, label, selected, index, subindex=None,
#                                                                 attrs=None)
#
#         for x in self.option_style:
#             if option['value'] == x['name']:
#                 option['attrs'][x['attr_name']] = x['value']
#         return option
#


#
# class ExecutorSelectWidget(widgets.Select):
#     template_name = 'widgets/executer-dropdown.html'
#     option_template_name = 'widgets/executer-dropdown-options.html'
#
#     def __init__(self, attrs=None, choices=(),current_user=None):
#         super().__init__(attrs)
#         self.choices = list(choices)
#         self.current_user = current_user
#
#     def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
#         option = super(ExecutorSelectWidget, self).create_option(name, value, label, selected, index, subindex=None, attrs=None)
#         user = self.current_user
#         return option
#
#     def optgroups(self, name, value, attrs=None):
#         """Return a list of optgroups for this widget."""
#         groups = []
#         has_selected = False
#
#
#         for index, (option_value, option_label) in enumerate(self.choices):
#             if option_value is None:
#                 option_value = ''
#
#             subgroup = []
#             if isinstance(option_label, (list, tuple)):
#                 group_name = option_value
#                 subindex = 0
#                 choices = option_label
#             else:
#                 group_name = None
#                 subindex = None
#                 choices = [(option_value, option_label)]
#             groups.append((group_name, subgroup, index))
#
#             for subvalue, sublabel in choices:
#                 selected = (
#                     str(subvalue) in value and
#                     (not has_selected or self.allow_multiple_selected)
#                 )
#                 has_selected |= selected
#                 subgroup.append(self.create_option(
#                     name, subvalue, sublabel, selected, index,
#                     subindex=subindex, attrs=attrs,
#                 ))
#                 if subindex is not None:
#                     subindex += 1
#         return groups
#
#
#     def make_option(self,name,value,label,index,user=None):
#
#
#         return {
#             'name': name,
#             'value': value,
#             'label': label,
#             'index': index,
#             'type': self.input_type,
#             'template_name': self.option_template_name,
#             'wrap_label': True,
#             'user':user
#         }
#
#     def custome_options_set(self, name, value, attrs=None):
#         options_set = []
#
#         for index, (option_value, option_label) in enumerate(self.choices):
#
#             print(option_value,option_label)
#             if option_value == self.current_user.pk:
#                 break
#             user = None
#
#             if option_value != None and option_value != "":
#                 user=UserModel.objects.get(pk=option_value)
#             else:
#                 option_label = 'Any executer'
#
#             option = self.make_option(name=name,
#                                       value=option_value,
#                                       label=option_label,
#                                       index = index,
#                                       user=user)
#             options_set.append(option)
#
#         return options_set
#
#
#     def get_context(self, name, value, attrs):
#         context = super().get_context(name, value, attrs)
#         context['widget']['current_user'] = self.current_user
#         context['widget']['options'] = self.custome_options_set(name, context['widget']['value'], attrs)
#         return context



class TaskFilter(django_filters.FilterSet):

    # def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
    #     super().__init__(data=data,queryset=queryset,request=request,prefix=prefix)
    #     self.filters['executor'].extra['widget'].current_user = self.request.user

    #
    # status = django_filters.ChoiceFilter(choices=TASK_STATUSES,
    #                                      empty_label='Any status',
    #                                      widget=StatusSelectWidget(
    #                                      attrs={"class": 'selectpicker', 'data-width': 'fit'}))


    # executor = django_filters.ModelChoiceFilter(queryset=UserModel.objects.all(),
    #                                             widget=ExecutorSelectWidget(choices=(1,2,3),attrs={"class": 'selectpicker',
    #                                                                                "data-width": 'auto',
    #                                                                                "data-live-search": 'true'}))

    class Meta:
        model = Task
        fields = ['priority', 'project', 'executor', 'kind', 'status']



from django.db.models import Sum, Count

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
        for task in x.qs:

            task_files = task.task_files.all().aggregate(Count('id'))
            task.files_count = task_files['id__count']

            comments = task.task_comments.all().aggregate(Count('id'))
            task.comments_count= comments['id__count']

            all_time = task.time_set.all().aggregate(Sum('time'))
            task.all_time = all_time['time__sum']

            my_time=task.time_set.filter(tracker=self.request.user).aggregate(Sum('time'))
            task.my_time = my_time['time__sum']


        context['qs_set'] = x.qs

        return context

from .forms import ProjectForm

# @method_decorator(login_required, name='dispatch')
# @method_decorator(group_required(('ADMIN'), raise_exception=True), name='dispatch')
class CreateProjectView(View):

    def get(self, request, *args, **kwargs):
        form = ProjectForm()
        return render(self.request,template_name='projects-add.html',
                      context={'form':form})


    def post(self,request,*args,**kwargs):
        form = ProjectForm(data=self.request.POST,files=self.request.FILES)
        if form.is_valid():
            project_instance = form.save()
            return redirect('/projects/view/'+project_instance.slug+'/',permanent=True)
        else:
            return render(self.request, template_name='projects-add.html',
                          context={'form': form})

from django.views.decorators.csrf import csrf_exempt

# @method_decorator(login_required, name='dispatch')
# @method_decorator(group_required(('ADMIN'), raise_exception=True), name='dispatch')
class EditProjectView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects-edit.html'
    slug_field = 'slug'



    def get_success_url(self):
        project_slug = self.object.slug
        return '/projects/view/'+project_slug+'/'

@csrf_exempt
def TaskAssignView(request):
    if request.method == 'GET':
        return HttpResponse('API hit with post method',status=400)

    if request.method=='POST':
        task_id = request.POST.get('task_id',None)

        if task_id == None:
            return HttpResponse('No task id.', status=400)
        else:
            task = Task.objects.get(pk=task_id)
            if task.project.users.filter(pk=request.user.pk).exists():
                task.executor=request.user
                task.save()
                return HttpResponse('API hit with post method',status=200)
            else:
                return HttpResponse('Not assigned on project.', status=400)
