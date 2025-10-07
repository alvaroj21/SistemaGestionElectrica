# sistemaGestion/models.py
from django.db import models

class Cliente(models.Model):
    cliente = models.IntegerField(primary_key=True, db_column='cliente')
    nombre = models.CharField(max_length=45, db_column='nombre')
    email = models.CharField(max_length=45, db_column='email', blank=True, null=True)
    telefono = models.IntegerField(db_column='telefono', blank=True, null=True)
    numero_cliente = models.CharField(max_length=45, db_column='numero_cliente', unique=True)

    class Meta:
        db_table = "Cliente"
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.nombre} ({self.numero_cliente})"


class Contrato(models.Model):
    identificato = models.IntegerField(primary_key=True, db_column='Identificato')
    fecha_inicio = models.CharField(max_length=45, db_column='fecha_inicio')
    fecha_fin = models.CharField(max_length=45, db_column='fecha_fin', blank=True, null=True)
    estado = models.CharField(max_length=45, db_column='estado')
    numero_contrato = models.IntegerField(db_column='numero_contrato')
    cliente_id_cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        db_column='Cliente_idCliente',
        related_name='contratos'
    )

    class Meta:
        db_table = "Contrato"
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"

    def __str__(self):
        return f"Contrato {self.numero_contrato} - {self.estado}"


class Tarifa(models.Model):
    id_tarifa = models.IntegerField(primary_key=True, db_column='idTarifa')
    tipo_tarifa = models.CharField(max_length=45, db_column='tipo_tarifa')
    tipo_cliente = models.CharField(max_length=45, db_column='tipo_cliente', blank=True, null=True)
    fecha_vigencia = models.CharField(max_length=45, db_column='fecha_vigencia')
    precio = models.IntegerField(db_column='precio')
    contrato_id_contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,
        db_column='Contrato_idContrato',
        related_name='tarifas'
    )

    class Meta:
        db_table = "Tarifa"
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"

    def __str__(self):
        return f"Tarifa {self.tipo_tarifa} - ${self.precio}"


class Medidor(models.Model):
    id_medidor = models.IntegerField(primary_key=True, db_column='idMedidor')
    numero_medidor = models.IntegerField(db_column='numero_medidor')
    fecha_instalacion = models.CharField(max_length=45, db_column='fecha_instalacion', blank=True, null=True)
    ubicacion = models.CharField(max_length=45, db_column='ubicacion', blank=True, null=True)
    estado_medidor = models.CharField(max_length=45, db_column='estado_medidor', blank=True, null=True)
    contrato_id_contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,
        db_column='Contrato_idContrato',
        related_name='medidores'
    )

    class Meta:
        db_table = "Medidor"
        verbose_name = "Medidor"
        verbose_name_plural = "Medidores"

    def __str__(self):
        return f"Medidor {self.numero_medidor} - {self.ubicacion or 'Sin ubicación'}"


class Lectura(models.Model):
    id_lectura = models.IntegerField(primary_key=True, db_column='idLectura')
    fecha_lectura = models.CharField(max_length=45, db_column='fecha_lectura')
    consumo_energetico = models.CharField(max_length=45, db_column='consumo_energetico', blank=True, null=True)
    tipo_lectura = models.CharField(max_length=45, db_column='tipo_lectura', blank=True, null=True)
    lectura_actual = models.CharField(max_length=45, db_column='lectura_actual')
    medidor_id_medidor = models.ForeignKey(
        Medidor,
        on_delete=models.CASCADE,
        db_column='Medidor_idMedidor',
        related_name='lecturas'
    )
    medidor_contrato_id_contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,
        db_column='Medidor_Contrato_idContrato',
        related_name='lecturas'
    )

    class Meta:
        db_table = "Lectura"
        verbose_name = "Lectura"
        verbose_name_plural = "Lecturas"

    def __str__(self):
        return f"Lectura {self.id_lectura} - {self.fecha_lectura}"


class Boleta(models.Model):
    id_boleta = models.IntegerField(primary_key=True, db_column='idBoleta')
    fecha_emision = models.CharField(max_length=45, db_column='fecha_emision')
    fecha_vencimiento = models.CharField(max_length=45, db_column='fecha_vencimiento')
    monto_total = models.IntegerField(db_column='monto_total')
    consumo_energetico = models.CharField(max_length=45, db_column='consumo_energetico', blank=True, null=True)
    estado = models.CharField(max_length=45, db_column='estado')
    lectura_id_lectura = models.ForeignKey(
        Lectura,
        on_delete=models.CASCADE,
        db_column='Lectura_idLectura',
        related_name='boletas'
    )
    lectura_medidor_id_medidor = models.ForeignKey(
        Medidor,
        on_delete=models.CASCADE,
        db_column='Lectura_Medidor_idMedidor',
        related_name='boletas'
    )
    lectura_medidor_contrato_id_contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,
        db_column='Lectura_Medidor_Contrato_idContrato',
        related_name='boletas'
    )

    class Meta:
        db_table = "Boleta"
        verbose_name = "Boleta"
        verbose_name_plural = "Boletas"

    def __str__(self):
        return f"Boleta {self.id_boleta} - ${self.monto_total}"


class Pago(models.Model):
    id_pago = models.IntegerField(primary_key=True, db_column='idPago')
    fecha_pago = models.CharField(max_length=45, db_column='fecha_pago')
    monto_pagado = models.CharField(max_length=45, db_column='monto_pagado')
    metodo_pago = models.CharField(max_length=45, db_column='metodo_pago')
    numero_referencia = models.IntegerField(db_column='numero_referencia')
    estado_pago = models.CharField(max_length=45, db_column='estado_pago')
    boleta_id_boleta = models.ForeignKey(
        Boleta,
        on_delete=models.CASCADE,
        db_column='Boleta_idBoleta',
        related_name='pagos'
    )
    boleta_lectura_id_lectura = models.ForeignKey(
        Lectura,
        on_delete=models.CASCADE,
        db_column='Boleta_Lectura_idLectura',
        related_name='pagos'
    )
    boleta_lectura_medidor_id_medidor = models.ForeignKey(
        Medidor,
        on_delete=models.CASCADE,
        db_column='Boleta_Lectura_Medidor_idMedidor',
        related_name='pagos'
    )
    boleta_lectura_medidor_contrato_id_contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,
        db_column='Boleta_Lectura_Medidor_Contrato_idContrato',
        related_name='pagos'
    )

    class Meta:
        db_table = "Pago"
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"

    def __str__(self):
        return f"Pago {self.id_pago} - Ref: {self.numero_referencia}"


class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True, db_column='idUsuario')
    nombre = models.CharField(max_length=45, db_column='nombre')
    email = models.CharField(max_length=45, db_column='email', blank=True, null=True)
    telefono = models.CharField(max_length=45, db_column='telefono', blank=True, null=True)
    rol = models.CharField(max_length=45, db_column='rol')

    class Meta:
        db_table = "Usuario"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.nombre} - {self.rol}"


class Notification(models.Model):
    id_notification = models.IntegerField(primary_key=True, db_column='IdNotification')
    tipo_notification = models.CharField(max_length=45, db_column='tipo_notification')
    estado_notification = models.CharField(max_length=45, db_column='estado_notification')
    fecha_generation = models.CharField(max_length=45, db_column='fecha_generation')
    fecha_revision = models.CharField(max_length=45, db_column='fecha_revision', blank=True, null=True)
    lectura_id_lectura = models.ForeignKey(
        Lectura,
        on_delete=models.CASCADE,
        db_column='Lectura_idLectura',
        related_name='notifications',
        blank=True,
        null=True
    )
    lectura_medidor_id_medidor = models.ForeignKey(
        Medidor,
        on_delete=models.CASCADE,
        db_column='Lectura_Medidor_idMedidor',
        related_name='notifications',
        blank=True,
        null=True
    )
    lectura_medidor_contrato_id_contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,
        db_column='Lectura_Medidor_Contrato_idContrato',
        related_name='notifications',
        blank=True,
        null=True
    )
    pago_id_pago = models.ForeignKey(
        Pago,
        on_delete=models.CASCADE,
        db_column='Pago_idPago',
        related_name='notifications',
        blank=True,
        null=True
    )
    usuario_id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column='Usuario_idUsuario',
        related_name='notifications'
    )

    class Meta:
        db_table = "Notification"
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"Notificación {self.id_notification} - {self.tipo_notification}"