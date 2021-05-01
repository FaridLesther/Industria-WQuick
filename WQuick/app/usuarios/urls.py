from django.urls import path
from django.contrib.auth.decorators import login_required
from usuarios import views

urlpatterns = [
    path('accounts/login/', views.Login.as_view(), name='login'),
    path('logout/', login_required(views.logoutUsuario), name='logout'),
    path('registrar', views.Registrar.as_view(), name='registrar'),
    path('elige', views.elige, name='elegir'),
    path('crearProyecto', login_required(
        views.CrearProyecto.as_view()), name="crearProyecto"),
    path('serFreelancer', login_required(
        views.SerFreelancer.as_view()), name='serFreelancer'),
    path('perfil', login_required(views.Perfil.as_view()), name='perfil'),
    path('misProyectos', login_required(views.MisProyectos), name='misProyectos'), 
    path('editarPerfil', login_required(views.EditarPerfil.as_view()), name='editarPerfil'),
    path('buscarProyectos', views.buscarProyectos, name='buscarProyectos'),
    path('editarProyecto', login_required(views.EditarProyecto.as_view()), name='editarProyecto'),
    path('solicitudesFreel', login_required(views.solicitudesF), name='solicitudesF'),
]
