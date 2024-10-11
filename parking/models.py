from django.db import models

class Vehiculo(models.Model):
    TIPO_CHOICES = [
        ('Automóvil', 'Automóvil'),
        ('Moto', 'Moto'),
    ]
    
    id_vehiculo = models.CharField(max_length=6, primary_key=True)
    tipo_vehiculo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    
    def __str__(self):
        return f"{self.id_vehiculo} ({self.tipo_vehiculo})"
    
    class Meta:
        app_label = 'parking'

class UsuarioFrecuente(models.Model):
    id_usuario = models.CharField(max_length=10, primary_key=True)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    nombre_U = models.CharField(max_length=100)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    contraseña = models.CharField(max_length=128)
    email = models.EmailField()
    
    def __str__(self):
        return self.nombre_U
    
    class Meta:
        app_label = 'parking'

class Tarifa(models.Model):
    CHOICES_TARIFA = [
        ('Pagar día', 'Pagar día'),
        ('Pagar hora', 'Pagar hora'),
        ('Recargar saldo', 'Recargar saldo'),
    ]
    id_tarifa = models.CharField(max_length=20, choices=CHOICES_TARIFA, primary_key=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id_tarifa} ({self.cost})"
    
    class Meta:
        app_label = 'parking'

class Transaccion(models.Model):
    id_transaccion = models.CharField(max_length=10, primary_key=True)
    id_tarifa = models.ForeignKey(Tarifa, on_delete=models.CASCADE)
    id_vehicle = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    
    class Meta:
        app_label = 'parking'