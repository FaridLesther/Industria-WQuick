import datetime
import os
# shortcuts-> modulo para  renderizar plantillas html de forma rapida
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

path = os.path.dirname(__file__)


def inicio(request):
    # Funcion que renderiza la vista para la pagina de inicio
    # tiene conexion con la vista que esta en la carpeta template/index.html
    # revisar esta funcion en las rutas que estan en urls.py
    # version 0.0.1

    # diccionario con parametros que se cargaran en la plantilla html
    parametros = {"titulo": 'Inicio'}
    return render(request, 'index.html', parametros)
