"""
URL configuration for keicinema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from cine import views
from accounts import views as aviews
from users import views as bviews
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from admins import views as adm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('cartelera', views.cartelera, name = 'pelicula'),
    path('confiteria', views.confiteria, name = 'confiteria'),
    path('promociones', views.promociones, name = 'promociones'),
    path('contacto', views.contacto),
    path('login', aviews.loginV, name='login'),
    # path('register', aviews.register),
    path('forgotpassword', aviews.forgotpassword),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name='password_reset_complete'),
    #path('login/', bviews.login_view, name='login'),
    #path('register/', bviews.register_view, name='register'),
    #path('profile/', bviews.profile_view, name='profile'),
    path('logout/', aviews.cerrar_sesion, name='logout'),
    path('signup', aviews.signup), 
    path('compras', views.compras, name = 'compras'),
    path('detalle/<int:id>/', views.detalle, name= 'detalle'),
    path('carteleraAdmin', adm.Cartelera_admin, name = 'carteleraAdmin'),
    path('peliculasAdmin', adm.Peliculas_admin, name = 'peliculasAdmin'),
    path('adminfunciones', adm.Administrar_cartelera, name = 'AdminFunciones'),
    path('addfunction', adm.addfunction, name = 'addfunction'),
    path('agregarPeliculas', adm.agregar_pelicula, name = 'agregarPeliculas'),
    path('addPeliculas', adm.addPeliculas, name = 'addPeliculas'),
    path('agregarSalas', adm.admin_sala, name = 'agregarSalas'),
    path('addsala', adm.addsala, name = 'addsala'),
    path('getseats/<int:id_funcion>/', views.obtener_asientos, name='obtener_asientos'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
