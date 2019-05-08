from django.urls import path
from MAIN.views import IndexView, ProjectsView, ProjectsDetailView,\
                    TasksView,CreateProjectView
urlpatterns = [
    path('index/', IndexView.as_view() ),
    path('projects/', ProjectsView.as_view(), name='projects_page'),
    path('projects/add/', CreateProjectView.as_view(), name='projects_add_page'),
    path('projects/<slug:slug>/', ProjectsDetailView.as_view(), name='project_detail_page'),
    path('tasks/', TasksView.as_view(), name='tasks_page'),


]
