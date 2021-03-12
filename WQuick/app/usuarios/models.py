from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_user(self, nombre, correo, password):
        # metodo que se utilizara para crear usuarios
        usuario = self.model(nombre=nombre, correo=correo)
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, nombre, correo, password):
        # metodo que se utilizara para crear usuarios administradores
        usuario = self.create_user(
            nombre=nombre,
            correo=correo,
            password=password
        )
        usuario.admin = True
        usuario.save()
        return usuario

class Usuario(AbstractBaseUser):
    # modelo que enlazara con la tabla de la base de datos usuario
    nombre = models.CharField(
        'Nombre de usuario', max_length=15, unique=True)
    imagen = models.ImageField('Imagen de perfil', upload_to='perfil/',
                            height_field=None, width_field=None, max_length=200,
                            blank=True, null=True
                            )
    correo = models.EmailField(
        'Correo electronico', max_length=60, blank=False, null=False)

    admin = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    objects = UsuarioManager()

    USERNAME_FIELD = 'nombre'
    REQUIRED_FIELDS = 'Correo'

    def __str__(self):
        # metodo de sobrescritura de la funcion to_string esto representa
        # que se mostrara al imprimir el objeto usuario
        return f'{self.nombre}, {self.correo}'

    def has_perm(self, perm, obj=None):
        #  metodo para poder usar este modelo en el administrador de jango
        #  es llamado en la parte de los permisos de quien puede o no acceder
        #  administrador de django y lo maneja automaticament
        return True

    def has_module_perms(self, app_label):
        #  metodo utilizado para el admin de djando recibe como parametro la
        #  etiqueta de la aplicación donde esta este modelo
        return True

    @property
    def is_staff(self):
        # metodo que sera utilizado para saber si un usuario es administrador
        # o usuario comun
        return self.admin
