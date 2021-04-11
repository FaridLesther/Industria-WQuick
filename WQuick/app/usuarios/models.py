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
        'Nombre de usuario', max_length=50, unique=True)

    imagen = models.ImageField(
        'Imagen de perfil', upload_to='perfil/',
        height_field=None, width_field=None,
        max_length=200, blank=True, null=True
    )

    correo = models.EmailField(
        'Correo electronico', max_length=50,
        blank=False, null=False, unique=True
    )

    admin = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    objects = UsuarioManager()

    USERNAME_FIELD = 'nombre'
    REQUIRED_FIELDS = ['correo']

    def __str__(self):
        # metodo de sobrescritura de la funcion to_string esto representa
        # que se mostrara al imprimir el objeto usuario
        return f'nombre: {self.nombre}, correo: {self.correo}, admin: {self.admin}'

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


class Proyecto(models.Model):
    #  Modelo para la tabla proyecto en la base de datos
    #  Autor: Lesther Valladares
    #  Version: 0.0.1
    #  Atributos:
    #    -  usuario: Llave foranea de el usuario que crea el proyecto
    #    -  tipo: Representa el tipo de categoria al que pertenece el proyecto
    #    -  titulo: Contiene el titulo del proyecto(obligatorio)
    #    -  descripcion: Contiene una descripcon del proyecto(obligatorio)
    #    -  xp: Campo numerico para puntuar la experiencia requerida del freelancer
    #    -  fecha_inicio: Fecha de creacion del proyecto
    #    -  fecha_fin: Fecha en la que se espera que termine el proyecto
    usuario = models.ForeignKey(Usuario, null=False, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=30)
    titulo = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=500)
    xp = models.IntegerField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
