from django.contrib import admin
from usuarios import models
# Register your models here.
admin.site.register(models.Usuario)
admin.site.register(models.Proyecto)
admin.site.register(models.Freelancer)
admin.site.register(models.Notificaciones)
