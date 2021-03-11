from django.urls import path
from django.contrib.auth.decorators import login_required
from usuarios import views

urlpatterns = [
    path('login', views.login, name="login"),
    path('registrar', views.registrar, name="registrar"),
]
