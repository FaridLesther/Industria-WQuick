from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from usuarios.models import Usuario


@csrf_exempt
def cargarImagen(request):
    if request.method == 'POST':
        if(request.FILES.get('imagen')):
            try:
                usuario = Usuario.objects.get(pk=request.user.id)
            except Usuario.DoesNotExist:
                usuario = None

            if(usuario):
                usuario.imagen = request.FILES.get('imagen')
                usuario.save()
                return JsonResponse(
                    {
                        'resultado': True,
                        'datos': {'img': str(usuario.imagen.url)},
                        'mensaje': 'Imagen actualizada correctamente'
                    }
                )
            else:
                return JsonResponse({'resultado': False, 'mensaje': 'El usuario no existe'})

    else:
        return JsonResponse({'resultado': False, 'mensaje': 'Error con el método del formulario'})
