from django import forms
from datetime import date, timedelta
import re
from .models import Cliente, Contrato, Tarifa, Medidor, Lectura, Boleta, Pago, Usuario, NotificacionPago, NotificacionLectura
#se importan los modelos necesarios para los formularios y el timedelta y date para validaciones de fechas
#timedelta permite hacer operaciones con fechas como sumar o restar días
#time permite obtener la fecha actual para validaciones
#los fields permiten definir qué campos del modelo se van a utilizar en el formulario
#los widgets permiten personalizar los campos del formulario con atributos HTML como clases CSS o placeholders o tipos de input
#los labels permiten definir etiquetas personalizadas para los campos del formulario
# y los def clean_<campo> permiten definir validaciones personalizadas para cada campo
# ==========================================================
# FORMULARIO CLIENTE
# ==========================================================
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['numero_cliente', 'nombre', 'email', 'telefono'] 
        widgets = {
            'numero_cliente': forms.TextInput(attrs={'placeholder': 'Ejemplo: CLI-001','class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingresa el nombre completo del cliente','class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com','class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'placeholder': '+56 9 1234 5678','class': 'form-control'})
        }
        labels = {
            'numero_cliente': 'Número de Cliente',
            'nombre': 'Nombre Completo',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono'
        }
    #def clean_email se encarga de validar que el email tenga un formato correcto y que no exista otro cliente con el mismo email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not forms.EmailField().clean(email):
            raise forms.ValidationError("Ingresa un email válido.")
        
        clientes = Cliente.objects.filter(email=email)
        if self.instance.id:
            clientes = clientes.exclude(id=self.instance.id)
        
        if clientes.exists():
            raise forms.ValidationError("Ya existe un cliente con este email.")
        return email
    #def clean_numero_cliente se encarga de validar que el número de cliente tenga un formato correcto y que no exista otro cliente con el mismo número
    def clean_numero_cliente(self):
        numero_cliente = self.cleaned_data.get('numero_cliente')

        if not numero_cliente.startswith('CLI-'):
            raise forms.ValidationError("El número de cliente debe comenzar con 'CLI-'")

        clientes = Cliente.objects.filter(numero_cliente=numero_cliente)
        if self.instance.id:
            clientes = clientes.exclude(id=self.instance.id)
        
        if clientes.exists():
            raise forms.ValidationError("Ya existe un cliente con este número de cliente.")
        return numero_cliente
    #def clean_telefono se encarga de validar que el teléfono tenga al menos 8 dígitos
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        # Permite solo números y el símbolo +, sin letras
        #r significa raw string, para que no interprete caracteres especiales
        #^ significa inicio de cadena
        #+? significa que se permite el símbolo + una o ninguna vez
        #\d+ significa que se permiten uno o más dígitos
        #y $ significa fin de cadena
        patron = re.compile(r'^\+?\d+$')
        if telefono and not patron.match(telefono):
            raise forms.ValidationError("El teléfono solo puede contener números y el símbolo '+', sin espacios ni letras.")
        return telefono
    #def clean_nombre se encarga de validar que el nombre no contenga números y lo formatea a título
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if any(char.isdigit() for char in nombre):
            raise forms.ValidationError("El nombre no puede contener números")
        
        return nombre.title()
    
    
# ==========================================================
# FORMULARIO CONTRATO
# ==========================================================
class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['fecha_inicio', 'fecha_fin', 'estado', 'numero_contrato']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'numero_contrato': forms.TextInput(attrs={'placeholder': 'Ejemplo: CON-001', 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Finalización',
            'estado': 'Estado del Contrato',
            'numero_contrato': 'Número de Contrato'
        }
    #def clean_numero_contrato se encarga de validar que el número de contrato tenga un formato correcto y que no exista otro contrato con el mismo número
    def clean_numero_contrato(self):
        numero = self.cleaned_data.get('numero_contrato')
        
        if not numero.startswith('CON-'):
            raise forms.ValidationError("El número de contrato debe comenzar con 'CON-'")

        contratos = Contrato.objects.filter(numero_contrato=numero)
        if self.instance.id:
            contratos = contratos.exclude(id=self.instance.id)
        
        if contratos.exists():
            raise forms.ValidationError("Ya existe un contrato con este número.")
        return numero
    #def clean_fecha_fin se encarga de validar que la fecha de fin sea posterior a la fecha de inicio y que el contrato tenga al menos 30 días de duración
    def clean_fecha_fin(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_fin = self.cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            if fecha_fin <= fecha_inicio:
                raise forms.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")
            
            # Validar que el contrato tenga al menos 30 días de duración
            diferencia = fecha_fin - fecha_inicio
            if diferencia.days < 30:
                raise forms.ValidationError("El contrato debe tener una duración mínima de 30 días.")
        
        return fecha_fin
    #def clean_fecha_inicio se encarga de validar que la fecha de inicio no sea anterior a la fecha actual y que no sea más de 1 año en el futuro
    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        
        if fecha_inicio < date.today():
            raise forms.ValidationError("La fecha de inicio no puede ser una fecha anterior a la de hoy")
        
        # Validar que no sea más de 1 año en el futuro
        un_año_futuro = date.today() + timedelta(days=365)
        if fecha_inicio > un_año_futuro:
            raise forms.ValidationError("La fecha de inicio no puede ser más de 1 año en el futuro")
        
        return fecha_inicio
    #def clean se encarga de validar que si el estado es Activo, la fecha de fin sea futura
    #se utiliza clean en lugar de clean_<campo> porque depende de dos campos
    #en este caso, estado y fecha_fin
    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get('estado')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        # Si el estado es Activo, la fecha de fin debe ser futura
        if estado == 'Activo' and fecha_fin and fecha_fin <= date.today():
            raise forms.ValidationError("Un contrato activo no puede tener fecha de fin pasada")
        
        return cleaned_data

# ==========================================================
# FORMULARIO TARIFA
# ==========================================================
class TarifaForm(forms.ModelForm):

    class Meta:
        model = Tarifa
        fields = ['fecha_vigencia', 'precio', 'tipo_tarifa', 'tipo_cliente']
        widgets = {
            'fecha_vigencia': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'placeholder': 'Ejemplo: 150', 'class': 'form-control', 'min': '1'}),
            'tipo_tarifa': forms.Select(attrs={'class': 'form-control'}),
            'tipo_cliente': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'fecha_vigencia': 'Fecha de Vigencia',
            'precio': 'Precio por kWh',
            'tipo_tarifa': 'Tipo de Tarifa',
            'tipo_cliente': 'Tipo de Cliente'
        }
    #def clean_precio se encarga de validar que el precio sea mayor a 0
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a 0")
        return precio
    #def clean_fecha_vigencia se encarga de validar que la fecha de vigencia no sea anterior a la fecha actual
    def clean_fecha_vigencia(self):
        fecha = self.cleaned_data.get('fecha_vigencia')
        
        if fecha < date.today():
            raise forms.ValidationError("La fecha de vigencia no puede ser anterior a la fecha de hoy")
        
        return fecha

# ==========================================================
# FORMULARIO MEDIDOR
# ==========================================================
class MedidorForm(forms.ModelForm):
    class Meta:
        model = Medidor
        fields = ['numero_medidor', 'fecha_instalacion', 'ubicacion', 'estado_medidor', 'imagen_ubicacion', 'imagen_fisica']
        widgets = {
            'numero_medidor': forms.TextInput(attrs={'placeholder': 'Ejemplo: MED-001','class': 'form-control'}),
            'fecha_instalacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'placeholder': 'Dirección o ubicación del medidor','class': 'form-control'}),
            'estado_medidor': forms.Select(attrs={'class': 'form-control'}),
            'imagen_ubicacion': forms.URLInput(attrs={'placeholder': 'https://ejemplo.com/mapa-ubicacion.jpg','class': 'form-control'}),
            'imagen_fisica': forms.URLInput(attrs={'placeholder': 'https://ejemplo.com/foto-medidor.jpg','class': 'form-control'})
        }
        labels = {
            'numero_medidor': 'Número de Medidor',
            'fecha_instalacion': 'Fecha de Instalación',
            'ubicacion': 'Ubicación',
            'estado_medidor': 'Estado del Medidor',
            'imagen_ubicacion': 'URL Imagen Mapa/Ubicación (opcional)',
            'imagen_fisica': 'URL Imagen Física del Medidor (opcional)'
        }
    #def clean_numero_medidor se encarga de validar que el número de medidor tenga un formato correcto y que no exista otro medidor con el mismo número
    def clean_numero_medidor(self):
        numero = self.cleaned_data.get('numero_medidor')
        
        if not numero.startswith('MED-'):
            raise forms.ValidationError("El número de medidor debe comenzar con 'MED-'")
        
        medidores = Medidor.objects.filter(numero_medidor=numero)
        if self.instance.id:
            medidores = medidores.exclude(id=self.instance.id)
        
        if medidores.exists():
            raise forms.ValidationError("Ya existe un medidor con ese número.")
        return numero
    #def clean_fecha_instalacion se encarga de validar que la fecha de instalación no sea posterior a 365 días desde hoy y no sea tan antigua (más de 10 años)
    def clean_fecha_instalacion(self):
        fecha_instalacion = self.cleaned_data.get('fecha_instalacion')
    
        fecha_limite = date.today() + timedelta(days=365)
        if fecha_instalacion > fecha_limite:
            raise forms.ValidationError("La fecha de instalación no puede ser posterior a 365 días desde hoy")

        diez_años_atras = date.today() - timedelta(days=365*10)
        if fecha_instalacion < diez_años_atras:
            raise forms.ValidationError("La fecha de instalación no puede ser tan antigua")
        
        return fecha_instalacion
    #def clean_ubicacion se encarga de validar que la ubicación tenga al menos 4 caracteres y la formatea a título
    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get('ubicacion')
        
        if len(ubicacion) < 4:
            raise forms.ValidationError("La ubicación debe tener al menos 4 caracteres")

        return ubicacion.title()


# ==========================================================
# FORMULARIO LECTURA
# ==========================================================
class LecturaForm(forms.ModelForm):
    class Meta:
        model = Lectura
        fields = ['fecha_lectura', 'consumo_energetico', 'tipo_lectura', 'lectura_actual']
        widgets = {
            'fecha_lectura': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'consumo_energetico': forms.NumberInput(attrs={'placeholder': 'Consumo en kWh','class': 'form-control','min': '0'}),
            'tipo_lectura': forms.Select(attrs={'class': 'form-control'}),
            'lectura_actual': forms.NumberInput(attrs={'placeholder': 'Lectura actual del medidor','class': 'form-control','min': '0'})
        }
        labels = {
            'fecha_lectura': 'Fecha de Lectura',
            'consumo_energetico': 'Consumo Energético (kWh)',
            'tipo_lectura': 'Tipo de Lectura',
            'lectura_actual': 'Lectura Actual'
        }
    #def clean_lectura_actual se encarga de validar que la lectura actual sea un número positivo
    def clean_lectura_actual(self):
        lectura = self.cleaned_data.get('lectura_actual')
        
        if lectura is None or lectura < 0:
            raise forms.ValidationError("La lectura actual debe ser un número positivo.")

        if lectura is None or lectura == 0:
            raise forms.ValidationError("La lectura actual no puede ser cero.")

        if lectura > 9999999:
            raise forms.ValidationError("La lectura actual parece muy alta")
        return lectura
    #def clean_consumo_energetico se encarga de validar que el consumo energético sea un número positivo y no muy alto
    def clean_consumo_energetico(self):
        consumo = self.cleaned_data.get('consumo_energetico')
        
        if consumo and consumo < 0:
            raise forms.ValidationError("El consumo energético no puede ser negativo.")
        if consumo and consumo > 999999:
            raise forms.ValidationError("El consumo energético parece muy alto")
        
        return consumo
    #def clean_fecha_lectura se encarga de validar que la fecha de lectura no sea posterior a hoy y no sea tan antigua (más de 1 año)
    def clean_fecha_lectura(self):
        fecha_lectura = self.cleaned_data.get('fecha_lectura')
        
        if fecha_lectura and fecha_lectura > date.today():
            raise forms.ValidationError("La fecha de lectura no puede ser posterior a hoy.")

        fecha_limite = date.today() - timedelta(days=365)
        if fecha_lectura < fecha_limite:
            raise forms.ValidationError("La fecha de lectura no puede ser tan antigua")
        
        return fecha_lectura


# ==========================================================
# FORMULARIO BOLETA
# ==========================================================
class BoletaForm(forms.ModelForm):  
    class Meta:
        model = Boleta
        fields = ['fecha_emision', 'fecha_vencimiento', 'monto_total', 'consumo_energetico', 'estado']
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'monto_total': forms.NumberInput(attrs={'placeholder': 'Monto total a pagar','class': 'form-control','min': '1'}),
            'consumo_energetico': forms.TextInput(attrs={'placeholder': 'Ejemplo: 150 kWh','class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'fecha_emision': 'Fecha de Emisión',
            'fecha_vencimiento': 'Fecha de Vencimiento',
            'monto_total': 'Monto Total ($)',
            'consumo_energetico': 'Consumo Energético',
            'estado': 'Estado'
        }
    #def clean_monto_total se encarga de validar que el monto total sea mayor a 0
    def clean_monto_total(self):
        monto = self.cleaned_data.get('monto_total')
        
        if monto < 0:
            raise forms.ValidationError("El monto total no puede ser negativo.")
        
        if monto == 0:
            raise forms.ValidationError("El monto total debe ser mayor a cero.")
        
        return monto
    #def clean_fecha_vencimiento se encarga de validar que la fecha de vencimiento sea posterior a la fecha de emisión y que tenga al menos 15 días para pagar
    def clean_fecha_vencimiento(self):
        fecha_emision = self.cleaned_data.get('fecha_emision')
        fecha_vencimiento = self.cleaned_data.get('fecha_vencimiento')
        
        if fecha_emision and fecha_vencimiento:
            if fecha_vencimiento <= fecha_emision:
                raise forms.ValidationError("La fecha de vencimiento debe ser posterior a la fecha de emisión.")
            
            # Validar que tenga al menos 15 días para pagar
            diferencia = fecha_vencimiento - fecha_emision
            if diferencia.days < 15:
                raise forms.ValidationError("La boleta debe tener al menos 15 días para el pago")
        
        return fecha_vencimiento


# ==========================================================
# FORMULARIO PAGO
# ==========================================================
class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['fecha_pago', 'monto_pagado', 'metodo_pago', 'numero_referencia', 'estado_pago']
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'monto_pagado': forms.NumberInput(attrs={'placeholder': 'Monto pagado','class': 'form-control','min': '1'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'numero_referencia': forms.TextInput(attrs={'placeholder': 'Número de referencia o comprobante','class': 'form-control'}),
            'estado_pago': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'fecha_pago': 'Fecha de Pago',
            'monto_pagado': 'Monto Pagado ($)',
            'metodo_pago': 'Método de Pago',
            'numero_referencia': 'Número de Referencia',
            'estado_pago': 'Estado del Pago'
        }
    #def clean_numero_referencia se encarga de validar que el número de referencia no esté vacío y que no exista otro pago con el mismo número
    def clean_numero_referencia(self):
        referencia = self.cleaned_data.get('numero_referencia')

        if len(referencia) < 1:
            raise forms.ValidationError("El número de referencia debe tener al menos 1 carácter")

        pagos = Pago.objects.filter(numero_referencia=referencia)
        if self.instance.id:
            pagos = pagos.exclude(id=self.instance.id)
        
        if pagos.exists():
            raise forms.ValidationError("Ya existe un pago con este número de referencia.")
        
        return referencia
    #def clean_monto_pagado se encarga de validar que el monto pagado sea mayor a 0
    def clean_monto_pagado(self):
        monto = self.cleaned_data.get('monto_pagado')
        
        if monto <= 0:
            raise forms.ValidationError("El monto pagado debe ser mayor a cero.")
        return monto
    #def clean_fecha_pago se encarga de validar que la fecha de pago no sea futura
    def clean_fecha_pago(self):
        fecha_pago = self.cleaned_data.get('fecha_pago')
        
        if fecha_pago and fecha_pago > date.today():
            raise forms.ValidationError("La fecha de pago no puede ser futura.")
        
        return fecha_pago


# ==========================================================
# FORMULARIO USUARIO
# ==========================================================
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'email', 'telefono', 'rol']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario único','class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Contraseña (mínimo 6 caracteres)','class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com','class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'placeholder': '+56 9 1234 5678','class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'username': 'Nombre de Usuario',
            'password': 'Contraseña',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'rol': 'Rol del Usuario'
        }
    #def clean_telefono se encarga de validar que el teléfono tenga al menos 8 dígitos
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        usuarios = Usuario.objects.filter(email=email)
        if self.instance.id:
            usuarios = usuarios.exclude(id=self.instance.id)
        
        if usuarios.exists():
            raise forms.ValidationError("Ya existe un usuario con este correo.")
        
        return email
    #def clean_username se encarga de validar que el nombre de usuario tenga al menos 3 caracteres y que no exista otro usuario con el mismo nombre
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if len(username) < 3:
            raise forms.ValidationError("El nombre de usuario debe tener al menos 3 caracteres")
        
        usuarios = Usuario.objects.filter(username=username)
        if self.instance.id:
            usuarios = usuarios.exclude(id=self.instance.id)
        
        if usuarios.exists():
            raise forms.ValidationError("Ya existe un usuario con este nombre de usuario.")
        
        return username
    #def clean_telefono se encarga de validar que el teléfono tenga al menos 8 dígitos
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        # Permitir solo números y el símbolo +, sin letras
        patron = re.compile(r'^\+?\d+$')
        if telefono and not patron.match(telefono):
            raise forms.ValidationError("El teléfono solo puede contener números y el símbolo '+', sin espacios ni letras.")
        return telefono
    #def clean_password se encarga de validar que la contraseña tenga al menos 6 caracteres
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if len(password) < 6:
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres")
        
        return password


# ==========================================================
# FORMULARIO NOTIFICACION PAGO
# ==========================================================
class NotificacionPagoForm(forms.ModelForm):
    class Meta:
        model = NotificacionPago
        fields = ['deuda_pendiente']
        widgets = {
            'deuda_pendiente': forms.Textarea(attrs={'placeholder': 'Descripción de la deuda pendiente','class': 'form-control','rows': 3})
        }
        labels = {
            'deuda_pendiente': 'Descripción de Deuda Pendiente'
        }
    #def clean_deuda_pendiente se encarga de validar que la información de deuda pendiente no esté vacía
    def clean_deuda_pendiente(self):
        deuda = self.cleaned_data.get('deuda_pendiente')
        
        if not deuda or deuda.strip() == '':
            raise forms.ValidationError("La información de deuda pendiente es requerida.")
        
        if len(deuda) < 10:
            raise forms.ValidationError("La descripción debe tener al menos 10 caracteres")
        
        return deuda


# ==========================================================
# FORMULARIO NOTIFICACION LECTURA
# ==========================================================
class NotificacionLecturaForm(forms.ModelForm):
    class Meta:
        model = NotificacionLectura
        fields = ['registro_consumo']
        widgets = {
            'registro_consumo': forms.Textarea(attrs={'placeholder': 'Descripción del registro de consumo','class': 'form-control','rows': 3})
        }
        labels = {
            'registro_consumo': 'Registro de Consumo'
        }
    #def clean_registro_consumo se encarga de validar que la información de registro de consumo no esté vacía
    def clean_registro_consumo(self):
        registro = self.cleaned_data.get('registro_consumo')
        
        if not registro or registro.strip() == '':
            raise forms.ValidationError("El registro de consumo es requerido.")
        
        if len(registro) < 10:
            raise forms.ValidationError("El registro debe tener al menos 10 caracteres")
        
        return registro
