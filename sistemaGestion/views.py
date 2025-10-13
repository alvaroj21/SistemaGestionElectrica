"""
Este módulo contiene todas las vistas del sistema de gestión eléctrica desarrollado en Django.
El sistema permite gestionar clientes, contratos, medidores, lecturas, boletas, pagos, tarifas,
usuarios y notificaciones con un sistema de autenticación por roles.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cliente, Contrato, Tarifa, Medidor, Lectura, Boleta, Pago, Usuario, NotificacionPago, NotificacionLectura
from .forms import ClienteForm, ContratoForm, MedidorForm, LecturaForm, BoletaForm, PagoForm, TarifaForm, UsuarioForm


# ============================================================================
# CONFIGURACIÓN DEL SISTEMA
# ============================================================================

# Diccionario que define qué módulos puede acceder cada rol
PERMISOS_ROL = {
    'Administrador': ['medidores', 'lecturas', 'clientes', 'contratos', 'tarifas', 'boletas', 'pagos', 'usuarios', 'notificaciones'],
    'Eléctrico': ['medidores', 'lecturas', 'notificaciones'],
    'Finanzas': ['clientes', 'contratos', 'tarifas', 'boletas', 'pagos', 'notificaciones'],
}


# ============================================================================
# FUNCIONES AUXILIARES DE AUTENTICACIÓN
# ============================================================================

def usuario_logueado(request):
    return request.session.get('user_logged', False)

def tiene_permiso(request, modulo):
    if not usuario_logueado(request):
        return False
    rol = request.session.get('rol', '')
    permisos = PERMISOS_ROL.get(rol, [])
    return modulo in permisos


# ============================================================================
# VISTAS DE AUTENTICACIÓN (LOGIN Y LOGOUT)
# ============================================================================

def login_view(request):
    if usuario_logueado(request):
        return redirect('sistemaGestion:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            # Buscar el usuario en la base de datos
            usuario = Usuario.objects.get(username=username)
            
            # Verificar la contraseña (comparación simple)
            if usuario.password == password:
                # Iniciar sesión
                request.session['user_logged'] = True
                request.session['usuario'] = usuario.username
                request.session['username'] = usuario.username  # Agregado para consistencia
                request.session['rol'] = usuario.rol
                request.session['nombre'] = usuario.username
                request.session['email'] = usuario.email

                messages.success(request, f'Bienvenido {usuario.username}')
                return redirect('sistemaGestion:dashboard')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'auth/login.html')

def logout_view(request):
    request.session.flush()
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('sistemaGestion:login')


# ============================================================================
# VISTA DEL DASHBOARD PRINCIPAL
# ============================================================================

def dashboard(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # VISTA CORREGIDA - usar campos que SÍ existen
    datos = {
        'total_clientes': Cliente.objects.count(),
        'total_contratos': Contrato.objects.count(),
        'total_medidores': Medidor.objects.count(),
        'lecturas_pendientes': Lectura.objects.count(),  # ← CAMBIADO: usar count() simple
        'boletas_emitidas': Boleta.objects.count(),
        'pagos_realizados': Pago.objects.filter(estado_pago='Confirmado').count(),
    }
    return render(request, 'dashboard.html', datos)

def interfaz(request):
    return redirect('sistemaGestion:dashboard')


# ============================================================================
# VISTAS PARA GESTIÓN DE CLIENTES
# ============================================================================

def lista_clientes(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')

    if not tiene_permiso(request, 'clientes'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    clientes = Cliente.objects.all()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'clientes': clientes
    }
    return render(request, 'clientes/lista_clientes.html', datos)

def crear_cliente(request):
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'clientes'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Procesar formulario
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            # Guardar el cliente
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nombre}" creado exitosamente con número {cliente.numero_cliente}')
            return redirect('sistemaGestion:lista_clientes')
    else:
        # GET request - mostrar formulario vacío
        form = ClienteForm()
    
    # Preparar datos para el template
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'form': form
    }
    return render(request, 'clientes/crear_cliente.html', datos)


def editar_cliente(request, cliente_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    if not tiene_permiso(request, 'clientes'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        cliente = Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        messages.error(request, 'El cliente no existe')
        return redirect('sistemaGestion:lista_clientes')
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente_actualizado = form.save()
            messages.success(request, f'Cliente "{cliente_actualizado.nombre}" actualizado exitosamente')
            return redirect('sistemaGestion:lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'form': form,
        'cliente': cliente
    }
    return render(request, 'clientes/editar_cliente.html', datos)


def eliminar_cliente(request, cliente_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'clientes'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        cliente = Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
            messages.error(request, 'El cliente no existe')
            return redirect('sistemaGestion:lista_clientes')
    if request.method == 'POST':
        nombre_cliente = cliente.nombre
        cliente.delete()
        messages.success(request, f'Cliente "{nombre_cliente}" eliminado exitosamente')
        return redirect('sistemaGestion:lista_clientes')
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'cliente': cliente
    }
    return render(request, 'clientes/eliminar_cliente.html', datos)


# ============================================================================
# VISTAS PARA GESTIÓN DE CONTRATOS
# ============================================================================

def lista_contratos(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'contratos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    contratos = Contrato.objects.all()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'contratos': contratos
    }
    return render(request, 'contratos/lista_contratos.html', datos)

def crear_contrato(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'contratos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            contrato = form.save()
            messages.success(request, f'Contrato "{contrato.numero_contrato}" creado exitosamente')
            return redirect('sistemaGestion:lista_contratos')
    else:
        form = ContratoForm()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'form': form
    }
    return render(request, 'contratos/crear_contrato.html', datos)

def editar_contrato(request, contrato_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    if not tiene_permiso(request, 'contratos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')

    try:
        contrato = Contrato.objects.get(id=contrato_id)
    except Contrato.DoesNotExist:
        messages.error(request, 'El contrato no existe')
        return redirect('sistemaGestion:lista_contratos')

    if request.method == 'POST':
        form = ContratoForm(request.POST, instance=contrato)
        if form.is_valid():
            contrato_actualizado = form.save()
            messages.success(request, f'Contrato "{contrato_actualizado.numero_contrato}" actualizado exitosamente')
            return redirect('sistemaGestion:lista_contratos')
    else:
        form = ContratoForm(instance=contrato)

    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'form': form,
        'contrato': contrato
    }
    return render(request, 'contratos/editar_contrato.html', datos)


def eliminar_contrato(request, contrato_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')

    if not tiene_permiso(request, 'contratos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        contrato = Contrato.objects.get(id=contrato_id)
    except Contrato.DoesNotExist:
        messages.error(request, 'El contrato no existe')
        return redirect('sistemaGestion:lista_contratos')
    if request.method == 'POST':
        nombre_contrato = contrato.numero_contrato
        contrato.delete()
        messages.success(request, f'Contrato "{nombre_contrato}" eliminado exitosamente')
        return redirect('sistemaGestion:lista_contratos')
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'contrato': contrato
    }
    return render(request, 'contratos/eliminar_contrato.html', datos)


# ============================================================================
# VISTAS PARA GESTIÓN DE MEDIDORES
# ============================================================================

def lista_medidores(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'medidores'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    medidores = Medidor.objects.all()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'medidores': medidores
    }
    return render(request, 'medidores/lista_medidores.html', datos)

def crear_medidor(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'medidores'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')

    if request.method == 'POST':
        form = MedidorForm(request.POST)
        if form.is_valid():
            medidor = form.save()
            messages.success(request, f'Medidor "{medidor.numero_medidor}" creado exitosamente')
            return redirect('sistemaGestion:lista_medidores')
    else:
        form = MedidorForm()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'form': form
    }
    return render(request, 'medidores/crear_medidor.html', datos)


# ============================================================================
# VISTAS PARA GESTIÓN DE LECTURAS
# ============================================================================

def lista_lecturas(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')

    if not tiene_permiso(request, 'lecturas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    lecturas = Lectura.objects.all()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'lecturas': lecturas
    }
    return render(request, 'lecturas/lista_lecturas.html', datos)

def crear_lectura(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'lecturas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    if request.method == 'POST':
        form = LecturaForm(request.POST)
        if form.is_valid():
            lectura = form.save()
            messages.success(request, 'Lectura creada exitosamente')
            return redirect('sistemaGestion:lista_lecturas')
    else:
        form = LecturaForm()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'form': form
    }
    return render(request, 'lecturas/crear_lectura.html', datos)


# ============================================================================
# VISTAS PARA GESTIÓN DE BOLETAS
# ============================================================================

def lista_boletas(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'boletas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    boletas = Boleta.objects.all()
    
    # Estadísticas reales
    estadisticas = {
        'total_servicios': Boleta.objects.count(),
        'servicios_pagados': Pago.objects.filter(estado_pago='Confirmado').count(),
        'servicios_pendientes': Boleta.objects.filter(estado='Pendiente').count(),
        'gasto_total_presupuestado': sum(boleta.monto_total for boleta in boletas),
        'total_pagado': sum(pago.monto_pagado for pago in Pago.objects.filter(estado_pago='Confirmado')),
    }
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'boletas': boletas,
        'estadisticas': estadisticas
    }
    return render(request, 'boletas/lista_boletas.html', datos)


# ============================================================================
# VISTAS PARA GESTIÓN DE TARIFAS
# ============================================================================

def lista_tarifas(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'tarifas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    tarifas = Tarifa.objects.all()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'tarifas': tarifas
    }
    return render(request, 'tarifas/lista_tarifas.html', datos)


# ============================================================================
# VISTAS PARA GESTIÓN DE USUARIOS DEL SISTEMA
# ============================================================================

def lista_usuarios(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'usuarios'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    usuarios = Usuario.objects.all()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'usuarios': usuarios
    }
    return render(request, 'usuarios/lista_usuarios.html', datos)


# ============================================================================
# VISTAS PARA SISTEMA DE NOTIFICACIONES
# ============================================================================
 
def lista_notificaciones(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'notificaciones'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Obtener notificaciones de ambos tipos
    notificaciones_lectura = NotificacionLectura.objects.all()
    notificaciones_pago = NotificacionPago.objects.all()
    
    # Combinar ambos tipos de notificaciones
    notificaciones = []
    for notif in notificaciones_lectura:
        notificaciones.append({
            'tipo': 'Lectura',
            'titulo': 'Notificación de Lectura',
            'mensaje': notif.registro_consumo,
        })
    
    for notif in notificaciones_pago:
        notificaciones.append({
            'tipo': 'Pago',
            'titulo': 'Notificación de Pago',
            'mensaje': notif.deuda_pendiente,
        })
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'notificaciones': notificaciones
    }
    return render(request, 'notificaciones/lista_notificaciones.html', datos)

# ============================================================================
# VISTAS CREAR BOLETA Y PAGO, TARIFA Y USUARIO
# ============================================================================

def crear_boleta(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'boletas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    if request.method == 'POST':
        form = BoletaForm(request.POST)
        if form.is_valid():
            boleta = form.save()
            messages.success(request, 'Boleta creada exitosamente')
            return redirect('sistemaGestion:lista_boletas')
    else:
        form = BoletaForm()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'form': form
    }
    return render(request, 'boletas/crear_boleta.html', datos)


def crear_pago(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'pagos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save()
            messages.success(request, 'Pago registrado exitosamente')
            return redirect('sistemaGestion:lista_pagos')
    else:
        form = PagoForm()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'form': form
    }
    return render(request, 'pagos/crear_pago.html', datos)


def crear_tarifa(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'tarifas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    if request.method == 'POST':
        form = TarifaForm(request.POST)
        if form.is_valid():
            tarifa = form.save()
            messages.success(request, 'Tarifa creada exitosamente')
            return redirect('sistemaGestion:lista_tarifas')
    else:
        form = TarifaForm()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'form': form
    }
    return render(request, 'tarifas/crear_tarifa.html', datos)


def crear_usuario(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'usuarios'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuario "{usuario.username}" creado exitosamente')
            return redirect('sistemaGestion:lista_usuarios')
    else:
        form = UsuarioForm()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'form': form
    }
    return render(request, 'usuarios/crear_usuario.html', datos)


def lista_pagos(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'pagos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    pagos = Pago.objects.all()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'pagos': pagos
    }
    return render(request, 'pagos/lista_pagos.html', datos)