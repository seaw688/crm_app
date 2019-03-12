from django.urls import path
from MAIN.views import IndexView, TestView
urlpatterns = [
    path('index/', IndexView.as_view() ),
    path('test/', TestView.as_view()),

]
