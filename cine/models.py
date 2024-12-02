from django.db import models

# Create your models here.

class Peliculas (models.Model):
   
    titulo=models.CharField(max_length=100)
    sinopsis=models.CharField(max_length=500)
    duracion=models.DurationField()
    clasificacion=models.CharField(max_length=3)
    genero=models.CharField(max_length=20)
    fecha_estreno=models.DateField(auto_now=False, auto_now_add=False)
    estado_peliculas=models.CharField(max_length=10)
    valor_peliculas=models.IntegerField(max_length=10)
    director=models.CharField(max_length=100)
    imagen_url=models.CharField(max_length=500)
    reparto=models.CharField(max_length=100)
    titulo_original=models.CharField(max_length=100)
    trailer_url=models.CharField(max_length=500)   

class Sala (models.Model):
    
    numero_sala=models.CharField(max_length=2)
    numero_butaca=models.CharField(max_length=2)


class Funciones (models.Model):

    id_sala=models.ForeignKey(Sala, on_delete=models.CASCADE)
    id_peliculas=models.ForeignKey(Peliculas, on_delete=models.CASCADE)
    fecha_funcion=models.DateField(auto_now=False, auto_now_add=False)
    hora_funcion=models.TimeField(auto_now=False, auto_now_add=False)
    precio_funcion=models.IntegerField(default=1)



class Tickets (models.Model):
    id_funcion=models.ForeignKey(Funciones, on_delete=models.CASCADE)
    asiento=models.CharField(max_length=2)
    estado_ticket=models.CharField(max_length=10)
    dia_expiracion=models.CharField(max_length=20)


class Productos_confiteria (models.Model):
    nombre_producto=models.CharField(max_length=100)
    descripcion_producto=models.CharField(max_length=100)
    precio_producto=models.CharField(max_length=20)
    stock_producto=models.CharField(max_length=10)
    descuento_productos=models.FloatField()
    

class Usuarios (models.Model):
    nombre_usuario=models.CharField(max_length=20)
    correo_electronico=models.CharField(max_length=10)
    contrasena=models.CharField(max_length=20)
    
    

class Descuentos (models.Model):
    codigo_descuento=models.CharField(max_length=50)
    usuario=models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    
class Carrito (models.Model):
    usuario=models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    peliculas_carrito=models.CharField(max_length=10)
    confiteria_carrito=models.CharField(max_length=10)


class Venta (models.Model):
    id_tickets=models.ForeignKey(Tickets, on_delete=models.CASCADE)
    id_usuario=models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    id_confiteria=models.ForeignKey(Productos_confiteria, on_delete=models.CASCADE)
    fecha_compra=models.DateField(auto_now=False, auto_now_add=False)
    estado_venta=models.CharField(max_length=10)
