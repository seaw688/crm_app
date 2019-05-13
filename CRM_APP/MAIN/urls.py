from django.urls import path,re_path
from MAIN.views import IndexView, ProjectsView, ProjectsDetailView,\
                    TasksView,CreateProjectView, EditProjectView, TaskAssignView
urlpatterns = [
    path('index/', IndexView.as_view() ),
    path('projects/', ProjectsView.as_view(), name='projects_page'),
    path('projects/add/', CreateProjectView.as_view(), name='projects_add_page'),
    path('projects/view/<slug:slug>/', ProjectsDetailView.as_view(), name='projects_detail_page'),
    re_path(r'^projects/edit/(?P<slug>[-\w]+)/$', EditProjectView.as_view(), name='projects_edit_page'),
    path('tasks/', TasksView.as_view(), name='tasks_page'),
    path('tasks/assign/', TaskAssignView, name='tasks_assign_page'),

]
