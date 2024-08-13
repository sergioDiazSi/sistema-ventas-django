from django.db import models

# Create your models here.

class Categoria(models.Model):
    descripcion=models.CharField(max_length=30)
    estado=models.BooleanField(default=True)
    def __str__(self):
        return self.descripcion
    
class Unidad(models.Model):
    descripcion=models.CharField(max_length=30)
    estado=models.BooleanField(default=True)
    def __str__(self):
        return self.descripcion

class Producto(models.Model):
    idUnidad = models.ForeignKey(Unidad,on_delete=models.CASCADE)
    idCategoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=30)
    estado=models.BooleanField(default=True)
    stock = models.IntegerField()
    precio = models.FloatField()
    def __str__(self):
        return self.descripcion
    
class Cliente(models.Model):
    nombres = models.CharField(max_length=80)
    email = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    rucDni = models.CharField(max_length=11)
    estado = models.BooleanField(default=True)
    def __str__(self) -> str:
        return self.nombres
    
class Tipo(models.Model):
    descripcion = models.CharField(max_length=20)

class Parametros(models.Model):
    nroDoc = models.CharField(max_length=12)
    serie = models.CharField(max_length=3)

class CabeceraVenta(models.Model):
    fechaVenta = models.DateField()
    idParametros = models.ForeignKey(Parametros,on_delete=models.CASCADE)
    idTipo = models.ForeignKey(Tipo,on_delete=models.CASCADE)
    idCliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    nroDoc = models.CharField(max_length=12)
    subTotal = models.FloatField()
    igv = models.FloatField(default=0.18)
    total = models.FloatField()
    estado = models.BooleanField(default=True)

class DetalleVenta(models.Model):
    idCabeceraVenta = models.ForeignKey(CabeceraVenta,on_delete=models.CASCADE)
    idProducto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    precio = models.FloatField()
    cantidad = models.IntegerField()

    