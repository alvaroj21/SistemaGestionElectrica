# sistemaGestion/admin.py
from django.contrib import admin
from .models import Cliente, Contrato, Tarifa, Medidor, Lectura, Boleta, Pago, Usuario, Notification

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'nombre', 'numero_cliente', 'email', 'telefono')
    search_fields = ('nombre', 'numero_cliente', 'email')
    list_filter = ('nombre',)

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('identificato', 'numero_contrato', 'cliente_id_cliente', 'estado', 'fecha_inicio')
    search_fields = ('numero_contrato', 'estado')
    list_filter = ('estado', 'cliente_id_cliente')

@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display = ('id_tarifa', 'tipo_tarifa', 'precio', 'fecha_vigencia', 'contrato_id_contrato')
    search_fields = ('tipo_tarifa', 'tipo_cliente')
    list_filter = ('tipo_tarifa',)

@admin.register(Medidor)
class MedidorAdmin(admin.ModelAdmin):
    list_display = ('id_medidor', 'numero_medidor', 'ubicacion', 'estado_medidor', 'contrato_id_contrato')
    search_fields = ('numero_medidor', 'ubicacion')
    list_filter = ('estado_medidor',)

@admin.register(Lectura)
class LecturaAdmin(admin.ModelAdmin):
    list_display = ('id_lectura', 'fecha_lectura', 'lectura_actual', 'tipo_lectura', 'medidor_id_medidor')
    search_fields = ('fecha_lectura', 'tipo_lectura')
    list_filter = ('tipo_lectura',)

@admin.register(Boleta)
class BoletaAdmin(admin.ModelAdmin):
    list_display = ('id_boleta', 'fecha_emision', 'monto_total', 'estado', 'lectura_id_lectura')
    search_fields = ('estado',)
    list_filter = ('estado',)

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id_pago', 'fecha_pago', 'monto_pagado', 'estado_pago', 'numero_referencia')
    search_fields = ('estado_pago', 'metodo_pago')
    list_filter = ('estado_pago', 'metodo_pago')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombre', 'email', 'rol')
    search_fields = ('nombre', 'email', 'rol')
    list_filter = ('rol',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id_notification', 'tipo_notification', 'estado_notification', 'fecha_generation', 'usuario_id_usuario')
    search_fields = ('tipo_notification', 'estado_notification')
    list_filter = ('tipo_notification', 'estado_notification')