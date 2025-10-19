from django.contrib import admin
from .models import Cliente, Contrato, Tarifa, Medidor, Lectura, Boleta, Pago, NotificacionLectura, NotificacionPago, Usuario

##Configuraciones para el admin de Django para los modelos del sistema
#se utilizan list_display, list_filter, search_fields y ordering para mejorar la usabilidad
#list display permite ver campos importantes en la lista
#list_filter permite filtrar por ciertos campos
#search_fields permite buscar por ciertos campos
#ordering permite ordenar por ciertos campos

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - CLIENTE
# ==========================================================
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('numero_cliente', 'nombre', 'email', 'telefono')
    list_filter = ('numero_cliente',)
    search_fields = ('numero_cliente', 'nombre', 'email')
    ordering = ('numero_cliente',)

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - CONTRATO
# ==========================================================
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('numero_contrato', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado', 'fecha_inicio')
    search_fields = ('numero_contrato',)
    ordering = ('-fecha_inicio',)

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - TARIFA
# ==========================================================
class TarifaAdmin(admin.ModelAdmin):
    list_display = ('fecha_vigencia', 'precio', 'tipo_tarifa', 'tipo_cliente')
    list_filter = ('tipo_tarifa', 'tipo_cliente')
    search_fields = ('tipo_tarifa', 'tipo_cliente')
    ordering = ('-fecha_vigencia',)

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - MEDIDOR
# ==========================================================
class MedidorAdmin(admin.ModelAdmin):
    list_display = ('numero_medidor', 'ubicacion', 'estado_medidor', 'fecha_instalacion')
    list_filter = ('estado_medidor', 'fecha_instalacion')
    search_fields = ('numero_medidor', 'ubicacion')
    ordering = ('numero_medidor',)

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - LECTURA
# ==========================================================
class LecturaAdmin(admin.ModelAdmin):
    list_display = ('fecha_lectura', 'consumo_energetico', 'tipo_lectura', 'lectura_actual')
    list_filter = ('tipo_lectura', 'fecha_lectura')
    search_fields = ('tipo_lectura',)
    ordering = ('-fecha_lectura',)

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - BOLETA
# ==========================================================
class BoletaAdmin(admin.ModelAdmin):
    list_display = ('fecha_emision', 'fecha_vencimiento', 'monto_total', 'estado')
    list_filter = ('estado', 'fecha_emision')
    search_fields = ('estado',)
    ordering = ('-fecha_emision',)

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - PAGO
# ==========================================================
class PagoAdmin(admin.ModelAdmin):
    list_display = ('fecha_pago', 'monto_pagado', 'metodo_pago', 'numero_referencia')
    list_filter = ('metodo_pago', 'estado_pago')
    search_fields = ('numero_referencia', 'metodo_pago')
    ordering = ('-fecha_pago',)

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - USUARIO
# ==========================================================
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol', 'telefono')
    list_filter = ('rol',)
    search_fields = ('username', 'email')
    ordering = ('username',)

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - NOTIFICACIONES
# ==========================================================
class NotificacionLecturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'registro_consumo')
    search_fields = ('registro_consumo',)
    ordering = ('id',)

class NotificacionPagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'deuda_pendiente')
    search_fields = ('deuda_pendiente',)
    ordering = ('id',)

# ==========================================================
# REGISTRO DE MODELOS EN EL ADMIN
# ==========================================================
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Tarifa, TarifaAdmin)
admin.site.register(Medidor, MedidorAdmin)
admin.site.register(Lectura, LecturaAdmin)
admin.site.register(Boleta, BoletaAdmin)
admin.site.register(Pago, PagoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(NotificacionLectura, NotificacionLecturaAdmin)
admin.site.register(NotificacionPago, NotificacionPagoAdmin)