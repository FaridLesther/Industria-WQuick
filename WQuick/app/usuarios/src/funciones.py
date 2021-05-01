from usuarios import models


def nuevasNotificaciones(id):
    misProyectos = models.Proyecto.objects.filter(
        usuario_id=id).values('id')

    listaNotificaciones = []
    for proyecto in misProyectos:
        notificaciones = models.Notificaciones.objects.filter(
            proyecto_id=proyecto['id'], noLeido=True).values()
        if notificaciones.exists():
            for notificacion in notificaciones:
                freelancer = models.Freelancer.objects.filter(
                    pk=notificacion['freelancer_id']).values()[0]

                notificacion['freelancer_id'] = freelancer['nombre'] + \
                    ' '+freelancer['apellido']
                listaNotificaciones.append(notificacion)
    return listaNotificaciones

def misNotificaciones(id):
    misProyectos = models.Proyecto.objects.filter(
        usuario_id=id).values('id')
    listaNotificaciones = []
    for proyecto in misProyectos:
        notificaciones = models.Notificaciones.objects.filter(
            proyecto_id=proyecto['id']).values()

        if notificaciones.exists():
            for notificacion in notificaciones:
                freelancer = models.Freelancer.objects.filter(
                    pk=notificacion['freelancer_id']).values()[0]

                notificacion['freelancer_id'] = freelancer['nombre'] + \
                    ' '+freelancer['apellido']
                listaNotificaciones.append(notificacion)
    return listaNotificaciones