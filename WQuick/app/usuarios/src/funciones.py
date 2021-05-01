from usuarios import models


def ordenarNotificaciones(listaIds, listaNotificaciones):
    listaOrdenada = []
    for id in sorted(listaIds, reverse=True):
        for notificacion in enumerate(listaNotificaciones):
            if id == notificacion[1]['id']:
                listaOrdenada.append(notificacion[1])
    return listaOrdenada


def nuevasNotificaciones(id):
    misProyectos = models.Proyecto.objects.filter(
        usuario_id=id).values('id')

    listaNotificaciones = []
    listaIds = []
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
                listaIds.append(notificacion['id'])

    listaOrdenada = ordenarNotificaciones(listaIds, listaNotificaciones)
    return listaOrdenada


def misNotificaciones(id):
    misProyectos = models.Proyecto.objects.filter(
        usuario_id=id).values('id')
    listaNotificaciones = []
    listaIds = []
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
                listaIds.append(notificacion['id'])

    listaOrdenada = ordenarNotificaciones(listaIds, listaNotificaciones)
    return listaOrdenada
