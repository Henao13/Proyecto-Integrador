from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Vehiculo)
admin.site.register(models.UsuarioFrecuente)
admin.site.register(models.Tarifa)
admin.site.register(models.Transaccion)