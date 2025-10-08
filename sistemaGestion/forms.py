
from django import forms
from .models import Cliente, Usuario, Contrato, Medidor, Lectura, Boleta, Pago, Tarifa, NotificacionLectura, NotificacionPago


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['numero_cliente', 'nombre', 'email', 'telefono']
        widgets = {
            'numero_cliente': forms.TextInput(attrs={'placeholder': 'Ejemplo: CLI-001'}),
            'nombre':forms.TextInput(attrs={'placeholder': 'Ingresar nombre completo'}),
            'email':forms.TextInput(attrs={'placeholder': 'Ingresar email'}),
            'telefono':forms.TextInput(attrs={'placeholder':'Ingresar numero de telefono'})
        }

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
            'numero_contrato':forms.TextInput(attrs={'placeholder':'Ejemplo: CO-001'})
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
            'monto_total': forms.NumberInput(attrs={'placeholder':'ingresa el monto total'}),
            'consumo_energetico':forms.TextInput(attrs={'placeholder':'ingresa el consumo en kW'})
        }  

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['fecha_pago', 'monto_pagado','numero_referencia', 'metodo_pago','estado_pago']
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date'}),
            'monto_pagado':forms.NumberInput(attrs={'placeholder':'Ingresa el monto pagado'}),
            'numero_referencia':forms.TextInput(attrs={'placeholder':'Ingresa el numero de referencia'})
        }

class TarifaForm(forms.ModelForm):
    class Meta:
        model = Tarifa
        fields = ['fecha_vigencia', 'precio', 'tipo_tarifa', 'tipo_cliente']
        widgets = {
            'fecha_vigencia': forms.DateInput(attrs={'type': 'date'}),
            'Precio': forms.NumberInput(attrs={'placeholder':'Ingresa el precio de la tarifa'})
        }

class NotificacionLecturaForm(forms.ModelForm):
    class Meta:
        model = NotificacionLectura
        fields = ['registro_consumo']

class NotificacionPagoForm(forms.ModelForm):
    class Meta:
        model = NotificacionPago
        fields = ['deuda_pendiente']