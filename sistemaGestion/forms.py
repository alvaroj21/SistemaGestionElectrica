# sistemaGestion/forms.py
from django import forms
from .models import Cliente, Contrato, Tarifa, Medidor, Lectura, Boleta, Pago, Usuario, Notification

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cliente', 'nombre', 'email', 'telefono', 'numero_cliente']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and telefono < 0:
            raise forms.ValidationError("El teléfono debe ser un número positivo.")
        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and '@' not in email:
            raise forms.ValidationError("Ingrese un email válido.")
        return email


class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['identificato', 'fecha_inicio', 'fecha_fin', 'estado', 'numero_contrato', 'cliente_id_cliente']

    def clean_numero_contrato(self):
        numero = self.cleaned_data.get('numero_contrato')
        if numero <= 0:
            raise forms.ValidationError("El número de contrato debe ser positivo.")
        return numero


class TarifaForm(forms.ModelForm):
    class Meta:
        model = Tarifa
        fields = ['id_tarifa', 'tipo_tarifa', 'tipo_cliente', 'fecha_vigencia', 'precio', 'contrato_id_contrato']

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio


class MedidorForm(forms.ModelForm):
    class Meta:
        model = Medidor
        fields = ['id_medidor', 'numero_medidor', 'fecha_instalacion', 'ubicacion', 'estado_medidor', 'contrato_id_contrato']

    def clean_numero_medidor(self):
        numero = self.cleaned_data.get('numero_medidor')
        if numero <= 0:
            raise forms.ValidationError("El número de medidor debe ser positivo.")
        return numero


class LecturaForm(forms.ModelForm):
    class Meta:
        model = Lectura
        fields = ['id_lectura', 'fecha_lectura', 'consumo_energetico', 'tipo_lectura', 'lectura_actual', 
                 'medidor_id_medidor', 'medidor_contrato_id_contrato']

    def clean_lectura_actual(self):
        lectura = self.cleaned_data.get('lectura_actual')
        if not lectura:
            raise forms.ValidationError("La lectura actual es obligatoria.")
        return lectura


class BoletaForm(forms.ModelForm):
    class Meta:
        model = Boleta
        fields = ['id_boleta', 'fecha_emision', 'fecha_vencimiento', 'monto_total', 'consumo_energetico', 
                 'estado', 'lectura_id_lectura', 'lectura_medidor_id_medidor', 'lectura_medidor_contrato_id_contrato']

    def clean_monto_total(self):
        monto = self.cleaned_data.get('monto_total')
        if monto < 0:
            raise forms.ValidationError("El monto total no puede ser negativo.")
        return monto


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['id_pago', 'fecha_pago', 'monto_pagado', 'metodo_pago', 'numero_referencia', 'estado_pago',
                 'boleta_id_boleta', 'boleta_lectura_id_lectura', 'boleta_lectura_medidor_id_medidor', 
                 'boleta_lectura_medidor_contrato_id_contrato']

    def clean_numero_referencia(self):
        referencia = self.cleaned_data.get('numero_referencia')
        if referencia <= 0:
            raise forms.ValidationError("El número de referencia debe ser positivo.")
        return referencia


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nombre', 'email', 'telefono', 'rol']

    def clean_rol(self):
        rol = self.cleaned_data.get('rol')
        roles_validos = ['admin', 'usuario', 'operador']
        if rol.lower() not in roles_validos:
            raise forms.ValidationError("Rol no válido. Use: admin, usuario u operador.")
        return rol


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['id_notification', 'tipo_notification', 'estado_notification', 'fecha_generation', 
                 'fecha_revision', 'lectura_id_lectura', 'lectura_medidor_id_medidor', 
                 'lectura_medidor_contrato_id_contrato', 'pago_id_pago', 'usuario_id_usuario']