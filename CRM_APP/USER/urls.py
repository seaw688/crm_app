from django.urls import path
from .views import LoginView, LogoutView, SignUpView
urlpatterns = [
    path('login/', LoginView.as_view(), name="login_page"),
    path('logout/', LogoutView.as_view(), name="logut_page"),
    path('sign-up/', SignUpView.as_view(), name="sign_up_page"),

]
