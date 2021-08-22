from django.contrib import admin
from django.urls import path
from usuarios.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', list_usuarios, name='list_usuarios'),
    path('create', create_usuario, name='create_usuario'),
    path('update/<int:id>', update_usuario, name='update_usuario'),
    path('delete/<int:id>', delete_usuario, name='delete_usuario'),
    path('login/', login_user),
    path('login/submit', submit_login),
    path('login/forgot/', forgot_password),
    path('register/', register),
    path('register/submit', submit_register),
    path('register/code/', confirmation_code),

    path('login/submit_login_google', submit_login_google),


    path('logout/', logout),

]
