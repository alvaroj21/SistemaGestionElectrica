"""
Este módulo contiene todas las vistas del sistema de gestión eléctrica desarrollado en Django.
El sistema permite gestionar clientes, contratos, medidores, lecturas, boletas, pagos, tarifas,
usuarios y notificaciones con un sistema de autenticación por roles.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cliente, Contrato, Tarifa, Medidor, Lectura, Boleta, Pago, Usuario, Notification


# ============================================================================
# CONFIGURACIÓN DEL SISTEMA
# ============================================================================

# Diccionario que almacena los usuarios del sistema con sus credenciales y roles
USUARIOS = {
    'admin': {'password': 'admin123', 'rol': 'admin', 'nombre': 'Administrador'},
    'prueba': {'password': '1234', 'rol': 'admin', 'nombre': 'Alvaro Pinto - Administrador'},
    'electrico1': {'password': 'elec123', 'rol': 'electrico', 'nombre': 'Juan Pérez - Eléctrico'},
    'finanzas1': {'password': 'fin123', 'rol': 'finanzas', 'nombre': 'María García - Finanzas'},
}

# Diccionario que define qué módulos puede acceder cada rol
PERMISOS_ROL = {
    'admin': ['medidores', 'lecturas', 'clientes', 'contratos', 'tarifas', 'boletas', 'pagos', 'usuarios', 'notificaciones'],
    'electrico': ['medidores', 'lecturas', 'notificaciones'],
    'finanzas': ['clientes', 'contratos', 'tarifas', 'boletas', 'pagos', 'notificaciones'],
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
        
        if username in USUARIOS and USUARIOS[username]['password'] == password:
            request.session['user_logged'] = True
            request.session['username'] = username
            request.session['rol'] = USUARIOS[username]['rol']
            request.session['nombre'] = USUARIOS[username]['nombre']
            
            messages.success(request, f'Bienvenido {USUARIOS[username]["nombre"]}')
            return redirect('sistemaGestion:dashboard')
        else:
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
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'clientes'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre')
    }
    return render(request, 'clientes/crear_cliente.html', datos)


# ============================================================================
# VISTAS PARA GESTIÓN DE CONTRATOS
# ============================================================================

def lista_contratos(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'contratos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    contratos = Contrato.objects.select_related('cliente_id_cliente').all()
    
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
    
    # Usar modelos reales
    clientes = Cliente.objects.all()
    tarifas = Tarifa.objects.all()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'clientes': clientes,
        'tarifas': tarifas
    }
    return render(request, 'contratos/crear_contrato.html', datos)


# ============================================================================
# VISTAS PARA GESTIÓN DE MEDIDORES
# ============================================================================

def lista_medidores(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'medidores'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    medidores = Medidor.objects.select_related('contrato_id_contrato').all()
    
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

    contratos = Contrato.objects.all()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'contratos': contratos
    }
    return render(request, 'medidores/crear_medidor.html', datos)

def ubicacion_medidor(request):
    """
    Vista que muestra la ubicación específica de un medidor en un mapa o interfaz de ubicación.
    Requiere permisos de 'medidores'.
    """
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'medidores'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Obtener medidor específico
    medidor_id = request.GET.get('id', 1)
    try:
        medidor = Medidor.objects.get(id_medidor=medidor_id)
    except Medidor.DoesNotExist:
        medidor = None
        messages.error(request, 'Medidor no encontrado')
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'medidor': medidor
    }
    return render(request, 'medidores/ubicacion_medidor.html', datos)


# ============================================================================
# VISTAS PARA GESTIÓN DE LECTURAS
# ============================================================================

def lista_lecturas(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')

    if not tiene_permiso(request, 'lecturas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    lecturas = Lectura.objects.select_related('medidor_id_medidor').all()
    
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
    
    medidores = Medidor.objects.all()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'medidores': medidores
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
    
    boletas = Boleta.objects.select_related('lectura_id_lectura').all()
    
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
    
    notificaciones = Notification.objects.all()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'notificaciones': notificaciones
    }
    return render(request, 'notificaciones/lista_notificaciones.html', datos)

# ============================================================================
# VISTAS FALTANTES - AGREGAR ESTAS FUNCIONES
# ============================================================================

def ubicacion_medidor(request):
    """
    Vista que muestra la ubicación específica de un medidor.
    Requiere permisos de 'medidores'.
    """
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'medidores'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Obtener medidor específico
    medidor_id = request.GET.get('id', 1)
    try:
        medidor = Medidor.objects.get(id_medidor=medidor_id)
    except Medidor.DoesNotExist:
        medidor = None
        messages.error(request, 'Medidor no encontrado')
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'medidor': medidor
    }
    return render(request, 'medidores/ubicacion_medidor.html', datos)


def detalle_lectura(request):
    """
    Vista que muestra el detalle de una lectura específica.
    Requiere permisos de 'lecturas'.
    """
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'lecturas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Obtener lectura específica
    lectura_id = request.GET.get('id', 1)
    try:
        lectura = Lectura.objects.get(id_lectura=lectura_id)
    except Lectura.DoesNotExist:
        lectura = None
        messages.error(request, 'Lectura no encontrada')
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'lectura': lectura
    }
    return render(request, 'lecturas/detalle_lectura.html', datos)


def crear_boleta(request):
    """
    Vista que muestra el formulario para crear una nueva boleta.
    Requiere permisos de 'boletas'.
    """
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'boletas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Obtener lecturas disponibles
    lecturas = Lectura.objects.all()
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'lecturas': lecturas
    }
    return render(request, 'boletas/crear_boleta.html', datos)


def crear_pago(request):
    """
    Vista que muestra el formulario para crear un nuevo pago.
    Requiere permisos de 'pagos'.
    """
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'pagos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Obtener boletas pendientes
    boletas = Boleta.objects.filter(estado='Pendiente')
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'boletas': boletas
    }
    return render(request, 'pagos/crear_pago.html', datos)


def crear_tarifa(request):
    """
    Vista que muestra el formulario para crear una nueva tarifa.
    Requiere permisos de 'tarifas'.
    """
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'tarifas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre')
    }
    return render(request, 'tarifas/crear_tarifa.html', datos)


def crear_usuario(request):
    """
    Vista que muestra el formulario para crear un nuevo usuario.
    Requiere permisos de 'usuarios'.
    """
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'usuarios'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre')
    }
    return render(request, 'usuarios/crear_usuario.html', datos)


def lista_pagos(request):
    """
    Vista que muestra la lista de pagos.
    Requiere permisos de 'pagos'.
    """
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