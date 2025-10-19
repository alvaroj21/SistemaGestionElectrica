# sistemaGestion/models.py
from django.db import models

#aca estan los modelos de la base de datos
#algunos modelos tienen campos con opciones predefinidas usando choices
#cada modelo tiene un metodo __str__ para representar el objeto como una cadena de texto
#esto es util para el admin de Django y otras interfaces cuando se muestran los objetos
#en listas o selecciones al relacionar modelos entre si

#ademas se incluye el charfield unique para asegurar que ciertos campos no se repitan en la base de datos
#y el max_length para limitar la longitud de los campos de texto
#tambien null=True y blank=True para permitir que ciertos campos sean opcionales.
class Cliente(models.Model):
    numero_cliente = models.CharField(max_length=45, unique=True)
    nombre = models.CharField(max_length=45)
    email = models.CharField(max_length=45, unique=True)
    telefono = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.numero_cliente} - {self.nombre}"

class Contrato(models.Model):
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo','Inactivo')
    ]
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo')
    numero_contrato = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return f"Contrato {self.numero_contrato} - {self.estado}"


class Tarifa(models.Model):
    TARIFA_CHOICES = [
        ('Verano','Verano'),
        ('Invierno','Invierno')
    ]
    CLIENTE_CHOICES = [
        ('Residencial','Residencial'),
        ('Comercial','Comercial'),
        ('Industrial','Industrial')
    ]
    fecha_vigencia = models.DateField()
    precio = models.PositiveIntegerField()
    tipo_tarifa = models.CharField(max_length=45, choices=TARIFA_CHOICES, default='Verano')
    tipo_cliente = models.CharField(max_length=45, choices=CLIENTE_CHOICES, default='Residencial')

    def __str__(self):
        return f"Tarifa {self.tipo_tarifa} - {self.tipo_cliente} (${self.precio}/kWh)"

class Medidor(models.Model):
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Mantenimiento', 'Mantenimiento'),
        ('Dañado', 'Dañado'),
    ]
    
    numero_medidor = models.CharField(max_length=45, unique=True)
    fecha_instalacion = models.DateField()
    ubicacion = models.CharField(max_length=45)
    estado_medidor = models.CharField(max_length=45, choices=ESTADO_CHOICES, default='Activo')
    imagen_ubicacion = models.URLField(max_length=200, blank=True, null=True)  # Imagen del mapa de ubicación
    imagen_fisica = models.URLField(max_length=200, blank=True, null=True)     # Imagen física del medidor

    def __str__(self):
        return f"Medidor {self.numero_medidor} - {self.ubicacion} ({self.estado_medidor})"

class Lectura(models.Model):
    TIPO_LECTURA_CHOICES = [
        ('Digital', 'Digital'),
        ('Analogica', 'Analógica'),
    ]
    
    fecha_lectura = models.DateField()
    consumo_energetico = models.PositiveIntegerField()
    tipo_lectura = models.CharField(max_length=45, choices=TIPO_LECTURA_CHOICES, default='Digital')
    lectura_actual = models.PositiveIntegerField()

    def __str__(self):
        return f"Lectura {self.fecha_lectura} - {self.consumo_energetico} kWh"



class Boleta(models.Model):
    BOLETA_CHOICES = [
        ('Pagado','Pagado'),
        ('Vencido','Vencido'),
        ('Pendiente','Pendiente')
    ]
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    monto_total = models.PositiveIntegerField()
    consumo_energetico = models.CharField(max_length=45)
    estado = models.CharField(max_length=45, choices=BOLETA_CHOICES, default='Pendiente')

    def __str__(self):
        return f"Boleta {self.fecha_emision} - ${self.monto_total} ({self.estado})"



class Pago(models.Model):
    PAGO_CHOICES = [
        ('Pagado','Pagado'),
        ('No pagado completamente', 'No pagado completamente')
    ]
    METODOPAGO_CHOICES = [
        ('Efectivo','Efectivo'),
        ('Transferencia','Transferencia'),
        ('Tarjeta','Tarjeta de Crédito'),
        ('Debito','Tarjeta de Débito')
    ]
    fecha_pago = models.DateField()
    monto_pagado = models.PositiveIntegerField()
    metodo_pago = models.CharField(max_length=45, choices=METODOPAGO_CHOICES)
    numero_referencia = models.CharField(max_length=45)
    estado_pago = models.CharField(max_length=45, choices=PAGO_CHOICES, default='Pagado')

    def __str__(self):
        return f"Pago {self.numero_referencia} - ${self.monto_pagado} ({self.metodo_pago})"



class NotificacionLectura(models.Model):
    registro_consumo = models.CharField(max_length=500)

    def __str__(self):
        return f"Notificación Lectura - {self.registro_consumo[:30]}..."


class NotificacionPago(models.Model):
    deuda_pendiente = models.CharField(max_length=500)

    def __str__(self):
        return f"Notificación Pago - {self.deuda_pendiente[:30]}..."



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

    def __str__(self):
        return f"{self.username} - {self.rol}"

