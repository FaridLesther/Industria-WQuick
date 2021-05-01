from datetime import datetime
import time
from django import forms
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from usuarios import models


class FrmRegistar(UserCreationForm):
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
    password1.widget.attrs['style'] = 'background-color: #212121; margin-left:17px; border-radius: 2px;width: 77%;border: 1px solid #000;height: 5vh;'

    password2 = forms.CharField(widget=forms.PasswordInput())
    password2.widget.attrs['id'] = 'txt_cclave'
    password2.widget.attrs['style'] = 'background-color: #212121; margin-left:17px; border-radius: 2px;width: 77%;border: 1px solid #000;height: 5vh;'

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
                    'class': 'grey darken-4',
                    'id': 'txt_usuario',
                    'type': 'text',
                    'style': 'margin-left:17px; border-radius: 2px;width: 77%;border: 1px solid #000;height: 5vh;',
                    'required': 'required',
                    'maxlength': '25',
                }
            ),
            'correo': forms.TextInput(
                attrs={
                    'class': 'grey darken-4',
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


class FrmLogin(AuthenticationForm):
    #  Formulario de inicio de sesión (Login)
    #  Autor: Lesther Valladares
    #  Version: 0.0.1
    #  Variables:
    #    -  nombre: nombre de usuario registrado en la base de datos
    #    -  password: contraseña del usuario que ingresara al programa
    def __init__(self, *args, **kwargs):
        super(FrmLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'white-text grey darken-4'
        self.fields['username'].widget.attrs['id'] = 'txt_usuario'
        self.fields['username'].widget.attrs['style'] = 'border-radius: 2px;width: 60%;border: 1px solid #000;height: 5vh;'

        self.fields['password'].widget.attrs['class'] = 'white-text grey darken-4'
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


class FrmCrearProyecto(forms.ModelForm):
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

    moneda = (
        ('L.', 'L.'),
        ('$.', '$.'),
        ('€.', '€.'),
    )

    tipo = forms.CharField(max_length=30)
    tipo.widget.attrs['style'] = 'display: none;'
    tipo.widget.attrs['id'] = 'txt_tipo'

    fecha = forms.CharField(required=True)
    fecha.widget.attrs['id'] = 'data'
    fecha.widget.attrs['class'] = 'datepicker'
    fecha.widget.attrs['onkeypress'] = 'return false;'

    xp = forms.ChoiceField(label='Elija una opción', choices=nivelesXP)

    moneda = forms.ChoiceField(label='Moneda', choices=moneda)

    #  Modelo del cual sera construido el formulario: Proyecto
    #  es necesario especificar por lo menos un campo del modelo

    class Meta:
        model = models.Proyecto
        fields = ('tipo', 'titulo', 'descripcion', 'presupuesto')
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
                    'style': 'max-width: 100%; height:135px;border: 1px dotted #848484; color: #fb8c00;',
                    'required': 'required',
                }
            ),
            'presupuesto': forms.TextInput(
                attrs={
                    'class': 'validate',
                    'id': 'txt_presupuesto',
                    'type': 'number',
                    'style': 'margin-top: 15px;',
                    'required': 'required',
                    'value': '1000',
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

    def clean_presupuesto(self):
        try:
            valor = int(self.cleaned_data.get('presupuesto'))
            if valor < 99:
                raise forms.ValidationError(
                    'El presupuesto debe ser mayor que 100')
            return valor
        except ValueError:
            raise forms.ValidationError(
                'El presupuesto solo debe tener números')

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
        proyecto.moneda = self.cleaned_data.get('moneda')

        if commit:
            proyecto.save()
        return proyecto


class FrmSerFreelancer(forms.ModelForm):
    #  Formulario de registro de un freelancer en la base de datos
    #  Autor: Lesther Valladares
    #  Version: 0.0.1
    #  modelo: Freelancer

    listaIdiomas = (
        ('Ingles', 'Ingles'),
        ('Chino', 'Chino'),
        ('Alemán', 'Alemán'),
        ('Francés', 'Francés'),
        ('Portugués', 'Portugués'),
        ('Japonés', 'Japonés'),
    )

    nivelesXP = (
        (1, "Básico"),
        (2, "Medio"),
        (3, "Intermedio"),
        (4, "Avanzado"),
    )

    idiomas = forms.MultipleChoiceField(choices=listaIdiomas, required=False)
    idiomas.widget.attrs['class'] = 'browser-default'
    idiomas.widget.attrs['style'] = 'display: none;'

    xp = forms.ChoiceField(label='Elija una opción', choices=nivelesXP)
    xp.widget.attrs['class'] = 'form-control browser-default'
    xp.widget.attrs['style'] = 'width: 100%; color:#d6d6d6; background-color:#212121; border-color:#212121;'

    class Meta:
        model = models.Freelancer
        fields = ('nombre', 'apellido', 'correo',
                  'profesion', 'telefono', 'descripcion',)
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control browser-default',
                    'style': 'width: 100%; color:#d6d6d6; background-color:#212121; border-color:#212121;',
                    'type': 'text',
                    'required': 'required',
                }
            ),
            'apellido': forms.TextInput(
                attrs={
                    'class': 'form-control browser-default',
                    'style': 'width: 100%; color:#d6d6d6; background-color:#212121; border-color:#212121;',
                    'type': 'text',
                    'required': 'required',
                }
            ),
            'correo': forms.TextInput(
                attrs={
                    'class': 'form-control browser-default',
                    'style': 'width: 100%; color:#d6d6d6; background-color:#212121; border-color:#212121;',
                    'type': 'text',
                    'required': 'required',
                }
            ),
            'profesion': forms.TextInput(
                attrs={
                    'class': 'form-control browser-default',
                    'style': 'width: 100%; color:#d6d6d6; background-color:#212121; border-color:#212121;',
                    'type': 'text',
                    'required': 'required',
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'form-control browser-default',
                    'style': 'width: 100%; color:#d6d6d6; background-color:#212121; border-color:#212121;',
                    'type': 'text',
                    'required': 'required',
                }
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'rows': '5',
                    'class': 'form-control browser-default',
                    'id': 'txt-descripcion',
                    'placeholder': 'Tecnologías dominadas, especialidades, entre otras cualidades.',
                    'style': 'width: 100%; color:#d6d6d6; background-color:#212121; border-color:#212121;',
                    'required': 'required',
                }
            ),
        }

    def clean_telefono(self):
        telefono = str(self.cleaned_data.get('telefono'))
        if telefono.__len__() < 8:
            raise forms.ValidationError('Debe introducir un telefono válido')
        if telefono[0] != '+':
            return '+504'+self.cleaned_data.get('telefono')
        return self.cleaned_data.get('telefono')

    def clean_idiomas(self):
        if len(self.cleaned_data.get('idiomas')) > 6:
            raise forms.ValidationError(
                'Más idiomas seleccionados de los disponibles')
        return self.cleaned_data.get('idiomas')

    def clean_correo(self):
        # filtrar mayusculas del correo electronico
        correo = self.cleaned_data.get('correo').lower()
        return correo

    def save(self, commit=True, usuario=-1):
        try:
            freelancer = models.Freelancer.objects.get(usuario_id=usuario)
        except models.Freelancer.DoesNotExist:
            freelancer = None

        if freelancer == None:
            freelancer = super().save(commit=False)
            freelancer.usuario_id = usuario
            freelancer.xp = self.cleaned_data.get('xp')
            freelancer.idiomas = self.cleaned_data.get('idiomas')
        if commit:
            freelancer.save()
        return freelancer


class FrmCambiarPass(forms.ModelForm):
    #  Formulario de cambio de clave de usuario
    #  Autor: Lesther Valladares
    #  Version: 0.0.1
    #  modelo: Usuario
    aClave = forms.CharField(widget=forms.PasswordInput())
    aClave.widget.attrs['id'] = 'txt-clave'
    aClave.widget.attrs['style'] = 'width: 80%;'
    aClave.widget.attrs['disabled'] = 'disabled'

    confirmarClave = forms.CharField(widget=forms.PasswordInput())
    confirmarClave.widget.attrs['id'] = 'txt-cclave'
    confirmarClave.widget.attrs['style'] = 'width: 80%;'
    confirmarClave.widget.attrs['disabled'] = 'disabled'

    campo = forms.CharField(widget=forms.PasswordInput(), required=False)
    campo.widget.attrs['id'] = 'txt-campo'
    campo.widget.attrs['style'] = 'display:none;'

    class Meta:
        model = models.Usuario
        fields = ('password',)
        widgets = {
            'password': forms.PasswordInput(
                attrs={
                    'required': 'required',
                    'type': 'password',
                    'id': 'txt-nclave',
                    'style': 'width: 80%;',
                    'disabled': 'disabled'
                }
            )
        }

    def clean_campo(self):
        clave = self.cleaned_data.get('aClave')
        idUsuario = self.cleaned_data.get('campo')

        if idUsuario:
            claveActual = models.Usuario.objects.filter(
                id=idUsuario).values('password')
        else:
            claveActual = [{'password': -1}]

        claveNueva = self.cleaned_data.get('password')

        usuario = models.Usuario()
        usuario.password = claveActual[0]['password']

        if(not usuario.check_password(clave)):
            raise forms.ValidationError(
                'La contraseña actual es inválida')

        if(usuario.check_password(claveNueva)):
            raise forms.ValidationError(
                'La nueva contraseña es la actual, debe ingresar una nueva contraseña')

    def clean_confirmarClave(self):
        nuevaClave = self.cleaned_data.get('password')
        confirmarClave = self.cleaned_data.get('confirmarClave')

        if nuevaClave != confirmarClave:
            raise forms.ValidationError(
                'Las nuevas contraseñas no coinciden')
        return nuevaClave

    def save(self, commit=True, idUsuario=-1):
        usuario = models.Usuario.objects.get(pk=idUsuario)
        usuario.password = make_password(self.cleaned_data.get('password'))
        if commit:
            usuario.save()
        return usuario


class FrmEditarFreelancer(forms.ModelForm):
    #  Formulario de registro de un freelancer en la base de datos
    #  Autor: Lesther Valladares
    #  Version: 0.0.1
    #  modelo: Freelancer

    listaIdiomas = (
        ('Ingles', 'Ingles'),
        ('Chino', 'Chino'),
        ('Alemán', 'Alemán'),
        ('Francés', 'Francés'),
        ('Portugués', 'Portugués'),
        ('Japonés', 'Japonés'),
    )

    nivelesXP = (
        (1, "Básico"),
        (2, "Medio"),
        (3, "Intermedio"),
        (4, "Avanzado"),
    )

    correo = forms.CharField(required=True)
    correo.widget.attrs['class'] = 'grey-text text-lighten-2'

    idiomas = forms.MultipleChoiceField(choices=listaIdiomas, required=False)
    idiomas.widget.attrs['class'] = 'browser-default'
    idiomas.widget.attrs['style'] = 'display: none;'

    xp = forms.ChoiceField(label='Elija una opción', choices=nivelesXP)
    xp.widget.attrs['style'] = 'width: 100%;'

    class Meta:
        model = models.Freelancer
        fields = ('nombre', 'apellido',
                  'profesion', 'telefono', 'descripcion',)
        widgets = {

            'apellido': forms.TextInput(
                attrs={
                    'class': 'grey-text text-lighten-2',
                    'type': 'text',
                    'required': 'required',
                }
            ),
            'profesion': forms.TextInput(
                attrs={
                    'class': 'grey-text text-lighten-2',
                    'type': 'text',
                    'required': 'required',
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'grey-text text-lighten-2',
                    'type': 'text',
                    'required': 'required',
                }
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'rows': '5',
                    'class': 'grey-text text-lighten-2',
                    'id': 'txt-descripcion',
                    'placeholder': 'Tecnologías dominadas, especialidades, entre otras cualidades.',
                    'style': 'width: 100%;',
                    'required': 'required',
                }
            ),
        }

    def clean_telefono(self):
        telefono = str(self.cleaned_data.get('telefono'))
        if telefono.__len__() < 8:
            raise forms.ValidationError('Debe introducir un telefono válido')
        if telefono[0] != '+':
            return '+504'+self.cleaned_data.get('telefono')
        return self.cleaned_data.get('telefono')

    def clean_idiomas(self):
        if len(self.cleaned_data.get('idiomas')) > 6:
            raise forms.ValidationError(
                'Más idiomas seleccionados de los disponibles')
        return self.cleaned_data.get('idiomas')

    def clean_correo(self):
        # filtrar mayusculas del correo electronico
        correo = self.cleaned_data.get('correo').lower()
        return correo

    def save(self, commit=True, usuario=-1):
        try:
            freelancer = models.Freelancer.objects.get(usuario_id=usuario)
            freelancer.nombre = self.cleaned_data.get('nombre')
            freelancer.apellido = self.cleaned_data.get('apellido')
            freelancer.correo = self.cleaned_data.get('correo')
            freelancer.profesion = self.cleaned_data.get('profesion')
            freelancer.telefono = self.cleaned_data.get('telefono')
            freelancer.descripcion = self.cleaned_data.get('descripcion')
            freelancer.xp = self.cleaned_data.get('xp')
            freelancer.idiomas = self.cleaned_data.get('idiomas')
            if commit:
                freelancer.save()
        except models.Freelancer.DoesNotExist:
            freelancer = None
        return freelancer


class FrmEditarProyecto(forms.ModelForm):
    #  Formulario de edicion de proyectos en la base de datos
    #  modelo: Proyectos
    class Meta:
        model = models.Proyecto
        fields = ('titulo', 'tipo', 'descripcion',
                  'xp', 'fecha_inicio', 'fecha_fin')
        widgets = {
            'titulo': forms.TextInput(
                attrs={
                    'class': 'grey-text text-lighten-2',
                    'type': 'text',
                    'required': 'required',
                }
            ),
            'tipo': forms.TextInput(
                attrs={
                    'class': 'grey-text text-lighten-2',
                    'type': 'text',
                    'required': 'required',
                }
            ),
            'xp': forms.TextInput(
                attrs={
                    'class': 'grey-text text-lighten-2',
                    'type': 'text',
                    'required': 'required',
                }
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'rows': '5',
                    'class': 'grey-text text-lighten-2',
                    'id': 'txt-descripcion',
                    'placeholder': 'Proporciona una breve descripcion acerca de tu proyecto',
                    'style': 'width: 100%;',
                    'required': 'required',
                }
            ),
        }

    def save(self, commit=True, usuario=-1):
        try:
            proyecto = models.Proyecto.objects.get(usuario_id=usuario)
            proyecto.titulo = self.cleaned_data.get('titulo')
            proyecto.descripcion = self.cleaned_data.get('descripcion')
            proyecto.tipo = self.cleaned_data.get('tipo')
            proyecto.xp = self.cleaned_data.get('xp')
            if commit:
                proyecto.save()
        except models.Proyecto.DoesNotExist:
            proyecto = None
        return proyecto
