
from django import forms
from .models import Cliente, Usuario, Contrato, Medidor, Lectura, Boleta, Pago, Tarifa, NotificacionLectura, NotificacionPago


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['numero_cliente', 'nombre', 'email', 'telefono']

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'email', 'telefono', 'rol']

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['numero_contrato', 'fecha_inicio', 'fecha_fin', 'estado']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

class MedidorForm(forms.ModelForm):
    class Meta:
        model = Medidor
        fields = ['numero_medidor', 'fecha_instalacion', 'ubicacion', 'estado_medidor', 'imagen_ubicacion']
        widgets = {
            'fecha_instalacion': forms.DateInput(attrs={'type': 'date'}),
            'imagen_ubicacion': forms.URLInput(attrs={'placeholder': 'https://ejemplo.com/imagen.jpg'})
        } 

class LecturaForm(forms.ModelForm):
    class Meta:
        model = Lectura
        fields = ['fecha_lectura', 'consumo_energetico', 'tipo_lectura', 'lectura_actual']
        widgets = {
            'fecha_lectura': forms.DateInput(attrs={'type': 'date'}),
        }  

class BoletaForm(forms.ModelForm):
    class Meta:
        model = Boleta
        fields = ['fecha_emision', 'fecha_vencimiento', 'monto_total', 'consumo_energetico', 'estado']
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }  

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['fecha_pago', 'monto_pagado', 'metodo_pago', 'numero_referencia', 'estado_pago']
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date'}),
        }

class TarifaForm(forms.ModelForm):
    class Meta:
        model = Tarifa
        fields = ['fecha_vigencia', 'precio', 'tipo_tarifa', 'tipo_cliente']
        widgets = {
            'fecha_vigencia': forms.DateInput(attrs={'type': 'date'}),
        }

class NotificacionLecturaForm(forms.ModelForm):
    class Meta:
        model = NotificacionLectura
        fields = ['registro_consumo']

class NotificacionPagoForm(forms.ModelForm):
    class Meta:
        model = NotificacionPago
        fields = ['deuda_pendiente']