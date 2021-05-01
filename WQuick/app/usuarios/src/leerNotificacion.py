from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from usuarios.models import Proyecto, Freelancer, Notificaciones


@csrf_exempt
def leerNotificacion(request):
    if request.method == 'POST':
        if(request.POST.get('idNotificacion') and request.POST.get('freelancer')):
            idNotificacion = request.POST.get('idNotificacion')
            freelancer = request.POST.get('freelancer')
            try:
                notificacion = Notificaciones.objects.get(pk=idNotificacion)
            except Notificaciones.DoesNotExist:
                notificacion = None

            if notificacion != None:
                notificacion.noLeido = False
                notificacion.save()
                datos = {}
                datos['asunto'] = notificacion.asunto
                datos['solicitud'] = notificacion.solicitud
                datos['freelancer'] = freelancer
                return JsonResponse({'resultado': True, 'mensaje': datos})
        else:
            return JsonResponse({'resultado': False, 'mensaje': 'Notificación erronea'})

    else:
        return JsonResponse({'resultado': False, 'mensaje': 'Error con el método del formulario'})
