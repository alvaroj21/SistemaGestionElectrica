# sistemaGestion/models.py
from django.db import models

class Cliente(models.Model):
    numero_cliente = models.CharField(max_length=45)
    nombre = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    telefono = models.CharField(max_length=15)

class Contrato(models.Model):
    ESTADO_CHOICES =[
        ('Activo', 'Activo'),
        ('Inactivo','Inactivo')
    ]
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo')
    numero_contrato = models.CharField(max_length=45)


class Tarifa(models.Model):
    TARIFA_CHOICES =[
        ('Verano','Verano'),
        ('Invierno','Invierno')

    ]
    CLIENTE_CHOICES =[
        ('Residencial','Residencial'),
        ('Comercial','Comercial'),
        ('Industrial','Industrial')
    ]
    fecha_vigencia = models.DateField()
    precio = models.IntegerField()
    tipo_tarifa = models.CharField(max_length=45,choices=TARIFA_CHOICES, default='Verano')
    tipo_cliente = models.CharField(max_length=45,choices=CLIENTE_CHOICES,default='Residencial')

class Medidor(models.Model):
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Mantenimiento', 'Mantenimiento'),
        ('Dañado', 'Dañado'),
    ]
    
    numero_medidor = models.CharField(max_length=45)
    fecha_instalacion = models.DateField()
    ubicacion = models.CharField(max_length=45)
    estado_medidor = models.CharField(max_length=45, choices=ESTADO_CHOICES, default='Activo')
    imagen_ubicacion = models.URLField(max_length=200, blank=True, null=True, help_text="URL de la imagen de ubicación del medidor")

class Lectura(models.Model):
    TIPO_LECTURA_CHOICES = [
        ('Digital', 'Digital'),
        ('Analogica', 'Analógica'),
    ]
    
    fecha_lectura = models.DateField()
    consumo_energetico = models.CharField(max_length=45)
    tipo_lectura = models.CharField(max_length=45, choices=TIPO_LECTURA_CHOICES, default='Digital')
    lectura_actual = models.CharField(max_length=45)



class Boleta(models.Model):
    BOLETA_CHOICES =[
        ('Pagado','Pagado'),
        ('Vencido','Vencido')
    ]
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    monto_total = models.IntegerField()
    consumo_energetico = models.CharField(max_length=45)
    estado = models.CharField(max_length=45, choices=BOLETA_CHOICES)



class Pago(models.Model):
    PAGO_CHOICES =[
        ('Pagado','Pagado'),
        ('No pagado', 'No pagado')
    ]
    METODOPAGO_CHOICES =[
        ('Efectivo','Efectivo'),
        ('Transferencia','Transferencia')
    ]
    fecha_pago = models.DateField()
    monto_pagado = models.IntegerField()
    metodo_pago = models.CharField(max_length=45, choices=METODOPAGO_CHOICES)
    numero_referencia = models.CharField(max_length=45)
    estado_pago = models.CharField(max_length=45, choices=PAGO_CHOICES)



class NotificacionLectura(models.Model):
    registro_consumo = models.CharField(max_length=45)



class NotificacionPago(models.Model):
    deuda_pendiente = models.CharField(max_length=45)



class Usuario(models.Model):
    ROLES_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Eléctrico', 'Eléctrico'),
        ('Finanzas', 'Finanzas'),
    ]
    
    username = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=45)
    telefono = models.CharField(max_length=15)
    rol = models.CharField(max_length=45, choices=ROLES_CHOICES)

