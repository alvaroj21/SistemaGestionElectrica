from django import forms
from django.utils import timezone
from django.core.validators import RegexValidator
from .models import Cliente, Contrato, Tarifa, Medidor, Lectura, Boleta, Pago, Usuario, NotificacionPago, NotificacionLectura


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
        fields = ['numero_cliente', 'nombre', 'email', 'telefono']

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
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Contrato
        fields = ['fecha_inicio', 'fecha_fin', 'estado', 'numero_contrato']

    def clean_numero_contrato(self):
        numero = self.cleaned_data.get('numero_contrato')
        if Contrato.objects.filter(numero_contrato=numero).exists():
            raise forms.ValidationError("Ya existe un contrato con este número.")
        return numero

    def clean_fecha_fin(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_fin = self.cleaned_data.get('fecha_fin')
        if fecha_inicio and fecha_fin and fecha_fin <= fecha_inicio:
            raise forms.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")
        return fecha_fin


# ==========================================================
# FORMULARIO TARIFA
# ==========================================================
class TarifaForm(forms.ModelForm):
    fecha_vigencia = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Tarifa
        fields = ['fecha_vigencia', 'precio', 'tipo_tarifa', 'tipo_cliente']

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


# ==========================================================
# FORMULARIO MEDIDOR
# ==========================================================
class MedidorForm(forms.ModelForm):
    fecha_instalacion = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Medidor
        fields = ['numero_medidor', 'fecha_instalacion', 'ubicacion', 'estado_medidor', 'imagen_ubicacion']

    def clean_numero_medidor(self):
        numero = self.cleaned_data.get('numero_medidor')
        if Medidor.objects.filter(numero_medidor=numero).exists():
            raise forms.ValidationError("Ya existe un medidor con ese número.")
        return numero

    def clean_fecha_instalacion(self):
        fecha_instalacion = self.cleaned_data.get('fecha_instalacion')
        if fecha_instalacion and fecha_instalacion > timezone.now().date():
            raise forms.ValidationError("La fecha de instalación no puede ser en el futuro.")
        return fecha_instalacion


# ==========================================================
# FORMULARIO LECTURA
# ==========================================================
class LecturaForm(forms.ModelForm):
    fecha_lectura = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Lectura
        fields = ['fecha_lectura', 'consumo_energetico', 'tipo_lectura', 'lectura_actual']

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


# ==========================================================
# FORMULARIO BOLETA
# ==========================================================
class BoletaForm(forms.ModelForm):
    fecha_emision = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    fecha_vencimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Boleta
        fields = ['fecha_emision', 'fecha_vencimiento', 'monto_total', 'consumo_energetico', 'estado']

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


# ==========================================================
# FORMULARIO PAGO
# ==========================================================
class PagoForm(forms.ModelForm):
    fecha_pago = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Pago
        fields = ['fecha_pago', 'monto_pagado', 'metodo_pago', 'numero_referencia', 'estado_pago']

    def clean_numero_referencia(self):
        referencia = self.cleaned_data.get('numero_referencia')
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
        fields = ['username', 'password', 'email', 'telefono', 'rol']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Excluir el objeto actual al editar
        usuarios_existentes = Usuario.objects.filter(email=email)
        if self.instance.pk:
            usuarios_existentes = usuarios_existentes.exclude(pk=self.instance.pk)
        if usuarios_existentes.exists():
            raise forms.ValidationError("Ya existe un usuario con este correo.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Excluir el objeto actual al editar
        usuarios_existentes = Usuario.objects.filter(username=username)
        if self.instance.pk:
            usuarios_existentes = usuarios_existentes.exclude(pk=self.instance.pk)
        if usuarios_existentes.exists():
            raise forms.ValidationError("Ya existe un usuario con este nombre de usuario.")
        return username


# ==========================================================
# FORMULARIO NOTIFICACION PAGO
# ==========================================================
class NotificacionPagoForm(forms.ModelForm):
    class Meta:
        model = NotificacionPago
        fields = ['deuda_pendiente']

    def clean_deuda_pendiente(self):
        deuda = self.cleaned_data.get('deuda_pendiente')
        if not deuda or deuda.strip() == '':
            raise forms.ValidationError("La información de deuda pendiente es requerida.")
        return deuda


# ==========================================================
# FORMULARIO NOTIFICACION LECTURA
# ==========================================================
class NotificacionLecturaForm(forms.ModelForm):
    class Meta:
        model = NotificacionLectura
        fields = ['registro_consumo']

    def clean_registro_consumo(self):
        registro = self.cleaned_data.get('registro_consumo')
        if not registro or registro.strip() == '':
            raise forms.ValidationError("El registro de consumo es requerido.")
        return registro
