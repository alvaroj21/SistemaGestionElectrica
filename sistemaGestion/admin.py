from django.contrib import admin
from django.contrib import messages
from datetime import date
from .models import (
    Cliente, Contrato, Tarifa, Tarifa_has_Contrato, Medidor, Lectura, 
    Boleta, Pago, NotificacionLectura, NotificacionPago, Usuario
)

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - CLIENTE
# ==========================================================
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('numero_cliente', 'nombre', 'email', 'telefono')
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
    list_display = ('numero_contrato', 'cliente', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado', 'fecha_inicio', 'cliente')  # Filtrar por cliente
    search_fields = ('numero_contrato', 'cliente__nombre', 'cliente__numero_cliente')  # Buscar por datos del cliente
    ordering = ('-fecha_inicio',)
    
    fieldsets = (
        ('Información del Contrato', {'fields': ('numero_contrato', 'cliente', 'estado')}),
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
# CONFIGURACIÓN DEL ADMIN - TARIFA_HAS_CONTRATO (Relación M:N)
# ==========================================================
class TarifaHasContratoAdmin(admin.ModelAdmin):
    list_display = ('contrato', 'get_cliente', 'tarifa', 'get_precio', 'fecha_asignacion')
    list_filter = (
        'fecha_asignacion', 
        'tarifa__tipo_tarifa', 
        'tarifa__tipo_cliente',
        'contrato__estado',  # Filtrar por estado del contrato
        'contrato__cliente',  # Filtrar por cliente
    )
    search_fields = (
        'contrato__numero_contrato', 
        'contrato__cliente__nombre',  # Buscar por nombre del cliente
        'contrato__cliente__numero_cliente',  # Buscar por número de cliente
        'tarifa__tipo_tarifa',
        'tarifa__tipo_cliente',
    )
    ordering = ('-fecha_asignacion',)
    
    fieldsets = (
        ('Asignación de Tarifa', {'fields': ('contrato', 'tarifa')}),
    )
    
    readonly_fields = ('fecha_asignacion',)
    
    def get_cliente(self, obj):
        """Muestra el nombre del cliente del contrato"""
        if obj.contrato and obj.contrato.cliente:
            return obj.contrato.cliente.nombre
        return "Sin cliente"
    get_cliente.short_description = 'Cliente'
    get_cliente.admin_order_field = 'contrato__cliente__nombre'
    
    def get_precio(self, obj):
        """Muestra el precio de la tarifa"""
        return f"${obj.tarifa.precio}"
    get_precio.short_description = 'Precio'
    get_precio.admin_order_field = 'tarifa__precio'

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - MEDIDOR
# ==========================================================
class MedidorAdmin(admin.ModelAdmin):
    list_display = ('numero_medidor', 'get_cliente', 'contrato', 'ubicacion', 'estado_medidor', 'fecha_instalacion')
    list_filter = (
        'estado_medidor', 
        'fecha_instalacion',
        'contrato__cliente',  # Filtrar por cliente a través del contrato
        'contrato__estado',   # Filtrar por estado del contrato
    )
    search_fields = (
        'numero_medidor', 
        'ubicacion',
        'contrato__numero_contrato',           # Buscar por número de contrato
        'contrato__cliente__nombre',           # Buscar por nombre del cliente
        'contrato__cliente__numero_cliente',   # Buscar por número de cliente
    )
    ordering = ('numero_medidor',)
    
    fieldsets = (
        ('Identificación del Medidor', {'fields': ('numero_medidor', 'contrato', 'ubicacion')}),
        ('Estado y Fecha', {'fields': ('estado_medidor', 'fecha_instalacion')}),
        ('Imágenes', {'fields': ('imagen_ubicacion', 'imagen_fisica')}),
    )
    
    def get_cliente(self, obj):
        """Muestra el nombre del cliente en la lista"""
        if obj.contrato and obj.contrato.cliente:
            return obj.contrato.cliente.nombre
        return "Sin cliente"
    get_cliente.short_description = 'Cliente'
    get_cliente.admin_order_field = 'contrato__cliente__nombre'  # Permite ordenar por este campo
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('numero_medidor', 'fecha_instalacion')
        return ()

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - LECTURA
# ==========================================================
class LecturaAdmin(admin.ModelAdmin):
    list_display = ('fecha_lectura', 'medidor', 'get_cliente', 'consumo_energetico', 'tipo_lectura', 'lectura_actual')
    list_filter = (
        'tipo_lectura', 
        'fecha_lectura',
        'medidor',  # Filtrar por medidor específico
        'medidor__contrato__cliente',  # Filtrar por cliente a través de medidor->contrato
        'medidor__estado_medidor',     # Filtrar por estado del medidor
    )
    search_fields = (
        'medidor__numero_medidor',                        # Buscar por número de medidor
        'medidor__contrato__numero_contrato',             # Buscar por número de contrato
        'medidor__contrato__cliente__nombre',             # Buscar por nombre del cliente
        'medidor__contrato__cliente__numero_cliente',     # Buscar por número de cliente
        'tipo_lectura',
    )
    ordering = ('-fecha_lectura',)
    
    fieldsets = (
        ('Relación', {'fields': ('medidor',)}),
        ('Datos de Lectura', {'fields': ('fecha_lectura', 'lectura_actual', 'tipo_lectura')}),
        ('Consumo', {'fields': ('consumo_energetico',)}),
    )
    
    def get_cliente(self, obj):
        """Muestra el nombre del cliente en la lista"""
        try:
            if obj.medidor and obj.medidor.contrato and obj.medidor.contrato.cliente:
                return obj.medidor.contrato.cliente.nombre
        except:
            pass
        return "Sin cliente"
    get_cliente.short_description = 'Cliente'
    get_cliente.admin_order_field = 'medidor__contrato__cliente__nombre'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('fecha_lectura',)
        return ()

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - BOLETA
# ==========================================================
class BoletaAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_cliente', 'fecha_emision', 'fecha_vencimiento', 'monto_total', 'get_total_pagado', 'get_saldo_pendiente', 'estado')
    list_filter = (
        'estado', 
        'fecha_emision',
        'fecha_vencimiento',
        'lectura__medidor',  # Filtrar por medidor
        'lectura__medidor__contrato__cliente',  # Filtrar por cliente
        'lectura__tipo_lectura',  # Filtrar por tipo de lectura
    )
    search_fields = (
        'id',
        'lectura__medidor__numero_medidor',                        # Buscar por número de medidor
        'lectura__medidor__contrato__numero_contrato',             # Buscar por contrato
        'lectura__medidor__contrato__cliente__nombre',             # Buscar por nombre del cliente
        'lectura__medidor__contrato__cliente__numero_cliente',     # Buscar por número de cliente
        'estado',
        'consumo_energetico',
    )
    ordering = ('-fecha_emision',)
    
    fieldsets = (
        ('Relación', {'fields': ('lectura',)}),
        ('Información de la Boleta', {'fields': ('fecha_emision', 'monto_total', 'consumo_energetico')}),
        ('Vencimiento', {'fields': ('fecha_vencimiento',)}),
        ('Estado (Automático)', {
            'fields': ('estado', 'get_total_pagado_readonly', 'get_saldo_pendiente_readonly'),
            'description': 'El estado se actualiza automáticamente según los pagos realizados'
        }),
    )
    
    readonly_fields = ('fecha_emision', 'estado', 'get_total_pagado_readonly', 'get_saldo_pendiente_readonly')
    
    def get_cliente(self, obj):
        """Muestra el nombre del cliente en la lista"""
        try:
            if obj.lectura:
                cliente = obj.get_cliente()
                if cliente:
                    return cliente.nombre
        except:
            pass
        return "Sin cliente"
    get_cliente.short_description = 'Cliente'
    get_cliente.admin_order_field = 'lectura__medidor__contrato__cliente__nombre'
    
    def get_total_pagado(self, obj):
        """Muestra el total pagado en la lista"""
        total = obj.calcular_total_pagado()
        return f"${total:,}"
    get_total_pagado.short_description = 'Total Pagado'
    
    def get_saldo_pendiente(self, obj):
        """Muestra el saldo pendiente en la lista"""
        saldo = obj.calcular_saldo_pendiente()
        if saldo > 0:
            return f"${saldo:,}"
        else:
            return "$0"
    get_saldo_pendiente.short_description = 'Saldo Pendiente'
    
    def get_total_pagado_readonly(self, obj):
        """Muestra el total pagado en el formulario de detalle"""
        if obj.pk:
            total = obj.calcular_total_pagado()
            return f"${total:,}"
        return "$0"
    get_total_pagado_readonly.short_description = 'Total Pagado'
    
    def get_saldo_pendiente_readonly(self, obj):
        """Muestra el saldo pendiente en el formulario de detalle"""
        if obj.pk:
            saldo = obj.calcular_saldo_pendiente()
            return f"${saldo:,}"
        return "$0"
    get_saldo_pendiente_readonly.short_description = 'Saldo Pendiente'

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - PAGO
# ==========================================================
class PagoAdmin(admin.ModelAdmin):
    list_display = ('numero_referencia', 'get_cliente', 'fecha_pago', 'monto_pagado', 'get_monto_boleta', 'get_saldo_restante', 'metodo_pago', 'estado_pago')
    list_filter = (
        'metodo_pago', 
        'estado_pago',
        'fecha_pago',
        'boleta__estado',  # Filtrar por estado de la boleta
        'boleta__lectura__medidor',  # Filtrar por medidor
        'boleta__lectura__medidor__contrato__cliente',  # Filtrar por cliente
    )
    search_fields = (
        'numero_referencia', 
        'metodo_pago',
        'boleta__id',  # Buscar por ID de boleta
        'boleta__lectura__medidor__numero_medidor',                        # Buscar por medidor
        'boleta__lectura__medidor__contrato__numero_contrato',             # Buscar por contrato
        'boleta__lectura__medidor__contrato__cliente__nombre',             # Buscar por cliente
        'boleta__lectura__medidor__contrato__cliente__numero_cliente',
    )
    ordering = ('-fecha_pago',)
    
    fieldsets = (
        ('Selección de Boleta', {
            'fields': ('boleta',),
            'description': 'Seleccione la boleta a pagar'
        }),
        ('Información de la Boleta', {
            'fields': ('get_info_boleta_readonly',),
            'description': 'Información automática de la boleta seleccionada'
        }),
        ('Información del Pago', {
            'fields': ('fecha_pago', 'monto_pagado', 'metodo_pago')
        }),
        ('Referencia y Estado', {
            'fields': ('numero_referencia', 'estado_pago')
        }),
    )
    
    readonly_fields = ('fecha_pago', 'numero_referencia', 'get_info_boleta_readonly')
    
    def get_cliente(self, obj):
        """Muestra el nombre del cliente en la lista"""
        try:
            if obj.boleta:
                cliente = obj.boleta.get_cliente()
                if cliente:
                    return cliente.nombre
        except:
            pass
        return "Sin cliente"
    get_cliente.short_description = 'Cliente'
    get_cliente.admin_order_field = 'boleta__lectura__medidor__contrato__cliente__nombre'
    
    def get_monto_boleta(self, obj):
        """Muestra el monto total de la boleta"""
        try:
            if obj.boleta:
                return f"${obj.boleta.monto_total:,}"
        except:
            pass
        return "$0"
    get_monto_boleta.short_description = 'Monto Boleta'
    
    def get_saldo_restante(self, obj):
        """Muestra el saldo restante después de este pago"""
        try:
            if obj.boleta:
                saldo = obj.boleta.calcular_saldo_pendiente()
                if saldo > 0:
                    return f"${saldo:,}"
                else:
                    return "$0"
        except:
            pass
        return "$0"
    get_saldo_restante.short_description = 'Saldo Restante'
    
    def get_info_boleta_readonly(self, obj):
        """Muestra información completa de la boleta en el formulario"""
        if obj.pk and obj.boleta:
            try:
                info = f"""
            Boleta ID: {obj.boleta.id}
            Cliente: {obj.boleta.get_cliente().nombre if obj.boleta.get_cliente() else 'N/A'}
            Monto Total: ${obj.boleta.monto_total:,}
            Total Pagado: ${obj.boleta.calcular_total_pagado():,}
            Saldo Pendiente: ${obj.boleta.calcular_saldo_pendiente():,}
            Estado: {obj.boleta.estado}
            """
                return info.strip()
            except:
                return "Error al cargar información de la boleta"
        return "Seleccione una boleta para ver su información"
    get_info_boleta_readonly.short_description = 'Información de la Boleta'

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
    list_display = ('id', 'get_cliente', 'registro_consumo_corto', 'fecha_notificacion', 'revisada')
    list_filter = (
        'revisada',
        'fecha_notificacion',
        'lectura__medidor',  # Filtrar por medidor
        'lectura__medidor__contrato__cliente',  # Filtrar por cliente
        'lectura__tipo_lectura',  # Filtrar por tipo de lectura
    )
    search_fields = (
        'registro_consumo',
        'lectura__medidor__numero_medidor',
        'lectura__medidor__contrato__cliente__nombre',
        'lectura__medidor__contrato__cliente__numero_cliente',
    )
    ordering = ('-fecha_notificacion',)
    
    fieldsets = (
        ('Relación', {'fields': ('lectura',)}),
        ('Información de Notificación', {'fields': ('registro_consumo', 'revisada')}),
    )
    
    readonly_fields = ('fecha_notificacion',)
    
    def get_cliente(self, obj):
        """Muestra el nombre del cliente en la lista"""
        try:
            return obj.lectura.medidor.contrato.cliente.nombre
        except AttributeError:
            return "Sin cliente"
    get_cliente.short_description = 'Cliente'
    get_cliente.admin_order_field = 'lectura__medidor__contrato__cliente__nombre'
    
    def registro_consumo_corto(self, obj):
        """Muestra una versión corta del registro de consumo"""
        return obj.registro_consumo[:50] + "..." if len(obj.registro_consumo) > 50 else obj.registro_consumo
    registro_consumo_corto.short_description = 'Registro'

class NotificacionPagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_cliente', 'deuda_pendiente_corta', 'fecha_notificacion', 'revisada')
    list_filter = (
        'revisada',
        'fecha_notificacion',
        'pago__metodo_pago',  # Filtrar por método de pago
        'pago__estado_pago',  # Filtrar por estado del pago
        'pago__boleta__lectura__medidor__contrato__cliente',  # Filtrar por cliente
    )
    search_fields = (
        'deuda_pendiente',
        'pago__numero_referencia',
        'pago__boleta__lectura__medidor__contrato__cliente__nombre',
        'pago__boleta__lectura__medidor__contrato__cliente__numero_cliente',
    )
    ordering = ('-fecha_notificacion',)
    
    fieldsets = (
        ('Relación', {'fields': ('pago',)}),
        ('Información de Notificación', {'fields': ('deuda_pendiente', 'revisada')}),
    )
    
    readonly_fields = ('fecha_notificacion',)
    
    def get_cliente(self, obj):
        """Muestra el nombre del cliente en la lista"""
        try:
            return obj.pago.boleta.lectura.medidor.contrato.cliente.nombre
        except AttributeError:
            return "Sin cliente"
    get_cliente.short_description = 'Cliente'
    get_cliente.admin_order_field = 'pago__boleta__lectura__medidor__contrato__cliente__nombre'
    
    def deuda_pendiente_corta(self, obj):
        """Muestra una versión corta de la deuda pendiente"""
        return obj.deuda_pendiente[:50] + "..." if len(obj.deuda_pendiente) > 50 else obj.deuda_pendiente
    deuda_pendiente_corta.short_description = 'Deuda'

# ==========================================================
# REGISTRO DE MODELOS EN EL ADMIN
# ==========================================================
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Tarifa, TarifaAdmin)
admin.site.register(Tarifa_has_Contrato, TarifaHasContratoAdmin)
admin.site.register(Medidor, MedidorAdmin)
admin.site.register(Lectura, LecturaAdmin)
admin.site.register(Boleta, BoletaAdmin)
admin.site.register(Pago, PagoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(NotificacionLectura, NotificacionLecturaAdmin)
admin.site.register(NotificacionPago, NotificacionPagoAdmin)