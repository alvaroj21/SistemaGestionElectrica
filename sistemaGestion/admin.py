
from django.contrib import admin
from .models import Cliente, Contrato, Tarifa, Medidor, Lectura, Boleta, Pago, NotificacionLectura, NotificacionPago, Usuario

# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('numero_cliente', 'nombre', 'email', 'telefono')
admin.site.register(Cliente, ClienteAdmin)

class ContratoAdmin(admin.ModelAdmin):
    list_display = ('numero_contrato', 'fecha_inicio', 'fecha_fin', 'estado')
admin.site.register(Contrato, ContratoAdmin)

class MedidorAdmin(admin.ModelAdmin):
    list_display = ('numero_medidor', 'fecha_instalacion', 'ubicacion', 'estado_medidor')
admin.site.register(Medidor, MedidorAdmin)

class LecturaAdmin(admin.ModelAdmin):
    list_display = ('fecha_lectura', 'consumo_energetico', 'tipo_lectura', 'lectura_actual')
admin.site.register(Lectura, LecturaAdmin)

class BoletaAdmin(admin.ModelAdmin):
    list_display = ('fecha_emision', 'fecha_vencimiento', 'monto_total', 'consumo_energetico', 'estado')
admin.site.register(Boleta, BoletaAdmin)

class PagoAdmin(admin.ModelAdmin):
    list_display = ('fecha_pago', 'monto_pagado', 'metodo_pago', 'numero_referencia', 'estado_pago')
admin.site.register(Pago, PagoAdmin)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'email', 'telefono', 'rol')
admin.site.register(Usuario, UsuarioAdmin)

class TarifaAdmin(admin.ModelAdmin):
    list_display = ('fecha_vigencia', 'precio', 'tipo_tarifa', 'tipo_cliente')
admin.site.register(Tarifa, TarifaAdmin)

class NotificacionLecturaAdmin(admin.ModelAdmin):
    list_display = ('registro_consumo',)
admin.site.register(NotificacionLectura, NotificacionLecturaAdmin)

class NotificacionPagoAdmin(admin.ModelAdmin):
    list_display = ('deuda_pendiente',)
admin.site.register(NotificacionPago, NotificacionPagoAdmin)    
