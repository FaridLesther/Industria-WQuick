import datetime
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from usuarios.models import Proyecto, Contrataciones, Notificaciones


@csrf_exempt
def leerNotificacion(request):
    if request.method == 'POST':
        if(request.POST.get('contratar') == '1'):
            idNotificacion = request.POST.get('idNotificacion')
            freelancer = request.POST.get('freelancer')
            try:
                notificacion = Notificaciones.objects.get(pk=idNotificacion)
            except Notificaciones.DoesNotExist:
                notificacion = None
            if notificacion != None:
                contratacion = Contrataciones.objects.filter(
                    freelancer_id=notificacion.freelancer_id, proyecto_id=notificacion.proyecto_id
                ).values()

                if contratacion.exists():
                    return JsonResponse({'resultado': False, 'mensaje': 'Ya tiene contratado este usuario para este proyecto'})
                freelancerContratado = Contrataciones()
                freelancerContratado.freelancer_id = notificacion.freelancer_id
                freelancerContratado.proyecto_id = notificacion.proyecto_id
                freelancerContratado.fechaContratacion = datetime.datetime.now()
                freelancerContratado.save()
                datos = {}
                datos['url'] = reverse_lazy('fContratados')
                return JsonResponse({'resultado': 'contratado', 'mensaje': datos})

        elif(request.POST.get('idNotificacion') and request.POST.get('freelancer')):
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
                datos['id'] = notificacion.id
                return JsonResponse({'resultado': True, 'mensaje': datos})
        else:
            return JsonResponse({'resultado': False, 'mensaje': 'Notificación erronea'})

    else:
        return JsonResponse({'resultado': False, 'mensaje': 'Error con el método del formulario'})
