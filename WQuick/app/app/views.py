import datetime
import os
# shortcuts-> modulo para  renderizar plantillas html de forma rapida
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Count
from usuarios import models

path = os.path.dirname(__file__)


def inicio(request):
    # Funcion que renderiza la vista para la pagina de inicio
    # tiene conexion con la vista que esta en la carpeta template/index.html
    # revisar esta funcion en las rutas que estan en urls.py
    # version 0.0.1

    # diccionario con parametros que se cargaran en la plantilla html
    parametros = {"titulo": 'Inicio'}

    datos = {}
    freelancers = models.Freelancer.objects.all().values(
        'usuario_id', 'nombre'
    ).annotate(Count('usuario_id')).order_by('-usuario_id')[:10]

    usuarios = models.Usuario.objects.all().values(
        'id', 'imagen'
    ).annotate(Count('id')).order_by('-id')[:10]

    for freelancer in freelancers:
        for imagen in usuarios:
            if freelancer['usuario_id'] == imagen['id']:
                if imagen['imagen'] == '':
                    datos[freelancer['nombre']] = ''
                else:
                    datos[freelancer['nombre']] = 'media/'+imagen['imagen']

    parametros['freelancers'] = datos
    return render(request, 'e.html', parametros)
