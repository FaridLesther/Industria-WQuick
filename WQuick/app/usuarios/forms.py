from django import forms
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from usuarios import models


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
    password1.widget.attrs['style'] = 'border-radius: 2px;width: 90%;border: 1px solid #000;height: 5vh;'

    password2 = forms.CharField(widget=forms.PasswordInput())
    password2.widget.attrs['id'] = 'txt_cclave'
    password2.widget.attrs['style'] = 'border-radius: 2px;width: 90%;border: 1px solid #000;height: 5vh;'

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
                    'style': 'border-radius: 2px;width: 90%;border: 1px solid #000;height: 5vh;',
                    'required': 'required',
                    'maxlength': '25',
                }
            ),
            'correo': forms.TextInput(
                attrs={
                    'class': 'black-text',
                    'id': 'txt_correo',
                    'type': 'text',
                    'style': 'border-radius: 2px;width: 90%;border: 1px solid #000;height: 5vh;',
                    'required': 'required',
                }
            ),
        }

    def clean_nombre(self):
        # metodo para obviar mayusculas y minusculas en el nombre de usuario
        nombre = self.cleaned_data.get('nombre')
        usuarioEncontrado = models.Usuario.objects.filter(
            nombre__iexact=nombre)
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
            Q(nombre__iexact=nombre) | Q(correo__iexact=nombre))

        if usuarioEncontrado:
            nombre = usuarioEncontrado[0]
        else:
            raise forms.ValidationError('Nombre de usuario o correo electrónico incorrecto')
        return nombre
    