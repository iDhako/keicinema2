from django.shortcuts import render
from cine.models import Peliculas, Productos_confiteria, Funciones, Sala
from django.contrib import messages
from datetime import timedelta
from django.contrib.auth.decorators import login_required, user_passes_test

def es_admin_cine(user):
    return user.groups.filter(name='Administracion').exists()


@login_required
@user_passes_test(es_admin_cine)  
def Cartelera_admin(request):
    funciones = Funciones.objects.all()
    return render(request, "pages/funcionesadmin.html", {'funciones': funciones})

@login_required
@user_passes_test(es_admin_cine) 
def Administrar_cartelera(request):
    peliculas = Peliculas.objects.all()
    sala = Sala.objects.all()
    return render(request, "pages/adminfunciones.html", {'peliculas': peliculas, 'sala': sala})

@login_required
@user_passes_test(es_admin_cine)
def Peliculas_admin(request):
    listPelicula = Peliculas.objects.all()
    return render(request, "pages/peliculasadmin.html", {'pelicula': listPelicula})

@login_required
@user_passes_test(es_admin_cine)
def addfunction(request):
    if request.method == "POST":
        pelicula_id = int(request.POST.get('pelicula'))  # Obtener el ID de la película
        sala_id = int(request.POST.get('sala'))  # Obtener el ID de la sala
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        precio = int(request.POST.get('precio'))
        
        # Obtener las instancias de la película y la sala
        try:
            pelicula = Peliculas.objects.get(id=pelicula_id)
            sala = Sala.objects.get(id=sala_id)
        except Peliculas.DoesNotExist:
            messages.error(request, "La película seleccionada no existe.")
            return render(request, 'pages/adminfunciones.html')
        except Sala.DoesNotExist:
            messages.error(request, "La sala seleccionada no existe.")
            return render(request, 'pages/adminfunciones.html')

        # Crear la función
        purchase = Funciones.objects.create(
            id_sala=sala,  # Asignar la instancia de Sala
            id_peliculas=pelicula,  # Asignar la instancia de Peliculas
            fecha_funcion=fecha,
            hora_funcion=hora,
            precio_funcion=precio,
        )
        purchase.save()

        # Mensaje de éxito
        messages.success(request, f'¡Función Creada Correctamente!, Película: {pelicula.titulo}, Fecha: {purchase.fecha_funcion}, Hora: {purchase.hora_funcion}.')
        
        # Redirigir o renderizar la misma página
        return render(request, 'pages/adminfunciones.html')

@login_required
@user_passes_test(es_admin_cine)
def editar_funciones(request, funcion_id):

    try:
        funcion = Funciones.objects.get(id=funcion_id)  # Buscar la función por su ID
        pelicula = Pelicula.objects.get(pk=funcion.id_pelicula)
        peliculas = peliculas.objects.all()
        sala = Sala.objetcs
    except Funciones.DoesNotExist:
        messages.error(request, "La función seleccionada no existe.")
        return render(request, 'pages/funcionesadmin.html')

    if request.method == "POST":
        # Obtener los nuevos datos desde el formulario
        pelicula_id = int(request.POST.get('pelicula'))
        sala_id = int(request.POST.get('sala'))
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        precio = int(request.POST.get('precio'))

        # Obtener las instancias de la película y la sala
        try:
            pelicula = Peliculas.objects.get(id=pelicula_id)
            sala = Sala.objects.get(id=sala_id)
        except Peliculas.DoesNotExist:
            messages.error(request, "La película seleccionada no existe.")
            return render(request, 'pages/adminfunciones.html')
        except Sala.DoesNotExist:
            messages.error(request, "La sala seleccionada no existe.")
            return render(request, 'pages/adminfunciones.html')

        # Actualizar la función
        funcion.id_peliculas = pelicula
        funcion.id_sala = sala
        funcion.fecha_funcion = fecha
        funcion.hora_funcion = hora
        funcion.precio_funcion = precio
        funcion.save()

        # Mensaje de éxito
        messages.success(request, f'¡Función Actualizada Correctamente!, Película: {pelicula.titulo}, Fecha: {funcion.fecha_funcion}, Hora: {funcion.hora_funcion}.')
            
        return render(request, 'pages/funcionesadmin.html')
        
    return render(request, 'pages/editarfuncion.html', {'funcion': funcion})        

@login_required
@user_passes_test(es_admin_cine)
def eliminar_funcion(request, funcion_id):
    try:
        funcion = Funciones.objects.get(id=funcion_id)  # Buscar la función por su ID
    except Funciones.DoesNotExist:
        messages.error(request, "La función seleccionada no existe.")
        return render(request, 'pages/funcionesadmin.html')

    # Eliminar la función
    funcion.delete()

    # Mensaje de éxito
    messages.success(request, "¡Función eliminada correctamente!")

    return render(request, 'pages/funcionesadmin.html')

@login_required
@user_passes_test(es_admin_cine)
def agregar_pelicula(request):
    Pelicula = Peliculas.objects.all()
    return render(request, "pages/agregarpeliculas.html", {'pelicula': Pelicula})

@login_required
@user_passes_test(es_admin_cine) 
def addPeliculas(request):    
    if request.method == 'POST':

        # Obtener los datos del formulario
        titulo = request.POST.get('titulo')
        sinopsis = request.POST.get('sinopsis')
        duracion = request.POST.get('duracion')
        clasificacion = request.POST.get('clasificacion')
        genero = request.POST.get('genero')
        fecha_estreno = request.POST.get('fecha_estreno')
        estado_peliculas = request.POST.get('estado_peliculas')
        valor_peliculas = int(request.POST.get('valor_peliculas'))
        director = request.POST.get('director')
        imagen_url = request.POST.get('imagen_url')
        reparto = request.POST.get('reparto')
        titulo_original = request.POST.get('titulo_original')
        trailer_url = request.POST.get('trailer_url')

        try:
            duracion_segundos = int(duracion)  # Convertir a entero (segundos)
            duracion_timedelta = timedelta(seconds=duracion_segundos)  # Crear un timedelta con los segundos
        except ValueError:
            messages.error(request, 'La duración debe ser un número válido en segundos.')
            return render(request, 'pages/agregar_pelicula.html')

        # duracion_timedelta = timedelta(minutes=int(duracion))

        # Crear una nueva instancia de Peliculas con los datos del formulario
        purchase = Peliculas.objects.create(
            titulo=titulo,
            sinopsis=sinopsis,
            duracion=duracion_timedelta,
            clasificacion=clasificacion,
            genero=genero,
            fecha_estreno=fecha_estreno,
            estado_peliculas=estado_peliculas,
            valor_peliculas=valor_peliculas,
            director=director,
            imagen_url=imagen_url,
            reparto=reparto,
            titulo_original=titulo_original,
            trailer_url=trailer_url
        )
        
        # Guardar la película en la base de datos
        purchase.save()

        # Mensaje de éxito
        messages.success(request, f'¡Pelicula Creada Correctamente!, Película: {purchase.titulo}.')
        

        # Redirigir al usuario a una página de éxito (puedes cambiar esta redirección a donde desees)
        return render(request, 'pages/agregarpeliculas.html')
    else:
        # Si el método no es POST, muestra el formulario vacío
        return render(request, 'pages/agregarpeliculas.html')

@login_required
@user_passes_test(es_admin_cine)
def admin_sala(request):
    sala = Sala.objects.all()
    return render(request, "pages/agregarsalas.html", {'sala': sala})

@login_required
@user_passes_test(es_admin_cine)
def addsala(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        numero_sala = request.POST.get('numero_sala')
        numero_butaca = request.POST.get('numero_butaca')

        # Crear una nueva instancia de Sala con los datos del formulario
        sala = Sala(
            numero_sala=numero_sala,
            numero_butaca=numero_butaca
        )
        
        # Guardar la sala en la base de datos
        sala.save()

        # Mensaje de éxito
        messages.success(request, f'Sala {numero_sala} con numero de butacas {numero_butaca} creadas correctamente.')

        # Redirigir a una página de éxito
        return render(request,'pages/agregarsalas.html') 

    else:
        # Si el método no es POST, muestra el formulario vacío
        return render(request, 'pages/agregarsalas.html')