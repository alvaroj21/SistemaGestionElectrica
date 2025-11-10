"""
MODELOS DEL SISTEMA DE GESTIÓN ELÉCTRICA
=========================================

Este archivo contiene todos los modelos de la base de datos del sistema.

JERARQUÍA DE RELACIONES:
- Cliente (base) → Contrato → Medidor → Lectura → Boleta → Pago
- Tarifa ←→ Contrato (relación muchos a muchos)
- Lectura → NotificacionLectura
- Pago → NotificacionPago
- Usuario (modelo independiente para autenticación)

CARACTERÍSTICAS PRINCIPALES:
- CharField unique: Asegura que ciertos campos no se repitan en la BD
- max_length: Limita la longitud de los campos de texto
- null=True y blank=True: Permite que campos sean opcionales
- choices: Define opciones predefinidas para ciertos campos
- __str__: Representa el objeto como cadena de texto (útil para admin y formularios)
- related_name: Permite acceso inverso entre modelos relacionados
- on_delete=CASCADE: Si se elimina el padre, se eliminan los hijos

MÉTODOS PERSONALIZADOS:
- get_cliente(): Obtiene el cliente a través de la cadena de relaciones
- get_info_completa(): Retorna diccionario con toda la información relacionada
- calcular_total_pagado(): Calcula automáticamente el total pagado (Boleta)
- actualizar_estado(): Actualiza el estado según los pagos (Boleta)
"""

from django.db import models
from django.db.models import Sum


# ============================================
# MODELO CLIENTE
# ============================================
# Es el modelo base de la jerarquía. No tiene relaciones de entrada.
# Un cliente puede tener múltiples contratos (relación 1:N).
# 
# CAMPOS:
# - numero_cliente: Identificador único del cliente
# - nombre: Nombre completo del cliente
# - email: Correo electrónico único
# - telefono: Número de contacto
#
# RELACIONES:
# - contratos (1:N): Acceso a todos los contratos del cliente
#
class Cliente(models.Model):
    numero_cliente = models.CharField(max_length=45, unique=True)
    nombre = models.CharField(max_length=45)
    email = models.CharField(max_length=45, unique=True)
    telefono = models.CharField(max_length=15)
    
    def __str__(self):
        """Representación en texto del cliente"""
        return f"{self.numero_cliente} - {self.nombre}"
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre']  # Ordenar alfabéticamente por nombre

# ============================================
# MODELO CONTRATO
# ============================================
# Representa un contrato entre un cliente y la empresa eléctrica.
# Cada contrato pertenece a UN cliente (relación N:1 con Cliente).
# Un contrato puede tener múltiples medidores (relación 1:N).
#
# CAMPOS:
# - cliente: FK → Cliente (obligatorio)
# - fecha_inicio: Fecha de inicio del contrato
# - fecha_fin: Fecha de finalización del contrato
# - estado: Activo o Inactivo (choices)
# - numero_contrato: Identificador único del contrato
#
# RELACIONES:
# - cliente (N:1): El cliente dueño del contrato
# - medidores (1:N): Todos los medidores asociados al contrato
# - tarifa_contratos (N:M): Tarifas aplicadas al contrato (relación intermedia)
#
# COMPORTAMIENTO ON_DELETE:
# - CASCADE: Si se elimina el cliente, se eliminan todos sus contratos
#
class Contrato(models.Model):
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo','Inactivo')
    ]
    
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE,  # Si se elimina el cliente, se eliminan sus contratos
        related_name='contratos',  # Acceder desde cliente: cliente.contratos.all()
        verbose_name='Cliente',
        null=True,  # Temporal para migración
        blank=True
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo')
    numero_contrato = models.CharField(max_length=45, unique=True)

    def __str__(self):
        """Representación en texto del contrato"""
        return f"Contrato {self.numero_contrato} - Cliente: {self.cliente.nombre} ({self.estado})"
    
    def get_cliente_info(self):
        """
        Retorna un diccionario con la información completa del cliente asociado.
        Útil para mostrar datos del cliente sin múltiples consultas a la BD.
        """
        return {
            'nombre': self.cliente.nombre,
            'email': self.cliente.email,
            'telefono': self.cliente.telefono,
            'numero_cliente': self.cliente.numero_cliente
        }
    
    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
        ordering = ['-fecha_inicio']  # Más recientes primero


# ============================================
# MODELO TARIFA
# ============================================
# Define las tarifas eléctricas según temporada y tipo de cliente.
# No tiene relaciones de entrada (modelo independiente).
# Se relaciona con Contrato mediante una tabla intermedia (M:N).
#
# CAMPOS:
# - fecha_vigencia: Fecha desde la cual es válida esta tarifa
# - precio: Precio por kWh en pesos (entero positivo)
# - tipo_tarifa: Verano o Invierno (choices)
# - tipo_cliente: Residencial, Comercial o Industrial (choices)
#
# RELACIONES:
# - contrato_tarifas (M:N): Contratos que usan esta tarifa (a través de tabla intermedia)
#
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
    precio = models.PositiveIntegerField()  # Precio por kWh
    tipo_tarifa = models.CharField(max_length=45, choices=TARIFA_CHOICES, default='Verano')
    tipo_cliente = models.CharField(max_length=45, choices=CLIENTE_CHOICES, default='Residencial')

    def __str__(self):
        """Representación en texto de la tarifa con información clave"""
        return f"Tarifa {self.tipo_tarifa} - {self.tipo_cliente} (${self.precio}/kWh)"
    
    class Meta:
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"
        ordering = ['-fecha_vigencia']  # Más recientes primero

# ============================================
# MODELO INTERMEDIO: TARIFA_HAS_CONTRATO
# ============================================
# Tabla intermedia que conecta Tarifa con Contrato (relación M:N).
# Permite que un contrato tenga varias tarifas a lo largo del tiempo,
# y que una tarifa sea aplicada a múltiples contratos.
#
# CAMPOS:
# - tarifa: FK → Tarifa
# - contrato: FK → Contrato
# - fecha_asignacion: Se asigna automáticamente al crear la relación
#
# CARACTERÍSTICAS ESPECIALES:
# - unique_together: Evita que se asigne la misma tarifa al mismo contrato dos veces
# - auto_now_add=True: La fecha se crea automáticamente al guardar
#
# USO TÍPICO:
# - Asignar tarifa a contrato: Tarifa_has_Contrato.objects.create(tarifa=t, contrato=c)
# - Obtener tarifas de contrato: contrato.tarifa_contratos.all()
# - Obtener contratos de tarifa: tarifa.contrato_tarifas.all()
#
class Tarifa_has_Contrato(models.Model):
    tarifa = models.ForeignKey(
        Tarifa,
        on_delete=models.CASCADE,  # Si se elimina tarifa, se elimina la relación
        related_name='contrato_tarifas',
        verbose_name='Tarifa'
    )
    contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,  # Si se elimina contrato, se elimina la relación
        related_name='tarifa_contratos',
        verbose_name='Contrato'
    )
    fecha_asignacion = models.DateField(auto_now_add=True)
    
    def __str__(self):
        """Representación en texto de la relación"""
        return f"Tarifa {self.tarifa.tipo_tarifa} aplicada a Contrato {self.contrato.numero_contrato}"
    
    def get_info_completa(self):
        """
        Retorna un diccionario con toda la información de la relación.
        Útil para reportes y vistas que necesiten datos completos.
        """
        return {
            'tarifa': {
                'tipo': self.tarifa.tipo_tarifa,
                'precio': self.tarifa.precio,
                'tipo_cliente': self.tarifa.tipo_cliente
            },
            'contrato': {
                'numero': self.contrato.numero_contrato,
                'cliente': self.contrato.cliente.nombre
            },
            'fecha_asignacion': self.fecha_asignacion
        }
    
    class Meta:
        verbose_name = "Tarifa por Contrato"
        verbose_name_plural = "Tarifas por Contrato"
        unique_together = ['tarifa', 'contrato']  # Evita duplicados

# ============================================
# MODELO MEDIDOR
# ============================================
# Representa un medidor eléctrico instalado en una ubicación física.
# Cada medidor pertenece a UN contrato (relación N:1 con Contrato).
# Un medidor puede tener múltiples lecturas (relación 1:N).
#
# CAMPOS:
# - contrato: FK → Contrato (obligatorio)
# - numero_medidor: Identificador único del medidor
# - fecha_instalacion: Fecha en que se instaló el medidor
# - ubicacion: Dirección física donde está instalado
# - estado_medidor: Activo, Inactivo, Mantenimiento o Dañado (choices)
# - imagen_ubicacion: URL de imagen del mapa de ubicación (opcional)
# - imagen_fisica: URL de foto física del medidor (opcional)
#
# RELACIONES:
# - contrato (N:1): El contrato al que pertenece el medidor
# - lecturas (1:N): Todas las lecturas tomadas de este medidor
#
# MÉTODOS ÚTILES:
# - get_cliente(): Obtiene el cliente a través de contrato
# - get_info_completa(): Retorna toda la información incluyendo cliente y contrato
#
class Medidor(models.Model):
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
        ('Mantenimiento', 'Mantenimiento'),
        ('Dañado', 'Dañado'),
    ]
    
    contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,  # Si se elimina contrato, se eliminan sus medidores
        related_name='medidores',  # Acceder desde contrato: contrato.medidores.all()
        verbose_name='Contrato',
        null=True,  # Temporal para migración
        blank=True
    )
    numero_medidor = models.CharField(max_length=45, unique=True)
    fecha_instalacion = models.DateField()
    ubicacion = models.CharField(max_length=45)
    estado_medidor = models.CharField(max_length=45, choices=ESTADO_CHOICES, default='Activo')
    imagen_ubicacion = models.URLField(max_length=200, blank=True, null=True)  # Mapa de ubicación
    imagen_fisica = models.URLField(max_length=200, blank=True, null=True)     # Foto del medidor

    def __str__(self):
        """Representación en texto del medidor con ubicación y cliente"""
        return f"Medidor {self.numero_medidor} - Cliente: {self.contrato.cliente.nombre} - {self.ubicacion}"
    
    def get_cliente(self):
        """
        Retorna el cliente asociado navegando la cadena de relaciones.
        Medidor → Contrato → Cliente
        """
        return self.contrato.cliente
    
    def get_info_completa(self):
        """
        Retorna un diccionario con toda la información del medidor.
        Incluye datos del medidor, contrato y cliente en una sola estructura.
        Útil para vistas detalladas y reportes.
        """
        return {
            'numero_medidor': self.numero_medidor,
            'ubicacion': self.ubicacion,
            'estado': self.estado_medidor,
            'contrato': {
                'numero': self.contrato.numero_contrato,
                'estado': self.contrato.estado
            },
            'cliente': {
                'nombre': self.contrato.cliente.nombre,
                'numero_cliente': self.contrato.cliente.numero_cliente,
                'email': self.contrato.cliente.email,
                'telefono': self.contrato.cliente.telefono
            }
        }
    
    class Meta:
        verbose_name = "Medidor"
        verbose_name_plural = "Medidores"
        ordering = ['-fecha_instalacion']  # Más recientes primero

# ============================================
# MODELO LECTURA
# ============================================
# Representa una lectura del medidor eléctrico en una fecha específica.
# Cada lectura pertenece a UN medidor (relación N:1 con Medidor).
# Cada lectura puede tener UNA boleta asociada (relación 1:1).
#
# CAMPOS:
# - medidor: FK → Medidor (obligatorio)
# - fecha_lectura: Fecha en que se tomó la lectura
# - consumo_energetico: Consumo en kWh durante el período
# - tipo_lectura: Digital o Analógica (choices)
# - lectura_actual: Valor actual del medidor en kWh
#
# RELACIONES:
# - medidor (N:1): El medidor del cual se tomó la lectura
# - boleta (1:1): La boleta generada para esta lectura
# - notificaciones (1:N): Notificaciones asociadas a esta lectura
#
# CADENA DE RELACIONES:
# Lectura → Medidor → Contrato → Cliente
#
class Lectura(models.Model):
    TIPO_LECTURA_CHOICES = [
        ('Digital', 'Digital'),
        ('Analogica', 'Analógica'),
    ]
    
    medidor = models.ForeignKey(
        Medidor,
        on_delete=models.CASCADE,  # Si se elimina medidor, se eliminan sus lecturas
        related_name='lecturas',  # Acceder desde medidor: medidor.lecturas.all()
        verbose_name='Medidor',
        null=True,  # Temporal para migración
        blank=True
    )
    fecha_lectura = models.DateField()
    consumo_energetico = models.PositiveIntegerField()  # kWh consumidos
    tipo_lectura = models.CharField(max_length=45, choices=TIPO_LECTURA_CHOICES, default='Digital')
    lectura_actual = models.PositiveIntegerField()  # Valor actual del contador

    def __str__(self):
        """Representación en texto de la lectura con información clave"""
        return f"Lectura {self.fecha_lectura} - Medidor {self.medidor.numero_medidor} - {self.consumo_energetico} kWh"
    
    def get_cliente(self):
        """
        Retorna el cliente asociado navegando la cadena completa.
        Lectura → Medidor → Contrato → Cliente
        """
        return self.medidor.contrato.cliente
    
    def get_info_completa(self):
        """
        Retorna un diccionario con toda la información de la lectura.
        Incluye datos de lectura, medidor, contrato y cliente.
        Útil para vistas detalladas, reportes y APIs.
        """
        return {
            'fecha_lectura': self.fecha_lectura,
            'consumo': self.consumo_energetico,
            'lectura_actual': self.lectura_actual,
            'tipo': self.tipo_lectura,
            'medidor': {
                'numero': self.medidor.numero_medidor,
                'ubicacion': self.medidor.ubicacion
            },
            'contrato': {
                'numero': self.medidor.contrato.numero_contrato
            },
            'cliente': {
                'nombre': self.medidor.contrato.cliente.nombre,
                'numero_cliente': self.medidor.contrato.cliente.numero_cliente
            }
        }
    
    class Meta:
        verbose_name = "Lectura"
        verbose_name_plural = "Lecturas"
        ordering = ['-fecha_lectura']  # Más recientes primero


# ============================================
# MODELO BOLETA
# ============================================
# Representa una boleta de cobro por consumo eléctrico.
# Cada boleta pertenece a UNA lectura (relación 1:1 con Lectura).
# Una boleta puede tener múltiples pagos (relación 1:N).
#
# CAMPOS:
# - lectura: OneToOneField → Lectura (obligatorio, único)
# - fecha_emision: Fecha en que se emitió la boleta
# - fecha_vencimiento: Fecha límite de pago
# - monto_total: Monto total a pagar
# - consumo_energetico: Consumo que se está cobrando
# - estado: Pagado, Pagado Parcialmente o Pendiente (editable manualmente)
#
# RELACIONES:
# - lectura (1:1): La lectura que originó esta boleta
# - pagos (1:N): Todos los pagos realizados para esta boleta
#
# CADENA DE RELACIONES:
# Boleta → Lectura → Medidor → Contrato → Cliente
#
class Boleta(models.Model):
    BOLETA_CHOICES = [
        ('Pagado','Pagado'),
        ('Pagado Parcialmente','Pagado Parcialmente'),
        ('Pendiente','Pendiente')
    ]
    
    lectura = models.OneToOneField(
        Lectura,
        on_delete=models.CASCADE,  # Si se elimina lectura, se elimina su boleta
        related_name='boleta',  # Acceder desde lectura: lectura.boleta
        verbose_name='Lectura',
        null=True,  # Temporal para migración
        blank=True
    )
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    monto_total = models.PositiveIntegerField()
    consumo_energetico = models.CharField(max_length=45)
    estado = models.CharField(
        max_length=45, 
        choices=BOLETA_CHOICES, 
        default='Pendiente'
    )

    def __str__(self):
        """Representación en texto de la boleta con cliente y estado"""
        try:
            cliente_nombre = self.lectura.get_cliente().nombre if self.lectura and self.lectura.get_cliente() else "Sin cliente"
            return f"Boleta {self.id} - Cliente: {cliente_nombre} - ${self.monto_total} ({self.estado})"
        except:
            return f"Boleta {self.id} - ${self.monto_total} ({self.estado})"
    
    def get_cliente(self):
        """
        Retorna el cliente asociado navegando la cadena completa.
        Boleta → Lectura → Medidor → Contrato → Cliente
        
        Returns:
            Cliente: El cliente asociado, o None si hay error en la cadena
        """
        try:
            if self.lectura and self.lectura.medidor and self.lectura.medidor.contrato:
                return self.lectura.medidor.contrato.cliente
        except:
            pass
        return None
    
    def get_info_completa(self):
        """
        Retorna un diccionario completo con toda la información de la boleta.
        Incluye datos de boleta, lectura, medidor y cliente.
        """
        return {
            'id_boleta': self.id,
            'fecha_emision': self.fecha_emision,
            'fecha_vencimiento': self.fecha_vencimiento,
            'monto_total': self.monto_total,
            'estado': self.estado,
            'lectura': {
                'fecha': self.lectura.fecha_lectura,
                'consumo': self.lectura.consumo_energetico
            },
            'medidor': {
                'numero': self.lectura.medidor.numero_medidor,
                'ubicacion': self.lectura.medidor.ubicacion
            },
            'cliente': {
                'nombre': self.get_cliente().nombre,
                'numero_cliente': self.get_cliente().numero_cliente,
                'email': self.get_cliente().email
            }
        }
    
    def calcular_total_pagado(self):
        """
        Calcula la suma total de todos los pagos realizados para esta boleta.
        
        Returns:
            int: Total pagado en pesos, 0 si no hay pagos
        """
        total = self.pagos.aggregate(Sum('monto_pagado'))['monto_pagado__sum']
        return total if total is not None else 0
    
    def calcular_saldo_pendiente(self):
        """
        Calcula el saldo pendiente de pago (monto total - total pagado).
        
        Returns:
            int: Saldo pendiente en pesos
        """
        return self.monto_total - self.calcular_total_pagado()
    
    class Meta:
        verbose_name = "Boleta"
        verbose_name_plural = "Boletas"
        ordering = ['-fecha_emision']  # Más recientes primero


# ============================================
# MODELO PAGO
# ============================================
# Representa un pago realizado para una boleta.
# Cada pago pertenece a UNA boleta (relación N:1 con Boleta).
#
# CAMPOS:
# - boleta: FK → Boleta (obligatorio)
# - fecha_pago: Fecha en que se realizó el pago
# - monto_pagado: Cantidad pagada en pesos
# - metodo_pago: Efectivo, Transferencia, Tarjeta, Débito (choices)
# - numero_referencia: Número de comprobante/referencia del pago
# - estado_pago: Pagado o No pagado completamente (choices)
#
# RELACIONES:
# - boleta (N:1): La boleta a la que corresponde este pago
# - notificaciones (1:N): Notificaciones asociadas a este pago
#
# CADENA DE RELACIONES:
# Pago → Boleta → Lectura → Medidor → Contrato → Cliente
#
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
    
    boleta = models.ForeignKey(
        Boleta,
        on_delete=models.CASCADE,  # Si se elimina boleta, se eliminan sus pagos
        related_name='pagos',  # Acceder desde boleta: boleta.pagos.all()
        verbose_name='Boleta',
        null=True,  # Temporal para migración
        blank=True
    )
    fecha_pago = models.DateField()
    monto_pagado = models.PositiveIntegerField()
    metodo_pago = models.CharField(max_length=45, choices=METODOPAGO_CHOICES)
    numero_referencia = models.CharField(max_length=45)
    estado_pago = models.CharField(max_length=45, choices=PAGO_CHOICES, default='Pagado')

    def __str__(self):
        """Representación en texto del pago con información clave"""
        try:
            if self.boleta:
                return f"Pago {self.numero_referencia} - Boleta {self.boleta.id} - ${self.monto_pagado} ({self.metodo_pago})"
            else:
                return f"Pago {self.numero_referencia} - ${self.monto_pagado} ({self.metodo_pago})"
        except:
            return f"Pago {self.numero_referencia} - ${self.monto_pagado}"
    
    def get_cliente(self):
        """
        Retorna el cliente asociado navegando toda la cadena de relaciones.
        Pago → Boleta → Lectura → Medidor → Contrato → Cliente
        
        Returns:
            Cliente: El cliente asociado, o None si hay error en la cadena
        """
        try:
            if self.boleta and self.boleta.lectura and self.boleta.lectura.medidor and self.boleta.lectura.medidor.contrato:
                return self.boleta.lectura.medidor.contrato.cliente
        except:
            pass
        return None
    
    def get_info_completa(self):
        """
        Retorna un diccionario completo con toda la información del pago.
        Incluye validación robusta para cada nivel de la cadena de relaciones.
        Si algo falla, retorna 'N/A' en lugar de generar error.
        
        Returns:
            dict: Diccionario con información completa del pago
        """
        info = {
            'numero_referencia': self.numero_referencia,
            'fecha_pago': self.fecha_pago,
            'monto_pagado': self.monto_pagado,
            'metodo_pago': self.metodo_pago,
            'estado': self.estado_pago,
        }
        
        # Información de la boleta (con validación)
        if self.boleta:
            try:
                info['boleta'] = {
                    'id': self.boleta.id,
                    'monto_total': self.boleta.monto_total,
                    'total_pagado': self.boleta.calcular_total_pagado(),
                    'saldo_pendiente': self.boleta.calcular_saldo_pendiente(),
                    'estado': self.boleta.estado
                }
                info['monto_boleta'] = self.boleta.monto_total
                info['estado_boleta'] = self.boleta.estado
            except:
                info['monto_boleta'] = 'N/A'
                info['estado_boleta'] = 'N/A'
        else:
            info['monto_boleta'] = 'N/A'
            info['estado_boleta'] = 'N/A'
        
        # Información del cliente (con validación completa de la cadena)
        try:
            cliente = self.get_cliente()
            if cliente:
                info['cliente'] = {
                    'nombre': cliente.nombre,
                    'numero_cliente': cliente.numero_cliente,
                    'email': cliente.email
                }
                
                # Información del contrato
                if self.boleta and self.boleta.lectura and self.boleta.lectura.medidor and self.boleta.lectura.medidor.contrato:
                    contrato = self.boleta.lectura.medidor.contrato
                    info['numero_contrato'] = contrato.numero_contrato
                else:
                    info['numero_contrato'] = 'N/A'
                
                # Información del medidor
                if self.boleta and self.boleta.lectura and self.boleta.lectura.medidor:
                    medidor = self.boleta.lectura.medidor
                    info['numero_medidor'] = medidor.numero_medidor
                    info['ubicacion_medidor'] = medidor.ubicacion
                else:
                    info['numero_medidor'] = 'N/A'
                    info['ubicacion_medidor'] = 'N/A'
                
                # Información de la lectura
                if self.boleta and self.boleta.lectura:
                    lectura = self.boleta.lectura
                    info['fecha_lectura'] = lectura.fecha_lectura
                    info['consumo_lectura'] = lectura.consumo_energetico
                else:
                    info['fecha_lectura'] = 'N/A'
                    info['consumo_lectura'] = 'N/A'
            else:
                # Si no se puede obtener el cliente, rellenar con N/A
                info['cliente'] = 'N/A'
                info['numero_contrato'] = 'N/A'
                info['numero_medidor'] = 'N/A'
                info['ubicacion_medidor'] = 'N/A'
                info['fecha_lectura'] = 'N/A'
                info['consumo_lectura'] = 'N/A'
        except Exception as e:
            # Si hay cualquier error, rellenar con N/A
            info['cliente'] = 'N/A'
            info['numero_contrato'] = 'N/A'
            info['numero_medidor'] = 'N/A'
            info['ubicacion_medidor'] = 'N/A'
            info['fecha_lectura'] = 'N/A'
            info['consumo_lectura'] = 'N/A'
        
        return info
    
    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-fecha_pago']  # Más recientes primero


# ============================================
# MODELO NOTIFICACION LECTURA
# ============================================
# Representa una notificación relacionada con una lectura de medidor.
# Cada notificación pertenece a UNA lectura (relación N:1 con Lectura).
# Se usa para alertar sobre consumos anormales, lecturas especiales, etc.
#
# CAMPOS:
# - lectura: FK → Lectura (obligatorio)
# - registro_consumo: Texto descriptivo de la notificación (máx 500 caracteres)
# - fecha_notificacion: Se asigna automáticamente al crear
# - revisada: Boolean para marcar si fue leída (default: False)
#
# RELACIONES:
# - lectura (N:1): La lectura que generó esta notificación
#
# USO TÍPICO:
# - Personal eléctrico revisa notificaciones de consumo anormal
# - Se marca como revisada después de tomar acción
# - Los emojis en __str__ ayudan a identificar estado visual mente
#
# PERMISOS:
# - Solo usuarios con rol 'Administrador' o 'Eléctrico' pueden ver/editar
#
class NotificacionLectura(models.Model):
    lectura = models.ForeignKey(
        Lectura,
        on_delete=models.CASCADE,  # Si se elimina lectura, se eliminan sus notificaciones
        related_name='notificaciones',  # Acceder desde lectura: lectura.notificaciones.all()
        verbose_name='Lectura',
        null=True,  # Temporal para migración
        blank=True
    )
    registro_consumo = models.CharField(max_length=500)
    fecha_notificacion = models.DateTimeField(auto_now_add=True)  # Se asigna automáticamente
    revisada = models.BooleanField(default=False)  # Para marcar como leído

    def __str__(self):
        """Representación en texto con emoji indicando si fue revisada"""
        estado = "✅" if self.revisada else "🔔"
        return f"{estado} Notificación Lectura - Cliente: {self.lectura.get_cliente().nombre} - {self.registro_consumo[:30]}..."
    
    def get_info_completa(self):
        """
        Retorna información completa de la notificación con datos del cliente.
        Útil para mostrar detalles sin múltiples consultas a la BD.
        """
        return {
            'registro_consumo': self.registro_consumo,
            'fecha_notificacion': self.fecha_notificacion,
            'lectura': {
                'fecha': self.lectura.fecha_lectura,
                'consumo': self.lectura.consumo_energetico
            },
            'cliente': {
                'nombre': self.lectura.get_cliente().nombre,
                'email': self.lectura.get_cliente().email,
                'telefono': self.lectura.get_cliente().telefono
            }
        }
    
    class Meta:
        verbose_name = "Notificación de Lectura"
        verbose_name_plural = "Notificaciones de Lectura"
        ordering = ['-fecha_notificacion']  # Más recientes primero


# ============================================
# MODELO NOTIFICACION PAGO
# ============================================
# Representa una notificación relacionada con un pago.
# Cada notificación pertenece a UN pago (relación N:1 con Pago).
# Se usa para alertar sobre deudas pendientes, pagos recibidos, etc.
#
# CAMPOS:
# - pago: FK → Pago (obligatorio)
# - deuda_pendiente: Texto descriptivo de la notificación (máx 500 caracteres)
# - fecha_notificacion: Se asigna automáticamente al crear
# - revisada: Boolean para marcar si fue leída (default: False)
#
# RELACIONES:
# - pago (N:1): El pago que generó esta notificación
#
# USO TÍPICO:
# - Personal de finanzas revisa notificaciones de pagos/deudas
# - Se marca como revisada después de tomar acción
# - Los emojis en __str__ ayudan a identificar estado visualmente
#
# PERMISOS:
# - Solo usuarios con rol 'Administrador' o 'Finanzas' pueden ver/editar
#
class NotificacionPago(models.Model):
    pago = models.ForeignKey(
        Pago,
        on_delete=models.CASCADE,  # Si se elimina pago, se eliminan sus notificaciones
        related_name='notificaciones',  # Acceder desde pago: pago.notificaciones.all()
        verbose_name='Pago',
        null=True,  # Temporal para migración
        blank=True
    )
    deuda_pendiente = models.CharField(max_length=500)
    fecha_notificacion = models.DateTimeField(auto_now_add=True)  # Se asigna automáticamente
    revisada = models.BooleanField(default=False)  # Para marcar como leído

    def __str__(self):
        """Representación en texto con emoji indicando si fue revisada"""
        estado = "✅" if self.revisada else "🔔"
        return f"{estado} Notificación Pago - Cliente: {self.pago.get_cliente().nombre} - {self.deuda_pendiente[:30]}..."
    
    def get_info_completa(self):
        """
        Retorna información completa de la notificación con datos del cliente.
        Útil para mostrar detalles sin múltiples consultas a la BD.
        """
        return {
            'deuda_pendiente': self.deuda_pendiente,
            'fecha_notificacion': self.fecha_notificacion,
            'pago': {
                'numero_referencia': self.pago.numero_referencia,
                'monto_pagado': self.pago.monto_pagado,
                'fecha_pago': self.pago.fecha_pago
            },
            'cliente': {
                'nombre': self.pago.get_cliente().nombre,
                'email': self.pago.get_cliente().email,
                'telefono': self.pago.get_cliente().telefono
            }
        }
    
    class Meta:
        verbose_name = "Notificación de Pago"
        verbose_name_plural = "Notificaciones de Pago"
        ordering = ['-fecha_notificacion']  # Más recientes primero


# ============================================
# MODELO USUARIO
# ============================================
# Modelo independiente para el sistema de autenticación.
# No tiene relaciones con otros modelos del sistema eléctrico.
# Controla el acceso y permisos según el rol asignado.
#
# CAMPOS:
# - username: Nombre de usuario único para login
# - password: Contraseña (debe hashearse antes de guardar)
# - email: Correo electrónico del usuario
# - telefono: Número de contacto
# - rol: Administrador, Eléctrico o Finanzas (choices)
#
# ROLES Y PERMISOS (definidos en views.py PERMISOS_ROL):
# 
# Administrador:
#   - Acceso total a todos los módulos
#   - Puede gestionar: medidores, lecturas, clientes, contratos, 
#     tarifas, boletas, pagos, usuarios, notificaciones
#
# Eléctrico:
#   - Acceso limitado a funciones técnicas
#   - Puede gestionar: medidores, lecturas, notificaciones
#   - NO puede ver/editar: clientes, contratos, tarifas, boletas, pagos, usuarios
#
# Finanzas:
#   - Acceso limitado a funciones financieras
#   - Puede gestionar: clientes, contratos, tarifas, boletas, pagos, notificaciones
#   - NO puede ver/editar: medidores, lecturas, usuarios
#
# SEGURIDAD:
# - El password debe hashearse antes de guardar (implementado en views.py)
# - username es único (no puede haber duplicados)
# - El sistema verifica permisos antes de cada acción
#
# USO EN VIEWS:
# - request.session['username']: Obtiene el username del usuario logueado
# - request.session['rol']: Obtiene el rol para verificar permisos
# - tiene_permiso(request, 'modulo'): Verifica si el usuario puede acceder
#
class Usuario(models.Model):
    ROLES_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Eléctrico', 'Eléctrico'),
        ('Finanzas', 'Finanzas'),
    ]
    
    username = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=128)  # Debe hashearse antes de guardar
    email = models.CharField(max_length=45)
    telefono = models.CharField(max_length=15)
    rol = models.CharField(max_length=45, choices=ROLES_CHOICES)

    def __str__(self):
        """Representación en texto del usuario con su rol"""
        return f"{self.username} - {self.rol}"
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['username']  # Orden alfabético por username
