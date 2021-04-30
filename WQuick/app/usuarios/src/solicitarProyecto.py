from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from usuarios.models import Proyecto, Freelancer, Notificaciones


@csrf_exempt
def solicitarProyecto(request):
    if request.method == 'POST':
        if(request.POST.get('solicitud')):
            if not (request.POST.get('idProyecto') and request.POST.get('asunto')):
                return JsonResponse({'resultado': False, 'mensaje': 'El proyecto no existe'})

            idProyecto = request.POST.get('idProyecto')
            freelancer = Freelancer.objects.filter(
                usuario_id=request.user.id).values('id')

            if(freelancer.exists()):
                try:
                    notificacion = Notificaciones.objects.get(
                        proyecto_id=idProyecto, freelancer_id=freelancer[0]['id'])
                except Notificaciones.DoesNotExist:
                    notificacion = None
                if not(notificacion == None):
                    return JsonResponse({'resultado': False, 'mensaje': 'Usted ya ha enviado una solicitud a este proyecto'})

                notificacion = Notificaciones()
                notificacion.freelancer_id = freelancer[0]['id']
                notificacion.proyecto_id = idProyecto
                notificacion.asunto = request.POST.get('asunto')
                notificacion.solicitud = request.POST.get('solicitud')
                notificacion.save()

                return JsonResponse({'resultado': True, 'mensaje': 'Solicitud enviada correctamente'})
            else:
                return JsonResponse({'resultado': False, 'mensaje': 'El freelancer no existe'})
        else:
            return JsonResponse({'resultado': False, 'mensaje': 'Asegurese de enviar una solicitud'})

    else:
        return JsonResponse({'resultado': False, 'mensaje': 'Error con el método del formulario'})
