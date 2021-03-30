from django.urls import path
from django.contrib.auth.decorators import login_required
from usuarios import views

urlpatterns = [
    path('accounts/login/', views.Login.as_view(), name='login'),
    path('logout/', login_required(views.logoutUsuario), name='logout'),
    path('registrar', views.Registrar.as_view(), name='registrar'),
    path('elige', views.elige, name='elegir'),
    path('crearProyecto', login_required(views.CrearProyecto.as_view()), name="crearProyecto"),
]
