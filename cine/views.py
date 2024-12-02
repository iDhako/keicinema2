from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django import template
from .models import Peliculas, Productos_confiteria, Funciones, Sala
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods

def index(request):
    return render(request, "pages/index.html")

def cartelera(request):
    Pelicula = Peliculas.objects.all()

    return render(request, "pages/cartelera.html", {'pelicula': Pelicula})

def confiteria(request):
    Confiteria = Productos_confiteria.objects.all()
    return render(request, "pages/confiteria.html", {'confiteria': Confiteria})

def promociones(request):
    productos = Productos_confiteria.objects.all()
    for producto in productos:
        producto.descuento_productos = int(producto.descuento_productos * 100)
    return render(request, 'pages/promociones.html', {'promociones': productos})

def contacto(request):
    return render(request, "pages/contacto.html")

def compras(request):
    if request.method == "POST":
        # Obtener el ID de la función desde el POST
        funcion_id = int(request.POST.get('funcion_id'))
        
        # Obtener la función correspondiente
        funcion = Funciones.objects.get(pk=funcion_id)
        
        # Obtener la película relacionada usando la relación id_peliculas
        pelicula = Peliculas.objects.get(pk=funcion.id_peliculas.pk)
        
        # Obtener la confitería y las salas
        confiteria = Productos_confiteria.objects.all()
        salas = Sala.objects.filter(funciones=funcion)  # O filtrar según cómo estén relacionadas las salas
        
        # Pasar los datos al template
        return render(request, "pages/compras.html", {
            'pelicula': pelicula,
            'confiteria': confiteria,
            'sala': salas
        })
    else:
        return render(request, "pages/error.html", {"mensaje": "Método no permitido"})


def detalle(request, id):
    pelicula = Peliculas.objects.get(pk=id)
    funciones = Funciones.objects.filter(id_peliculas=id)

    # Agrupar por días y agregar el id de la función junto con la hora
    funciones_por_dia = {}
    for funcion in funciones:
        fecha = funcion.fecha_funcion.strftime("%d-%b-%Y")
        if fecha not in funciones_por_dia:
            funciones_por_dia[fecha] = []
        funciones_por_dia[fecha].append({'id': funcion.id, 'hora': funcion.hora_funcion})

    return render(request, "pages/detalle.html", {'pelicula': pelicula, 'funciones_por_dia': funciones_por_dia})



@require_http_methods(["GET", "POST"])
def purchase_process(request):
    if request.method == "POST":
        # Procesar la compra
        cantidad_tickets = int(request.POST.get('ticketQuantity'))
        seleccion_butaca = request.POST.get('selectedSeats').split(',')
        metodo_pago = request.POST.get('paymentMethod')

        # Crear la compra
        purchase = Productos_confiteria.objects.create(
            ticket_quantity=cantidad_tickets,
            payment_method=metodo_pago
        )

        # Asociar las butacas seleccionadas
        for seat_number in seleccion_butaca:
            Productos_confiteria.objects.create(
                purchase=purchase,
                seat_number=int(seat_number)
            )

        # Procesar los snacks seleccionados
        for key, value in request.POST.items():
            if key.startswith('snack_quantity_'):
                nombre_producto = key.replace('snack_quantity_', '')
                quantity = int(value)
                if quantity > 0:
                    Productos_confiteria.objects.create(
                        purchase=purchase,
                        name=nombre_producto,
                        quantity=quantity
                    )

        # Redireccionar a una página de confirmación
        return redirect('purchase_confirmation', purchase_id=purchase.id)

    # Si es GET, mostrar el formulario
    return render(request, 'purchase_form.html')

def purchase_confirmation(request, purchase_id):
    purchase = Productos_confiteria.objects.get(id=purchase_id)
    return render(request, 'purchase_confirmation.html', {'purchase': purchase})

def obtener_asientos(request, id_funcion):
    try:
        funcion = Funciones.objects.get(id=id_funcion)
        asientos_ocupados = Sala.objects.filter(
            id=funcion.id_sala_id
        ).values_list('numero_butaca', flat=True)

        data = {
            'status': 'success',
            'asientos_libres' : list(asientos_libres),
            'asientos_ocupados': list(asientos_ocupados),
            'titulo': funcion.id_peliculas_id.titulo,
            'fecha_funcion': funcion.fecha_funcion,
            'hora_funcion': funcion.hora_funcion.strftime('%H:%M'),
            'sala': funcion.id_sala_id.numero_sala,
        }
    except Funciones.DoesNotExist:
        data = {'status': 'error', 'message': 'Función no encontrada'}  

    return JsonResponse(data)