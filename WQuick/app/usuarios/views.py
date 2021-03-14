import datetime
import os
from django.shortcuts import render, redirect
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


class Registrar(CreateView):
    model = models.Usuario
    form_class = forms.frmRegistar
    template_name = 'usuarios/Registrar.html'

    def form_valid(self, form):
        # Si el formulario es valido se guarda lo que se obtiene de él en una variable usuario
        # luego se hace login con ese usuario y se redirige al index
        usuario = form.save()
        login(self.request, usuario)
        return redirect('/')
    
    def get_context_data(self, **kwargs):
        context = super(Registrar, self).get_context_data(**kwargs)
        context['titulo'] = "Registro de usuarios"
        return context


class Login(FormView):
    template_name = 'usuarios/Login.html'
    form_class = forms.frmLogin
    success_url = reverse_lazy('inicio')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Capturamos el contexto del padre.
        context = super(Login, self).get_context_data(**kwargs)
        context['titulo'] = "Login"  # Le agregamos la información necesaria.
        return context  # Retornamos el contexto.


def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/')
