from django.urls import path
from MAIN.views import IndexView, ProjectsView
urlpatterns = [
    path('index/', IndexView.as_view() ),
    path('projects/', ProjectsView.as_view(), name='projects_page'),

]
