from .views import *
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('login', login_user, name="login-user"),
    path('logout', logout_user, name="logout-user"),
    path('informations', informations, name="informations-user"),
    path('update', update_user, name="update-user"),
    path('change-password', update_password, name="change-password"),
]
