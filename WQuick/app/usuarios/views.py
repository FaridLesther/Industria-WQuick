import datetime
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.mail import send_mail
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
        nombre = form.cleaned_data.get('nombre')
        remitente = settings.EMAIL_HOST_USER
        contenido = f"""
            Te damos la bienvenida {nombre} a WQuick
            
            Puedes acceder a tu cuenta de WQuick iniciando sesión
            en el siguiente enlace: https://industriawquick.herokuapp.com/login/

            Te invitamos a que publiques tus proyectos o trabajes como freelancer con los
            servicios que ofrecemos: https://www.freelancermap.com/blog/es/sobre-freelancermap/

            Fecha de registro: {datetime.datetime.now().strftime('%d/%m/%Y')}
        """
        destinatarios = [form.cleaned_data.get('correo')]
        send_mail('Registro exitoso a WQuick',
                  contenido, remitente, destinatarios)
        login(self.request, usuario)
        return redirect('/elige')

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


def elige(request):
    parametros = {"titulo": 'Elige una opción'}
    return render(request, 'usuarios/SeleccionarDeseas.html', parametros)


class CrearProyecto(CreateView):
    model = models.Proyecto
    form_class = forms.frmCrearProyecto
    template_name = 'usuarios/CrearProyecto.html'

    def form_valid(self, form):
        fechaInicio = datetime.datetime.now()
        proyecto = form.save(True, self.request.user.id, fechaInicio)
        return redirect('/')

    def get_context_data(self, **kwargs):
        context = super(CrearProyecto, self).get_context_data(**kwargs)
        context['titulo'] = "Crear proyecto"
        return context
