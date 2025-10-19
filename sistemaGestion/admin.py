from django.contrib import admin
from django.contrib import messages
from datetime import date
from .models import Cliente, Contrato, Tarifa, Medidor, Lectura, Boleta, Pago, NotificacionLectura, NotificacionPago, Usuario

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - CLIENTE
# ==========================================================
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('numero_cliente', 'nombre', 'email', 'telefono')
    list_filter = ('numero_cliente',)
    search_fields = ('numero_cliente', 'nombre', 'email', 'telefono')
    ordering = ('numero_cliente',)
    
    fieldsets = (
        ('Información del Cliente', {'fields': ('numero_cliente', 'nombre')}),
        ('Contacto', {'fields': ('email', 'telefono')}),
        )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('numero_cliente',)
        return ()

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - CONTRATO
# ==========================================================
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('numero_contrato', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado', 'fecha_inicio')
    search_fields = ('numero_contrato',)
    ordering = ('-fecha_inicio',)
    
    fieldsets = (
        ('Información del Contrato', {'fields': ('numero_contrato', 'estado')}),
        ('Periodo de Vigencia', {'fields': ('fecha_inicio', 'fecha_fin')}),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('numero_contrato',)
        return ()

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - TARIFA
# ==========================================================
class TarifaAdmin(admin.ModelAdmin):
    list_display = ('fecha_vigencia', 'precio', 'tipo_tarifa', 'tipo_cliente')
    list_filter = ('tipo_tarifa', 'tipo_cliente')
    search_fields = ('tipo_tarifa', 'tipo_cliente')
    ordering = ('-fecha_vigencia',)
    
    fieldsets = (
        ('Tipo de Tarifa', {'fields': ('tipo_tarifa', 'tipo_cliente')}),
        ('Valor y Vigencia', {'fields': ('precio', 'fecha_vigencia')}),
    )

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - MEDIDOR
# ==========================================================
class MedidorAdmin(admin.ModelAdmin):
    list_display = ('numero_medidor', 'ubicacion', 'estado_medidor', 'fecha_instalacion')
    list_filter = ('estado_medidor', 'fecha_instalacion')
    search_fields = ('numero_medidor', 'ubicacion')
    ordering = ('numero_medidor',)
    
    fieldsets = (
        ('Identificación del Medidor', {'fields': ('numero_medidor', 'ubicacion')
        }),
        ('Estado y Fecha', {'fields': ('estado_medidor', 'fecha_instalacion')
        }),
        ('Imágenes', {'fields': ('imagen_ubicacion', 'imagen_fisica')}),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('numero_medidor', 'fecha_instalacion')
        return ()

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - LECTURA
# ==========================================================
class LecturaAdmin(admin.ModelAdmin):
    list_display = ('fecha_lectura', 'consumo_energetico', 'tipo_lectura', 'lectura_actual')
    list_filter = ('tipo_lectura', 'fecha_lectura')
    search_fields = ('tipo_lectura',)
    ordering = ('-fecha_lectura',)
    
    fieldsets = (
        ('Datos de Lectura', {'fields': ('fecha_lectura', 'lectura_actual', 'tipo_lectura')}),
        ('Consumo', {'fields': ('consumo_energetico',)}),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('fecha_lectura',)
        return ()

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - BOLETA
# ==========================================================
class BoletaAdmin(admin.ModelAdmin):
    list_display = ('fecha_emision', 'fecha_vencimiento', 'monto_total', 'estado')
    list_filter = ('estado', 'fecha_emision')
    search_fields = ('estado', 'consumo_energetico')
    ordering = ('-fecha_emision',)
    
    fieldsets = (
        ('Información de la Boleta', {'fields': ('fecha_emision', 'monto_total', 'consumo_energetico')}),
        ('Estado y Vencimiento', {'fields': ('estado', 'fecha_vencimiento')}),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('fecha_emision',)
        return ()

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - PAGO
# ==========================================================
class PagoAdmin(admin.ModelAdmin):
    list_display = ('fecha_pago', 'monto_pagado', 'metodo_pago', 'numero_referencia')
    list_filter = ('metodo_pago', 'estado_pago')
    search_fields = ('numero_referencia', 'metodo_pago')
    ordering = ('-fecha_pago',)
    
    fieldsets = (
        ('Información del Pago', {'fields': ('fecha_pago', 'monto_pagado', 'metodo_pago')}),
        ('Referencia y Estado', {'fields': ('numero_referencia', 'estado_pago')}),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('fecha_pago', 'numero_referencia')
        return ()

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - USUARIO
# ==========================================================
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol', 'telefono')
    list_filter = ('rol',)
    search_fields = ('username', 'email')
    ordering = ('username',)
    
    fieldsets = (
        ('Credenciales', {'fields': ('username', 'password')
        }),
        ('Información del usuario', {'fields': ('email', 'telefono', 'rol')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('username',)
        return ()

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - NOTIFICACIONES
# ==========================================================
class NotificacionLecturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'registro_consumo')
    search_fields = ('registro_consumo',)
    ordering = ('id',)
    
    fieldsets = (
        ('Información de Notificación', {'fields': ('registro_consumo',)
        }),
    )

class NotificacionPagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'deuda_pendiente')
    search_fields = ('deuda_pendiente',)
    ordering = ('id',)
    
    fieldsets = (
        ('Información de Notificación', {'fields': ('deuda_pendiente',)}),
    )

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