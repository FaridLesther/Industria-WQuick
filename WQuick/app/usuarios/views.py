import datetime
import os
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from usuarios import forms, models

path = os.path.dirname(__file__)


#def login(request):
 #   parametros = {"titulo": 'Login'}
 #  return render(request, 'Login.html', parametros)


#def registrar(request):
    #parametros = {"titulo": 'Registrar'}
    #return render(request, 'Registrar.html', parametros)
