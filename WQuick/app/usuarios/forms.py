from django import forms
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from usuarios import models
from datetime import datetime
import time


class frmRegistar(UserCreationForm):
    #  Formulario de registro de un usuario en la base de datos
    #  Autor: Lesther Valladares
    #  Version: 0.0.1
    #  Variables:
    #    -  nombre: nombre de usuario que se registrara
    #    -  password1: contraseña del usuario
    #    -  password2: confirmación de contraseña del usuario
    #    -  admin: contiene el valor booleano para el administrador
    password1 = forms.CharField(widget=forms.PasswordInput())
    password1.widget.attrs['id'] = 'txt_clave'
    password1.widget.attrs['style'] = 'margin-left:17px; border-radius: 2px;width: 77%;border: 1px solid #000;height: 5vh;'

    password2 = forms.CharField(widget=forms.PasswordInput())
    password2.widget.attrs['id'] = 'txt_cclave'
    password2.widget.attrs['style'] = 'margin-left:17px; border-radius: 2px;width: 77%;border: 1px solid #000;height: 5vh;'

    admin = forms.BooleanField(initial=False, required=False)
    admin.widget.attrs['class'] = 'filled-in'
    admin.widget.attrs['value'] = 'false'

    class Meta:
        #  Modelo del cual sera contruido el formulario: Usuario
        #  es necesario especificar por lo menos un campo del modelo
        model = models.Usuario
        fields = ('nombre', 'correo',)
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'black-text',
                    'id': 'txt_usuario',
                    'type': 'text',
                    'style': 'margin-left:17px; border-radius: 2px;width: 77%;border: 1px solid #000;height: 5vh;',
                    'required': 'required',
                    'maxlength': '25',
                }
            ),
            'correo': forms.TextInput(
                attrs={
                    'class': 'black-text',
                    'id': 'txt_correo',
                    'type': 'text',
                    'style': 'margin-left:17px; border-radius: 2px;width: 77%;border: 1px solid #000;height: 5vh;',
                    'required': 'required',
                }
            ),
        }

    def clean_nombre(self):
        # metodo para obviar mayusculas y minusculas en el nombre de usuario
        nombre = self.cleaned_data.get('nombre')
        usuarioEncontrado = models.Usuario.objects.filter(
            Q(nombre__iexact=nombre) | Q(correo__iexact=nombre))

        if usuarioEncontrado:
            raise forms.ValidationError('Nombre de usuario no disponible')
        return nombre

    def clean_correo(self):
        # filtrar mayusculas del correo electronico
        correo = self.cleaned_data.get('correo').lower()
        return correo

    def clean_password2(self):
        #  Metodo de validación de los dos campos de contraseña
        # se valida que ambos tengan el mismo contenido
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('La contraseñas no coinciden')
        return password2


class frmLogin(AuthenticationForm):
    #  Formulario de inicio de sesión (Login)
    #  Autor: Lesther Valladares
    #  Version: 0.0.1
    #  Variables:
    #    -  nombre: nombre de usuario registrado en la base de datos
    #    -  password: contraseña del usuario que ingresara al programa
    def __init__(self, *args, **kwargs):
        super(frmLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'validate black-text'
        self.fields['username'].widget.attrs['id'] = 'txt_usuario'
        self.fields['username'].widget.attrs['style'] = 'border-radius: 2px;width: 60%;border: 1px solid #000;height: 5vh;'

        self.fields['password'].widget.attrs['class'] = 'validate black-text'
        self.fields['password'].widget.attrs['id'] = 'txt_clave'
        self.fields['password'].widget.attrs['style'] = 'border-radius: 2px;width: 60%;border: 1px solid #000;height: 5vh;'

    def clean_username(self):
        # metodo para obviar mayusculas y minusculas en el nombre de usuario
        nombre = self.cleaned_data.get('username')

        usuarioEncontrado = models.Usuario.objects.filter(
            Q(nombre__iexact=nombre) |
            Q(correo__iexact=nombre)
        ).values('nombre')

        if usuarioEncontrado:
            nombre = usuarioEncontrado[0]['nombre']
        else:
            raise forms.ValidationError(
                'Nombre de usuario o correo electrónico incorrecto')
        return nombre


class frmCrearProyecto(forms.ModelForm):
    #  Formulario de registro de un proyecto en la base de datos
    #  Autor: Lesther Valladares
    #  Version: 0.0.1
    #  modelo: Proyecto

    nivelesXP = (
        (1, "Básico"),
        (2, "Medio"),
        (3, "Intermedio"),
        (4, "Avanzado"),
    )

    tipo = forms.CharField(max_length=30)
    tipo.widget.attrs['style'] = 'display: none;'
    tipo.widget.attrs['id'] = 'txt_tipo'

    fecha = forms.CharField(required=True)
    fecha.widget.attrs['id'] = 'data'
    fecha.widget.attrs['class'] = 'datepicker'
    fecha.widget.attrs['onkeypress'] = 'return false;'

    xp = forms.ChoiceField(label='Elija una opción', choices=nivelesXP)

    #  Modelo del cual sera construido el formulario: Proyecto
    #  es necesario especificar por lo menos un campo del modelo

    class Meta:
        model = models.Proyecto
        fields = ('tipo', 'titulo', 'descripcion',)
        widgets = {
            'titulo': forms.TextInput(
                attrs={
                    'class': 'validate',
                    'id': 'txt_titulo',
                    'type': 'text',
                    'required': 'required',
                }
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'cols': '60',
                    'rows': '9',
                    'id': 'txt-descripcion',
                    'placeholder': 'Descipción del Proyecto',
                    'style': 'max-width: 100%; height:135px;border: 1px dotted #848484;',
                    'required': 'required',
                }
            ),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        titulo = titulo.replace('<', '')
        titulo = titulo.replace('>', '')
        titulo = titulo.replace('\\', '')
        return titulo

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        descripcion = descripcion.replace('<', '')
        descripcion = descripcion.replace('>', '')
        descripcion = descripcion.replace('\\', '')
        return descripcion

    def save(self, commit=True, usuario=-1, fechaInicio=None):
        proyecto = super().save(commit=False)
        proyecto.tipo = self.cleaned_data.get('tipo')
        proyecto.usuario_id = usuario
        proyecto.fecha_inicio = fechaInicio

        fecha_fin = self.cleaned_data.get('fecha')
        fecha_fin = fecha_fin + time.strftime(' %H:%M:%S', time.localtime())
        fecha_fin = datetime.strptime(fecha_fin, '%d-%m-%Y %H:%M:%S')

        proyecto.fecha_fin = fecha_fin
        proyecto.xp = self.cleaned_data.get('xp')

        if commit:
            proyecto.save()
        return proyecto
