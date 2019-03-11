from django.urls import path
from MAIN.views import IndexView
urlpatterns = [
    path('index/', IndexView.as_view() ),
]
