from django import forms
from django.utils import timezone
from django.core.validators import RegexValidator
from .models import Cliente, Contrato, Tarifa, Medidor, Lectura, Boleta, Pago, Usuario, Notification


# ==========================================================
# FORMULARIO CLIENTE
# ==========================================================
class ClienteForm(forms.ModelForm):
    telefono = forms.CharField(
        validators=[RegexValidator(r'^\+?\d{8,15}$', 'Ingrese un número de teléfono válido (8 a 15 dígitos).')],
        required=False
    )

    class Meta:
        model = Cliente
        fields = ['cliente', 'nombre', 'email', 'telefono', 'numero_cliente']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not forms.EmailField().clean(email):
            raise forms.ValidationError("Ingrese un email válido.")
        if Cliente.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un cliente con este email.")
        return email

    def clean_numero_cliente(self):
        numero = self.cleaned_data.get('numero_cliente')
        if Cliente.objects.filter(numero_cliente=numero).exists():
            raise forms.ValidationError("Ya existe un cliente con este número de cliente.")
        return numero


# ==========================================================
# FORMULARIO CONTRATO
# ==========================================================
class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['identificato', 'fecha_inicio', 'fecha_fin', 'estado', 'numero_contrato', 'cliente_id_cliente']

    def clean_numero_contrato(self):
        numero = self.cleaned_data.get('numero_contrato')
        if numero <= 0:
            raise forms.ValidationError("El número de contrato debe ser positivo.")
        if Contrato.objects.filter(numero_contrato=numero).exists():
            raise forms.ValidationError("Ya existe un contrato con este número.")
        return numero

    def clean_fecha_fin(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_fin = self.cleaned_data.get('fecha_fin')
        if fecha_inicio and fecha_fin and fecha_fin <= fecha_inicio:
            raise forms.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")
        return fecha_fin

    def clean_cliente_id_cliente(self):
        cliente = self.cleaned_data.get('cliente_id_cliente')
        if not Cliente.objects.filter(pk=cliente.pk).exists():
            raise forms.ValidationError("El cliente asociado no existe.")
        return cliente


# ==========================================================
# FORMULARIO TARIFA
# ==========================================================
class TarifaForm(forms.ModelForm):
    class Meta:
        model = Tarifa
        fields = ['id_tarifa', 'tipo_tarifa', 'tipo_cliente', 'fecha_vigencia', 'precio', 'contrato_id_contrato']

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio

    def clean_fecha_vigencia(self):
        fecha_vigencia = self.cleaned_data.get('fecha_vigencia')
        if fecha_vigencia and fecha_vigencia < timezone.now().date():
            raise forms.ValidationError("La fecha de vigencia no puede ser en el pasado.")
        return fecha_vigencia

    def clean_tipo_tarifa(self):
        tipo_tarifa = self.cleaned_data.get('tipo_tarifa')
        tipos_validos = ['residencial', 'comercial', 'industrial']
        if tipo_tarifa and tipo_tarifa.lower() not in tipos_validos:
            raise forms.ValidationError("Tipo de tarifa no válido. Use: residencial, comercial o industrial.")
        return tipo_tarifa

    def clean_tipo_cliente(self):
        tipo_cliente = self.cleaned_data.get('tipo_cliente')
        tipos_validos = ['nuevo', 'regular', 'preferencial']
        if tipo_cliente and tipo_cliente.lower() not in tipos_validos:
            raise forms.ValidationError("Tipo de cliente no válido. Use: nuevo, regular o preferencial.")
        return tipo_cliente


# ==========================================================
# FORMULARIO MEDIDOR
# ==========================================================
class MedidorForm(forms.ModelForm):
    class Meta:
        model = Medidor
        fields = ['id_medidor', 'numero_medidor', 'fecha_instalacion', 'ubicacion',
                  'estado_medidor', 'contrato_id_contrato']

    def clean_numero_medidor(self):
        numero = self.cleaned_data.get('numero_medidor')
        if numero <= 0:
            raise forms.ValidationError("El número de medidor debe ser positivo.")
        if Medidor.objects.filter(numero_medidor=numero).exists():
            raise forms.ValidationError("Ya existe un medidor con ese número.")
        return numero

    def clean_fecha_instalacion(self):
        fecha_instalacion = self.cleaned_data.get('fecha_instalacion')
        if fecha_instalacion and fecha_instalacion > timezone.now().date():
            raise forms.ValidationError("La fecha de instalación no puede ser en el futuro.")
        return fecha_instalacion

    def clean_estado_medidor(self):
        estado = self.cleaned_data.get('estado_medidor')
        estados_validos = ['activo', 'inactivo', 'mantenimiento', 'desinstalado']
        if estado and estado.lower() not in estados_validos:
            raise forms.ValidationError("Estado no válido. Use: activo, inactivo, mantenimiento o desinstalado.")
        return estado


# ==========================================================
# FORMULARIO LECTURA
# ==========================================================
class LecturaForm(forms.ModelForm):
    class Meta:
        model = Lectura
        fields = ['id_lectura', 'fecha_lectura', 'consumo_energetico', 'tipo_lectura', 'lectura_actual',
                  'medidor_id_medidor', 'medidor_contrato_id_contrato']

    def clean_lectura_actual(self):
        lectura = self.cleaned_data.get('lectura_actual')
        if lectura is None or lectura < 0:
            raise forms.ValidationError("La lectura actual debe ser un número positivo.")
        return lectura

    def clean_consumo_energetico(self):
        consumo = self.cleaned_data.get('consumo_energetico')
        if consumo and consumo < 0:
            raise forms.ValidationError("El consumo energético no puede ser negativo.")
        return consumo

    def clean_fecha_lectura(self):
        fecha_lectura = self.cleaned_data.get('fecha_lectura')
        if fecha_lectura and fecha_lectura > timezone.now().date():
            raise forms.ValidationError("La fecha de lectura no puede ser en el futuro.")
        return fecha_lectura

    def clean_tipo_lectura(self):
        tipo_lectura = self.cleaned_data.get('tipo_lectura')
        tipos_validos = ['real', 'estimada', 'automatica']
        if tipo_lectura and tipo_lectura.lower() not in tipos_validos:
            raise forms.ValidationError("Tipo de lectura no válido. Use: real, estimada o automatica.")
        return tipo_lectura


# ==========================================================
# FORMULARIO BOLETA
# ==========================================================
class BoletaForm(forms.ModelForm):
    class Meta:
        model = Boleta
        fields = ['id_boleta', 'fecha_emision', 'fecha_vencimiento', 'monto_total', 'consumo_energetico',
                  'estado', 'lectura_id_lectura', 'lectura_medidor_id_medidor',
                  'lectura_medidor_contrato_id_contrato']

    def clean_monto_total(self):
        monto = self.cleaned_data.get('monto_total')
        if monto < 0:
            raise forms.ValidationError("El monto total no puede ser negativo.")
        return monto

    def clean_fecha_vencimiento(self):
        fecha_emision = self.cleaned_data.get('fecha_emision')
        fecha_vencimiento = self.cleaned_data.get('fecha_vencimiento')
        if fecha_emision and fecha_vencimiento and fecha_vencimiento <= fecha_emision:
            raise forms.ValidationError("La fecha de vencimiento debe ser posterior a la fecha de emisión.")
        return fecha_vencimiento

    def clean_estado(self):
        estado = self.cleaned_data.get('estado')
        estados_validos = ['pendiente', 'pagada', 'vencida', 'cancelada']
        if estado and estado.lower() not in estados_validos:
            raise forms.ValidationError("Estado no válido. Use: pendiente, pagada, vencida o cancelada.")
        return estado


# ==========================================================
# FORMULARIO PAGO
# ==========================================================
class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['id_pago', 'fecha_pago', 'monto_pagado', 'metodo_pago', 'numero_referencia',
                  'estado_pago', 'boleta_id_boleta', 'boleta_lectura_id_lectura',
                  'boleta_lectura_medidor_id_medidor', 'boleta_lectura_medidor_contrato_id_contrato']

    def clean_numero_referencia(self):
        referencia = self.cleaned_data.get('numero_referencia')
        if referencia <= 0:
            raise forms.ValidationError("El número de referencia debe ser positivo.")
        if Pago.objects.filter(numero_referencia=referencia).exists():
            raise forms.ValidationError("Ya existe un pago con este número de referencia.")
        return referencia

    def clean_monto_pagado(self):
        monto = self.cleaned_data.get('monto_pagado')
        if monto <= 0:
            raise forms.ValidationError("El monto pagado debe ser mayor a cero.")
        return monto

    def clean_fecha_pago(self):
        fecha_pago = self.cleaned_data.get('fecha_pago')
        if fecha_pago and fecha_pago > timezone.now().date():
            raise forms.ValidationError("La fecha de pago no puede ser en el futuro.")
        return fecha_pago

    def clean_metodo_pago(self):
        metodo = self.cleaned_data.get('metodo_pago')
        metodos_validos = ['efectivo', 'tarjeta', 'transferencia', 'cheque']
        if metodo and metodo.lower() not in metodos_validos:
            raise forms.ValidationError("Método de pago no válido. Use: efectivo, tarjeta, transferencia o cheque.")
        return metodo

    def clean_estado_pago(self):
        estado = self.cleaned_data.get('estado_pago')
        estados_validos = ['pendiente', 'completado', 'fallido', 'reembolsado']
        if estado and estado.lower() not in estados_validos:
            raise forms.ValidationError("Estado de pago no válido. Use: pendiente, completado, fallido o reembolsado.")
        return estado


# ==========================================================
# FORMULARIO USUARIO
# ==========================================================
class UsuarioForm(forms.ModelForm):
    telefono = forms.CharField(
        validators=[RegexValidator(r'^\+?\d{8,15}$', 'Ingrese un número de teléfono válido (8 a 15 dígitos).')],
        required=False
    )

    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nombre', 'email', 'telefono', 'rol']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo.")
        return email

    def clean_rol(self):
        rol = self.cleaned_data.get('rol')
        roles_validos = ['admin', 'usuario', 'operador']
        if rol.lower() not in roles_validos:
            raise forms.ValidationError("Rol no válido. Use: admin, usuario u operador.")
        return rol


# ==========================================================
# FORMULARIO NOTIFICACIONES
# ==========================================================
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['id_notification', 'tipo_notification', 'estado_notification', 'fecha_generation',
                  'fecha_revision', 'lectura_id_lectura', 'lectura_medidor_id_medidor',
                  'lectura_medidor_contrato_id_contrato', 'pago_id_pago', 'usuario_id_usuario']

    def clean_fecha_revision(self):
        fecha_generation = self.cleaned_data.get('fecha_generation')
        fecha_revision = self.cleaned_data.get('fecha_revision')
        if fecha_generation and fecha_revision and fecha_revision < fecha_generation:
            raise forms.ValidationError("La fecha de revisión no puede ser anterior a la fecha de generación.")
        return fecha_revision

    def clean_tipo_notification(self):
        tipo = self.cleaned_data.get('tipo_notification')
        tipos_validos = ['lectura', 'pago', 'vencimiento', 'corte', 'reconexion', 'general']
        if tipo and tipo.lower() not in tipos_validos:
            raise forms.ValidationError("Tipo de notificación no válido. Use: lectura, pago, vencimiento, corte, reconexion o general.")
        return tipo

    def clean_estado_notification(self):
        estado = self.cleaned_data.get('estado_notification')
        estados_validos = ['pendiente', 'leida', 'enviada', 'fallida']
        if estado and estado.lower() not in estados_validos:
            raise forms.ValidationError("Estado de notificación no válido. Use: pendiente, leida, enviada o fallida.")
        return estado
