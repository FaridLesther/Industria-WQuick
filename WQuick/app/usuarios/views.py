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
from django.core.paginator import Paginator
from django.db.models import Q
from usuarios import forms, models
from usuarios.src.imagenPerfil import cargarImagen
from usuarios.src.solicitarProyecto import solicitarProyecto
from usuarios.src import leerNotificacion as leer, funciones

path = os.path.dirname(__file__)


class Registrar(CreateView):
    model = models.Usuario
    form_class = forms.FrmRegistar
    template_name = 'usuarios/registrar.html'

    def get(self, *args, **kwargs):
        if not (self.request.user.is_anonymous):
            return redirect('/')
        return super(Registrar, self).get(*args, **kwargs)

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
            servicios que ofrecemos: https://industriawquick.herokuapp.com/elige/

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
    template_name = 'usuarios/login.html'
    form_class = forms.FrmLogin
    success_url = reverse_lazy('inicio')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if('next' in self.request.GET):
            self.success_url = self.request.GET['next']

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
    return render(request, 'usuarios/elige.html', parametros)


class CrearProyecto(CreateView):
    # Vista para la plantilla crearProyecto.html
    model = models.Proyecto
    form_class = forms.FrmCrearProyecto
    template_name = 'usuarios/crearProyecto.html'
    success_url = reverse_lazy('misProyectos')

    def form_valid(self, form):
        fechaInicio = datetime.datetime.now()
        proyecto = form.save(True, self.request.user.id, fechaInicio)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(CrearProyecto, self).get_context_data(**kwargs)
        context['titulo'] = "Crear proyecto"
        return context


class SerFreelancer(CreateView):
    # Vista para la plantilla serFreelancer.html
    # Esta vista se usa en el registro de un freelancer
    model = models.Freelancer
    form_class = forms.FrmSerFreelancer
    template_name = 'usuarios/serFreelancer.html'

    def form_valid(self, form):
        freelancer = form.save(True, self.request.user.id)
        return redirect('/perfil')

    def get_context_data(self, **kwargs):
        context = super(SerFreelancer, self).get_context_data(**kwargs)
        context['titulo'] = "Ser Freelancer"
        return context

    def get(self, *args, **kwargs):
        idusuario = models.Freelancer.objects.filter(
            usuario_id=self.request.user.id)
        if idusuario:
            return redirect('/perfil')
        return super(SerFreelancer, self).get(*args, **kwargs)


class Perfil(CreateView):
    model = models.Usuario
    form_class = forms.FrmCambiarPass
    template_name = 'usuarios/perfilUsuario.html'

    def form_valid(self, form):
        usuario = form.save(True, self.request.user.id)
        return redirect('/perfil')

    def get_context_data(self, **kwargs):
        context = super(Perfil, self).get_context_data(**kwargs)
        freelancer = models.Freelancer.objects.filter(
            usuario_id=self.request.user.id).values()
        context['titulo'] = 'Perfil de usuario'
        context['freelancer'] = False
        if freelancer and freelancer.__len__() < 2:
            context['freelancer'] = freelancer[0]
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            return cargarImagen(self.request)
        else:
            response_kwargs.setdefault('content_type', self.content_type)
            return self.response_class(
                request=self.request,
                template=self.get_template_names(),
                context=context,
            )


def MisProyectos(request):
    mproyectos = models.Proyecto.objects.filter(
        usuario_id=request.user.id).values()
    # Paginator recibe una lista de objetos y la cantidad de
    # paginas  en la que se van a cortar
    paginacion = Paginator(mproyectos, 5)
    pagina = request.GET.get('pagina', 1)
    mproyectos = paginacion.get_page(pagina)
    # lista objetos contiene todos los proyectos que se van a
    # dibujar en la pagina
    parametros = {'titulo': 'Mis proyectos', 'listaObjetos': False}
    if mproyectos:
        parametros["listaObjetos"] = mproyectos
        parametros["paginacion"] = paginacion
    return render(request, 'usuarios/misProyectos.html', parametros)


class EditarPerfil(CreateView):
    model = models.Freelancer
    template_name = 'usuarios/editarPerfil.html'
    form_class = forms.FrmEditarFreelancer
    success_url = reverse_lazy('perfil')

    def form_valid(self, form):
        freelancer = form.save(True, self.request.user.id)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(EditarPerfil, self).get_context_data(**kwargs)
        context['titulo'] = 'Editar mi Perfil'
        freelancer = models.Freelancer.objects.filter(
            usuario_id=self.request.user.id).values()
        context['freelancer'] = False
        if freelancer and freelancer.__len__() < 2:
            context['freelancer'] = freelancer[0]

        return context


def buscarProyectos(request):
    mproyectos = models.Proyecto.objects.all().exclude(
        usuario_id=request.user.id).values()
    datos = {}
    for proyecto in mproyectos:
        datos[proyecto['titulo']] = '../static/img/diseñoweb.jpg'

    if request.GET.get('buscar'):
        busqueda = request.GET.get('buscar')
        mproyectos = models.Proyecto.objects.filter(
            (Q(titulo__icontains=busqueda) |
             Q(descripcion__icontains=busqueda)),
        ).exclude(usuario_id=request.user.id).values()

    paginacion = Paginator(mproyectos, 6)
    pagina = request.GET.get('pagina', 1)
    mproyectos = paginacion.get_page(pagina)

    # lista objetos contiene todos los proyectos que se van a dibujar en la pagina
    context = {'titulo': 'Proyectos', 'listaObjetos': False}

    if mproyectos:
        context["listaObjetos"] = mproyectos
        context["paginacion"] = paginacion
        context["busqueda"] = datos
        context["texto"] = 'Hola me gustaría trabajar en este proyecto'

    contexto = {'titulo': 'Buscar Proyectos'}

    if request.is_ajax():
        return solicitarProyecto(request)
    return render(request, 'usuarios/buscarProyectos.html', context)


class EditarProyecto(CreateView):
    model = models.Proyecto
    template_name = 'usuarios/editarProyecto.html'
    form_class = forms.FrmEditarProyecto
    success_url = reverse_lazy('misProyectos')

    def form_valid(self, form):
        proyecto = form.save(True, self.request.proyecto.id)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(EditarProyecto, self).get_context_data(**kwargs)
        context['titulo'] = 'Editar mi Proyecto'
        return context


def solicitudesF(request):
    contexto = {'titulo': 'Solicitudes de freelancers'}

    misProyectos = models.Proyecto.objects.filter(
        usuario_id=request.user.id).values('id')

    listaNotificaciones = funciones.misNotificaciones(request.user.id)

    nuevasNotificaciones = funciones.nuevasNotificaciones(request.user.id)

    if listaNotificaciones.__len__() > 0:
        contexto['notificaciones'] = nuevasNotificaciones
        contexto['numNotificaciones'] = nuevasNotificaciones.__len__()
        contexto['misNotificaciones'] = listaNotificaciones

    if request.is_ajax():
        return leer.leerNotificacion(request)

    return render(request, 'usuarios/solicitudesF.html', contexto)
