from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render, redirect
from MAIN.models import Task, Project
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required, login_required


class IndexView(View):
    def get(self, request, *args, **kwargs):
        print(request.user.get_all_permissions())
        if request.user.has_perm('MAIN.add_project'):
            return HttpResponse('ok')
        else:
            return HttpResponse('not ok')
        # return render(request,'default.html')


@method_decorator(permission_required(('MAIN.add_project'), raise_exception=True), name='dispatch')
@method_decorator(login_required, name='dispatch')
class ProjectsView(ListView):
    model = Project
    template_name = "test.html"
    context_object_name = 'projects'
