from django.contrib import admin
from django.contrib.auth.models import Group
from .models import (
    Cliente, Contrato, Medidor, Lectura, Boleta, 
    Pago, Tarifa, Usuario, Notificacion
)

# Configuración del sitio admin
admin.site.site_header = "Sistema de Gestión Eléctrica - Administración"
admin.site.site_title = "Sistema Gestión Eléctrica"
admin.site.index_title = "Panel de Administración"

# ===============================
# CLIENTE ADMIN CONFIGURATION
# ===============================
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    # LISTADO - Configuración de visualización en lista
    list_display = [
        'rut', 'nombre_completo', 'email', 'telefono', 
        'direccion', 'fecha_registro', 'estado'
    ]
    
    # FILTROS
    list_filter = [
        'estado', 'fecha_registro', 'comuna'
    ]
    
    # BÚSQUEDA
    search_fields = [
        'rut', 'nombres', 'apellidos', 'email', 'direccion'
    ]
    
    # PAGINACIÓN
    list_per_page = 20
    
    # ORDENAMIENTO
    ordering = ['-fecha_registro']
    
    # CAMPOS DE SOLO LECTURA
    readonly_fields = ['fecha_registro', 'ultima_actualizacion']
    
    # CONFIGURACIÓN DE FORMULARIO - Crear/Editar
    fieldsets = (
        ('Información Personal', {
            'fields': (
                'rut', 'nombres', 'apellidos', 'email', 'telefono'
            )
        }),
        ('Dirección', {
            'fields': (
                'direccion', 'comuna', 'ciudad', 'region'
            )
        }),
        ('Estado del Cliente', {
            'fields': (
                'estado', 'fecha_registro', 'ultima_actualizacion'
            )
        }),
    )
    
    # ACCIONES PERSONALIZADAS
    actions = ['activar_clientes', 'desactivar_clientes']
    
    def nombre_completo(self, obj):
        return f"{obj.nombres} {obj.apellidos}"
    nombre_completo.short_description = 'Nombre Completo'
    
    def activar_clientes(self, request, queryset):
        updated = queryset.update(estado='ACTIVO')
        self.message_user(request, f'{updated} clientes activados exitosamente.')
    
    def desactivar_clientes(self, request, queryset):
        updated = queryset.update(estado='INACTIVO')
        self.message_user(request, f'{updated} clientes desactivados exitosamente.')

# ===============================
# CONTRATO ADMIN CONFIGURATION
# ===============================
@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = [
        'numero_contrato', 'cliente_rut', 'tipo_servicio', 
        'fecha_inicio', 'fecha_termino', 'estado_contrato'
    ]
    
    list_filter = [
        'tipo_servicio', 'estado_contrato', 'fecha_inicio'
    ]
    
    search_fields = [
        'numero_contrato', 'cliente_rut', 'tipo_servicio'
    ]
    
    readonly_fields = ['fecha_creacion']
    
    fieldsets = (
        ('Información del Contrato', {
            'fields': (
                'numero_contrato', 'cliente_rut', 'tipo_servicio'
            )
        }),
        ('Fechas del Contrato', {
            'fields': (
                'fecha_inicio', 'fecha_termino', 'fecha_creacion'
            )
        }),
        ('Estado y Tarifa', {
            'fields': (
                'estado_contrato', 'tarifa_aplicada'
            )
        }),
    )

# ===============================
# MEDIDOR ADMIN CONFIGURATION
# ===============================
@admin.register(Medidor)
class MedidorAdmin(admin.ModelAdmin):
    list_display = [
        'numero_serie', 'cliente_rut', 'tipo_medidor', 
        'fecha_instalacion', 'estado', 'ultima_calibracion'
    ]
    
    list_filter = [
        'tipo_medidor', 'estado', 'fecha_instalacion'
    ]
    
    search_fields = [
        'numero_serie', 'cliente_rut', 'direccion_instalacion'
    ]
    
    readonly_fields = ['fecha_registro']
    
    fieldsets = (
        ('Identificación', {
            'fields': (
                'numero_serie', 'cliente_rut', 'tipo_medidor'
            )
        }),
        ('Ubicación', {
            'fields': (
                'direccion_instalacion', 'coordenadas'
            )
        }),
        ('Estado y Mantención', {
            'fields': (
                'estado', 'fecha_instalacion', 'ultima_calibracion',
                'fecha_registro'
            )
        }),
    )

# ===============================
# LECTURA ADMIN CONFIGURATION
# ===============================
@admin.register(Lectura)
class LecturaAdmin(admin.ModelAdmin):
    list_display = [
        'medidor_numero_serie', 'fecha_lectura', 'lectura_actual',
        'consumo_kwh', 'lector_asignado', 'estado_lectura'
    ]
    
    list_filter = [
        'estado_lectura', 'fecha_lectura', 'lector_asignado'
    ]
    
    search_fields = [
        'medidor_numero_serie', 'lector_asignado'
    ]
    
    readonly_fields = ['fecha_registro']
    
    fieldsets = (
        ('Datos de Lectura', {
            'fields': (
                'medidor_numero_serie', 'fecha_lectura', 'lectura_actual'
            )
        }),
        ('Cálculos', {
            'fields': (
                'consumo_kwh', 'lectura_anterior'
            )
        }),
        ('Información del Lector', {
            'fields': (
                'lector_asignado', 'estado_lectura', 'observaciones'
            )
        }),
    )

# ===============================
# BOLETA ADMIN CONFIGURATION
# ===============================
@admin.register(Boleta)
class BoletaAdmin(admin.ModelAdmin):
    list_display = [
        'numero_boleta', 'cliente_rut', 'fecha_emision',
        'fecha_vencimiento', 'monto_total', 'estado_pago'
    ]
    
    list_filter = [
        'estado_pago', 'fecha_emision', 'fecha_vencimiento'
    ]
    
    search_fields = [
        'numero_boleta', 'cliente_rut'
    ]
    
    readonly_fields = ['fecha_creacion']
    
    fieldsets = (
        ('Identificación', {
            'fields': (
                'numero_boleta', 'cliente_rut', 'periodo_facturado'
            )
        }),
        ('Fechas', {
            'fields': (
                'fecha_emision', 'fecha_vencimiento', 'fecha_creacion'
            )
        }),
        ('Montos', {
            'fields': (
                'consumo_kwh', 'monto_base', 'impuestos', 'monto_total'
            )
        }),
        ('Estado', {
            'fields': (
                'estado_pago', 'observaciones'
            )
        }),
    )

# ===============================
# PAGO ADMIN CONFIGURATION
# ===============================
@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = [
        'numero_transaccion', 'cliente_rut', 'boleta_numero',
        'fecha_pago', 'monto_pagado', 'metodo_pago', 'estado_pago'
    ]
    
    list_filter = [
        'metodo_pago', 'estado_pago', 'fecha_pago'
    ]
    
    search_fields = [
        'numero_transaccion', 'cliente_rut', 'boleta_numero'
    ]
    
    readonly_fields = ['fecha_registro']
    
    fieldsets = (
        ('Información del Pago', {
            'fields': (
                'numero_transaccion', 'cliente_rut', 'boleta_numero'
            )
        }),
        ('Detalles del Pago', {
            'fields': (
                'fecha_pago', 'monto_pagado', 'metodo_pago'
            )
        }),
        ('Estado y Validación', {
            'fields': (
                'estado_pago', 'comprobante', 'fecha_registro'
            )
        }),
    )

# ===============================
# TARIFA ADMIN CONFIGURATION
# ===============================
@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display = [
        'codigo_tarifa', 'nombre_tarifa', 'tipo_tarifa',
        'precio_kwh', 'fecha_vigencia', 'estado'
    ]
    
    list_filter = [
        'tipo_tarifa', 'estado', 'fecha_vigencia'
    ]
    
    search_fields = [
        'codigo_tarifa', 'nombre_tarifa'
    ]
    
    readonly_fields = ['fecha_creacion']
    
    fieldsets = (
        ('Identificación', {
            'fields': (
                'codigo_tarifa', 'nombre_tarifa', 'tipo_tarifa'
            )
        }),
        ('Precios', {
            'fields': (
                'precio_kwh', 'cargo_fijo', 'impuestos_aplicados'
            )
        }),
        ('Vigencia', {
            'fields': (
                'fecha_vigencia', 'estado', 'fecha_creacion'
            )
        }),
    )

# ===============================
# USUARIO ADMIN CONFIGURATION
# ===============================
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'email', 'nombres', 'apellidos',
        'tipo_usuario', 'is_active', 'fecha_registro'
    ]
    
    list_filter = [
        'tipo_usuario', 'is_active', 'fecha_registro'
    ]
    
    search_fields = [
        'username', 'email', 'nombres', 'apellidos'
    ]
    
    readonly_fields = ['fecha_registro', 'ultimo_login']
    
    fieldsets = (
        ('Credenciales', {
            'fields': (
                'username', 'email', 'password'
            )
        }),
        ('Información Personal', {
            'fields': (
                'nombres', 'apellidos', 'rut', 'telefono'
            )
        }),
        ('Permisos y Roles', {
            'fields': (
                'tipo_usuario', 'is_active', 'is_staff'
            )
        }),
        ('Fechas', {
            'fields': (
                'fecha_registro', 'ultimo_login'
            )
        }),
    )

# ===============================
# NOTIFICACION ADMIN CONFIGURATION
# ===============================
@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = [
        'titulo', 'cliente_rut', 'tipo_notificacion',
        'fecha_envio', 'estado', 'leido'
    ]
    
    list_filter = [
        'tipo_notificacion', 'estado', 'leido', 'fecha_envio'
    ]
    
    search_fields = [
        'titulo', 'cliente_rut', 'mensaje'
    ]
    
    readonly_fields = ['fecha_creacion']
    
    fieldsets = (
        ('Destinatario', {
            'fields': (
                'cliente_rut', 'titulo', 'tipo_notificacion'
            )
        }),
        ('Contenido', {
            'fields': (
                'mensaje', 'prioridad'
            )
        }),
        ('Estado y Envío', {
            'fields': (
                'estado', 'leido', 'fecha_envio', 'fecha_creacion'
            )
        }),
    )

# Desregistrar Group si no es necesario
admin.site.unregister(Group)