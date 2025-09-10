"""
Este módulo contiene todas las vistas del sistema de gestión eléctrica desarrollado en Django.
El sistema permite gestionar clientes, contratos, medidores, lecturas, boletas, pagos, tarifas,
usuarios y notificaciones con un sistema de autenticación por roles.
"""

from django.shortcuts import render, redirect
from django.contrib import messages


# ============================================================================
# CONFIGURACIÓN DEL SISTEMA
# ============================================================================

# Diccionario que almacena los usuarios del sistema con sus credenciales y roles
# Estructura: 'username': {'password': 'contraseña', 'rol': 'tipo_rol', 'nombre': 'nombre_completo'}
USUARIOS = {
    'admin': {'password': 'admin123', 'rol': 'admin', 'nombre': 'Administrador'},
    'prueba': {'password': '1234', 'rol': 'admin', 'nombre': 'Alvaro Pinto - Administrador'},
    'electrico1': {'password': 'elec123', 'rol': 'electrico', 'nombre': 'Juan Pérez - Eléctrico'},
    'finanzas1': {'password': 'fin123', 'rol': 'finanzas', 'nombre': 'María García - Finanzas'},
}

# Diccionario que define qué módulos puede acceder cada rol
# - admin: acceso completo a todos los módulos del sistema
# - electrico: acceso limitado a medidores, lecturas y notificaciones
# - finanzas: acceso a gestión comercial (clientes, contratos, tarifas, boletas, pagos, notificaciones)
PERMISOS_ROL = {
    'admin': ['medidores', 'lecturas', 'clientes', 'contratos', 'tarifas', 'boletas', 'pagos', 'usuarios', 'notificaciones'],
    'electrico': ['medidores', 'lecturas', 'notificaciones'],
    'finanzas': ['clientes', 'contratos', 'tarifas', 'boletas', 'pagos', 'notificaciones'],
}


# ============================================================================
# FUNCIONES AUXILIARES DE AUTENTICACIÓN
# ============================================================================

def usuario_logueado(request):
    """
    Verifica si existe un usuario autenticado en la sesión actual.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP de Django
        
    Returns:
        bool: True si hay un usuario logueado, False en caso contrario
    """
    return request.session.get('user_logged', False)

def tiene_permiso(request, modulo):
    """
    Verifica si el usuario actual tiene permisos para acceder a un módulo específico.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP de Django
        modulo (str): Nombre del módulo a verificar
        
    Returns:
        bool: True si tiene permisos, False en caso contrario
    """
    # Verificar primero si el usuario está logueado
    if not usuario_logueado(request):
        return False
    
    # Obtener el rol del usuario desde la sesión
    rol = request.session.get('rol', '')
    # Obtener la lista de permisos para ese rol
    permisos = PERMISOS_ROL.get(rol, [])
    # Verificar si el módulo está en la lista de permisos
    return modulo in permisos


# ============================================================================
# VISTAS DE AUTENTICACIÓN (LOGIN Y LOGOUT)
# ============================================================================

def login_view(request):
    """
    Vista que maneja el proceso de autenticación de usuarios.
    
    GET: Muestra el formulario de login
    POST: Procesa las credenciales y autentica al usuario
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza la página de login o redirige al dashboard
    """
    # Si el usuario ya está logueado, redirigir al dashboard
    if usuario_logueado(request):
        return redirect('sistemaGestion:dashboard')
    
    # Procesar formulario de login (método POST)
    if request.method == 'POST':
        # Obtener credenciales del formulario
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Verificar que el usuario existe y la contraseña es correcta
        if username in USUARIOS and USUARIOS[username]['password'] == password:
            # Guardar información del usuario en la sesión
            request.session['user_logged'] = True
            request.session['username'] = username
            request.session['rol'] = USUARIOS[username]['rol']
            request.session['nombre'] = USUARIOS[username]['nombre']
            
            # Mostrar mensaje de bienvenida y redirigir al dashboard
            messages.success(request, f'Bienvenido {USUARIOS[username]["nombre"]}')
            return redirect('sistemaGestion:dashboard')
        else:
            # Mostrar error si las credenciales son incorrectas
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    # Mostrar la página de login
    return render(request, 'auth/login.html')

def logout_view(request):
    """
    Vista que maneja el cierre de sesión del usuario.
    Limpia toda la información de la sesión y redirige al login.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Redirige a la página de login
    """
    # Limpiar toda la sesión del usuario
    request.session.flush()
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('sistemaGestion:login')


# ============================================================================
# VISTA DEL DASHBOARD PRINCIPAL
# ============================================================================

def dashboard(request):
    """
    Vista principal del sistema que muestra estadísticas generales.
    Requiere que el usuario esté autenticado.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza el dashboard o redirige al login
    """
    # Verificar que el usuario esté logueado
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Datos estadísticos del sistema (simulados)
    datos = {
        'total_clientes': 120,
        'total_contratos': 98,
        'total_medidores': 98,
        'lecturas_pendientes': 15,
        'boletas_emitidas': 45,
        'gastos_pagados': 32,
    }
    return render(request, 'dashboard.html', datos)

def interfaz(request):
    """
    Vista de redirección hacia el dashboard principal.
    Funciona como página de inicio del sistema.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP de Django
    
    Returns:
        HttpResponse: Redirige al dashboard
    """
    return redirect('sistemaGestion:dashboard')


# ============================================================================
# VISTAS PARA GESTIÓN DE CLIENTES
# ============================================================================

def lista_clientes(request):
    """
    Vista que muestra la lista completa de clientes registrados en el sistema.
    Requiere permisos de 'clientes'.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza la lista de clientes o redirige según permisos
    """
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')

    # Verificar permisos para acceder a la gestión de clientes
    if not tiene_permiso(request, 'clientes'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de clientes de ejemplo (en un sistema real, estos datos vendrían de la base de datos)
    clientes = [
        {
            'nombre': 'Juan Pérez', 
            'email': 'juan@email.com', 
            'telefono': '123456789', 
            'numero_cliente': 'CL-001'
        },
        {
            'nombre': 'María Rodríguez', 
            'email': 'maria@email.com', 
            'telefono': '987654321', 
            'numero_cliente': 'CL-002'
        },
        {
            'nombre': 'Carlos Sánchez', 
            'email': 'carlos@email.com', 
            'telefono': '111222333', 
            'numero_cliente': 'CL-003'
        },
        {
            'nombre': 'Ana Gomez', 
            'email': 'ana@email.com', 
            'telefono': '14262333', 
            'numero_cliente': 'CL-004'
        },
    ]
    
    # Preparar datos para enviar al template
    datos = {
        'clientes': clientes
    }
    return render(request, 'clientes/lista_clientes.html', datos)

def crear_cliente(request):
    """
    Vista que muestra el formulario para crear un nuevo cliente.
    Requiere permisos de 'clientes'.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza el formulario de creación de cliente
    """
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'clientes'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Datos del usuario actual para mostrar en el template
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre')
    }
    return render(request, 'clientes/crear_cliente.html', datos)


# ============================================================================
# VISTAS PARA GESTIÓN DE CONTRATOS
# ============================================================================

def lista_contratos(request):
    """
    Vista que muestra la lista de todos los contratos del sistema.
    Incluye información del cliente asociado y estado del contrato.
    Requiere permisos de 'contratos'.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza la lista de contratos
    """
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'contratos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de contratos de ejemplo
    contratos = [
        {
            'numero_contrato': 'CON-001', 
            'fecha_inicio': '21-05-2025', 
            'fecha_fin': '21-09-2025', 
            'estado': 'Activo',
            'cliente_nombre': 'Juan Pérez'
        },
        {
            'numero_contrato': 'CON-002', 
            'fecha_inicio': '21-05-2025', 
            'fecha_fin': '21-09-2025', 
            'estado': 'Activo',
            'cliente_nombre': 'María Rodríguez'  
        },
        { 
            'numero_contrato': 'CON-003', 
            'fecha_inicio': '21-05-2025', 
            'fecha_fin': '21-09-2025', 
            'estado': 'Vencido',
            'cliente_nombre': 'Carlos Sánchez'  
        },
    ]
    
    # Preparar datos para el template
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'contratos': contratos
    }
    return render(request, 'contratos/lista_contratos.html', datos)

def crear_contrato(request):
    """
    Vista que muestra el formulario para crear un nuevo contrato.
    Incluye listas de clientes y tarifas disponibles para seleccionar.
    Requiere permisos de 'contratos'.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza el formulario de creación de contrato
    """
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'contratos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de clientes disponibles para asignar al contrato
    clientes = [
        {
            'nombre': 'Juan Pérez', 
            'numero_cliente': 'CL-001'
        },
        {
            'nombre': 'María Rodríguez', 
            'numero_cliente': 'CL-002'
        },
        {
            'nombre': 'Carlos Sánchez', 
            'numero_cliente': 'CL-003'
        },
        {
            'nombre': 'Ana Gomez', 
            'numero_cliente': 'CL-004'
        },
    ]

    # Lista de tarifas disponibles para asignar al contrato
    tarifas = [
        {'tipo_tarifa': 'Invierno','tipo_cliente': 'Residencial'},
        {'tipo_tarifa': 'Invierno','tipo_cliente': 'Comercial'},
        {'tipo_tarifa': 'Invierno','tipo_cliente': 'Industrial'}
    ]
    
    # Preparar datos para el template
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
    """
    Vista que muestra la lista de todos los medidores instalados en el sistema.
    Incluye información de ubicación, estado y cliente asociado.
    Requiere permisos de 'medidores'.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza la lista de medidores
    """
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'medidores'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de medidores de ejemplo
    medidores = [
        {
            'id_medidor': 1,
            'numero_medidor': 'MED-001', 
            'fecha_instalacion': '05-03-2021',
            'ubicacion': 'Calle Principal 123, Casa Juan Pérez',
            'estado_medidor': 'Activo',
            'cliente_nombre': 'Juan Perez'  
        },
        {
            'id_medidor': 2,
            'numero_medidor': 'MED-002', 
            'fecha_instalacion': '20-03-2021',
            'ubicacion': 'Av. Comercial 456, Local María Rodríguez',
            'estado_medidor': 'Activo',
            'cliente_nombre': 'Maria Rodríguez'  
        },
        {
            'id_medidor': 3,
            'numero_medidor': 'MED-003', 
            'fecha_instalacion': '01-12-2023',
            'ubicacion': 'Barrio Industrial 789, Empresa Carlos Sánchez',
            'estado_medidor': 'Mantenimiento',
            'cliente_nombre': 'Carlos Castillo'  
        },
    ]
    
    # Preparar datos para el template
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'medidores': medidores
    }
    return render(request, 'medidores/lista_medidores.html', datos)

def crear_medidor(request):
    """
    Vista que muestra el formulario para registrar un nuevo medidor.
    Incluye lista de clientes disponibles para asignar el medidor.
    Requiere permisos de 'medidores'.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza el formulario de creación de medidor
    """
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'medidores'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de clientes disponibles para asignar el medidor
    clientes = [
        {
            'nombre': 'Juan Pérez', 
            'numero_cliente': 'CL-001'
        },
        {
            'nombre': 'María Rodríguez', 
            'numero_cliente': 'CL-002'
        },
        {
            'nombre': 'Carlos Sánchez', 
            'numero_cliente': 'CL-003'
        },
        {
            'nombre': 'Ana Gomez', 
            'numero_cliente': 'CL-004'
        },
    ]
    
    # Preparar datos para el template
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'clientes': clientes
    }
    return render(request, 'medidores/crear_medidor.html', datos)

def ubicacion_medidor(request):
    """
    Vista que muestra la ubicación específica de un medidor en un mapa o interfaz de ubicación.
    Requiere permisos de 'medidores'.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza la página de ubicación del medidor
    """
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'medidores'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Datos simulados del medidor específico
    medidor = {
        'id_medidor': 1,
        'numero_medidor': 'MED-001',
        'cliente_nombre': 'Juan Perez',
        'ubicacion': 'Ubicación de Prueba',
        'direccion': 'Calle 123',
        'estado_medidor': 'Activo',
        'fecha_instalacion': '03-04-2021'
    }
    
    # Preparar datos para el template
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
    """
    Vista que muestra el historial de lecturas de consumo eléctrico.
    Incluye información del medidor, consumo y tipo de lectura.
    Requiere permisos de 'lecturas'.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza la lista de lecturas
    """
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')

    # Verificar permisos
    if not tiene_permiso(request, 'lecturas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de lecturas de ejemplo
    lecturas = [
        {
            'fecha_lectura': '01-09-2025', 
            'consumo_energetico': 125,  
            'tipo_lectura': 'Manual', 
            'lectura_actual': 1250,    
            'medidor_numero': 'MED-001'  
        },
        {
            'fecha_lectura': '01-09-2025', 
            'consumo_energetico': 98,  
            'tipo_lectura': 'Automatica',
            'lectura_actual': 980,
            'medidor_numero': 'MED-002'  
        },
        {
            'fecha_lectura': '01-08-2025', 
            'consumo_energetico': 156,
            'tipo_lectura': 'Manual',
            'lectura_actual': 1125,
            'medidor_numero': 'MED-001'  
        },
    ]
    
    # Preparar datos para el template
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'lecturas': lecturas
    }
    return render(request, 'lecturas/lista_lecturas.html', datos)

def crear_lectura(request):
    """
    Vista que muestra el formulario para registrar una nueva lectura de consumo.
    Incluye lista de medidores disponibles para tomar lectura.
    Requiere permisos de 'lecturas'.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza el formulario de creación de lectura
    """
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'lecturas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de medidores disponibles para tomar lectura
    medidores = [
        {'id_medidor': 1, 'numero_medidor': 'MED-001', 'estado': 'Activo'},
        {'id_medidor': 2, 'numero_medidor': 'MED-002', 'estado': 'Activo'},
        {'id_medidor': 3, 'numero_medidor': 'MED-003', 'estado': 'Inactivo'},
        {'id_medidor': 4, 'numero_medidor': 'MED-004', 'estado': 'Activo'},
    ]
    
    # Preparar datos para el template
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
    """
    Vista que muestra la lista de boletas emitidas con sus estados de pago.
    Incluye estadísticas generales de facturación.
    Requiere permisos de 'boletas'.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza la lista de boletas con estadísticas
    """
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'boletas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de boletas de ejemplo
    boletas = [
        {
            'id_boleta': 1,
            'fecha_emision': '17-09-2025',
            'fecha_vencimiento': '22-10-2025',
            'monto_total': 28400,                  
            'consumo_energetico': 125,               
            'estado': 'Pendiente',                      
            'cliente_nombre': 'Juan Pérez'  
        },
        {
            'id_boleta': 2,
            'fecha_emision': '17-09-2025',
            'fecha_vencimiento': '22-10-2025',
            'monto_total': 23600,
            'consumo_energetico': 98,
            'estado': 'Pagada',
            'cliente_nombre': 'María Rodríguez' 
        },
        {
            'id_boleta': 3,
            'fecha_emision': '17-07-2025',
            'fecha_vencimiento': '22-08-2025',
            'monto_total': 35200,
            'consumo_energetico': 156,
            'estado': 'Vencida',
            'cliente_nombre': 'Juan Pérez'  
        },
    ]
    
    # Estadísticas generales del sistema de facturación
    estadisticas = {
        'total_servicios': 45,             
        'servicios_pagados': 32,          
        'servicios_pendientes': 13,         
        'gasto_total_presupuestado': 125750,
        'total_pagado': 89320,            
        'porcentaje_pagado': 71.1           
    }
    
    # Preparar datos para el template
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'boletas': boletas,
        'estadisticas': estadisticas
    }
    return render(request, 'boletas/lista_boletas.html', datos)
    
def crear_boleta(request):
    """
    Vista que muestra el formulario para emitir una nueva boleta.
    Incluye lista de clientes para seleccionar.
    Requiere permisos de 'boletas'.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza el formulario de creación de boleta
    """
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'boletas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de clientes disponibles para emitir boleta
    clientes = [
        {'idCliente': 1, 'nombre': 'Juan Pérez', 'estado': 'Activo'},
        {'idCliente': 2, 'nombre': 'María Rodríguez', 'estado': 'Activo'},
        {'idCliente': 3, 'nombre': 'Carlos Sánchez', 'estado': 'Activo'},
        {'idCliente': 4, 'nombre': 'Ana Gomez', 'estado': 'Activo'},
    ]
    
    # Preparar datos para el template
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'clientes': clientes
    }
    return render(request, 'boletas/crear_boleta.html', datos)


# ============================================================================
# VISTAS PARA GESTIÓN DE PAGOS
# ============================================================================

def lista_pagos(request):
    """
    Vista que muestra el historial de pagos recibidos de los clientes.
    Incluye método de pago, referencia y estado de confirmación.
    Requiere permisos de 'pagos'.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza la lista de pagos registrados
    """
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'pagos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de pagos registrados en el sistema
    pagos = [
        {
            'idpago': 1,
            'fecha_pago': '20-07-2025',
            'monto_pagado': 23600,                   
            'metodo_pago': 'Transferencia Bancaria',  
            'numero_referencia': 'TRF001',             
            'estado_pago': 'Confirmado',                
            'cliente_nombre': 'María Rodríguez'  
        },
        {
            'idpago': 2,
            'fecha_pago': '15-08-2024',
            'monto_pagado': 31500,
            'metodo_pago': 'Efectivo',
            'numero_referencia': 'EFE001',
            'estado_pago': 'Confirmado',
            'cliente_nombre': 'Juan Pérez' 
        },
        {
            'idpago': 3,
            'fecha_pago': '11-05-2025',
            'monto_pagado': 15000,
            'metodo_pago': 'Tarjeta de Crédito',
            'numero_referencia': 'TDC001',
            'estado_pago': 'Pendiente',
            'cliente_nombre': 'Carlos Mendoza' 
        },
    ]
    
    # Preparar datos para el template
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'pagos': pagos
    }
    return render(request, 'pagos/lista_pagos.html', datos)

def crear_pago(request):
    """
    Vista que muestra el formulario para registrar un nuevo pago.
    Incluye lista de boletas pendientes de pago.
    Requiere permisos de 'pagos'.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza el formulario de registro de pago
    """
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'pagos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de boletas pendientes de pago
    boletas = [
        {'numero_boleta': 'Bol-001', 'estado': 'Pendiente'},
        {'numero_boleta': 'Bol-002', 'estado': 'Pendiente'},
        {'numero_boleta': 'Bol-003', 'estado': 'Pendiente'},
        {'numero_boleta': 'Bol-004', 'estado': 'Pendiente'},
    ]
    
    # Preparar datos para el template
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'boletas': boletas
    }
    return render(request, 'pagos/crear_pago.html', datos)


# ============================================================================
# VISTAS PARA GESTIÓN DE TARIFAS
# ============================================================================

def lista_tarifas(request):
    """
    Vista que muestra las tarifas eléctricas vigentes en el sistema.
    Las tarifas se clasifican por tipo de cliente y temporada.
    Requiere permisos de 'tarifas'.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza la lista de tarifas vigentes
    """
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'tarifas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de tarifas vigentes en el sistema
    tarifas = [
        {
            'tipo_tarifa': 'Invierno',   
            'tipo_cliente': 'Residencial',  
            'precio': 120,                  
            'fecha_vigencia': '09-09-2025'  
        },
        {
            'tipo_tarifa': 'Invierno',
            'tipo_cliente': 'Comercial',
            'precio': 95,                   
            'fecha_vigencia': '09-09-2025'
        },
        {
            'tipo_tarifa': 'Invierno',
            'tipo_cliente': 'Industrial',
            'precio': 85,                   
            'fecha_vigencia': '09-09-2025'
        }
    ]
    
    # Preparar datos para el template
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'tarifas': tarifas
    }
    return render(request, 'tarifas/lista_tarifas.html', datos)

def crear_tarifa(request):
    """
    Vista que muestra el formulario para crear una nueva tarifa eléctrica.
    Requiere permisos de 'tarifas'.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza el formulario de creación de tarifa
    """
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'tarifas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Preparar datos para el template
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre')
    }
    return render(request, 'tarifas/crear_tarifa.html', datos)


# ============================================================================
# VISTAS PARA GESTIÓN DE USUARIOS DEL SISTEMA
# ============================================================================

def lista_usuarios(request):
    """
    Vista que muestra la lista de usuarios del sistema con sus roles asignados.
    Solo accesible para usuarios con rol 'admin'.
    Requiere permisos de 'usuarios'.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza la lista de usuarios del sistema
    """
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos (solo admins pueden gestionar usuarios)
    if not tiene_permiso(request, 'usuarios'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de usuarios registrados en el sistema
    usuarios = [
        {
            'idUsuario': 1,
            'nombreUsuario': 'electrico1',         
            'nombre': 'Juan Eléctrico',             
            'email': 'juan@sistemaelectrico.com',  
            'telefono': '+56987654321',             
            'rol': 'electrico',                     
        },
        {
            'idUsuario': 2,
            'nombreUsuario': 'admin',
            'nombre': 'Admin Sistema',
            'email': 'admin@sistemaelectrico.com',
            'telefono': '+56912345678',
            'rol': 'admin',                         
        },
        {
            'idUsuario': 3,
            'nombreUsuario': 'finanzas1',
            'nombre': 'Ana Finanzas',
            'email': 'ana@sistemaelectrico.com',
            'telefono': '+56923456789',
            'rol': 'finanzas',                      
        },
    ]
    
    # Preparar datos para el template
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'usuarios': usuarios
    }
    return render(request, 'usuarios/lista_usuarios.html', datos)

def crear_usuario(request):
    """
    Vista que muestra el formulario para crear un nuevo usuario del sistema.
    Solo accesible para usuarios con rol 'admin'.
    Requiere permisos de 'usuarios'.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza el formulario de creación de usuario
    """
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos (solo admins pueden crear usuarios)
    if not tiene_permiso(request, 'usuarios'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Preparar datos para el template
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre')
    }
    return render(request, 'usuarios/crear_usuario.html', datos)


# ============================================================================
# VISTAS PARA SISTEMA DE NOTIFICACIONES
# ============================================================================
 
def lista_notificaciones(request):
    """
    Vista que muestra las notificaciones del sistema para el usuario actual.
    Las notificaciones incluyen alertas sobre consumos altos, pagos vencidos, etc.
    Todos los usuarios tienen acceso a las notificaciones.
    
    Args:
        request (HttpRequest): Objeto de petición HTTP
        
    Returns:
        HttpResponse: Renderiza la lista de notificaciones del sistema
    """
    # Verificar autenticación (todos los usuarios logueados pueden ver notificaciones)
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Lista de notificaciones del sistema
    notificaciones = [
        {
            'tipo': 'Lectura',                              
            'titulo': 'Consumo Alto Detectado',           
            'mensaje': 'El cliente Juan Pérez ha superado el consumo promedio en un 150%',  
        },
        {
            'id_notificacion': 2,
            'tipo': 'Pago',                                 
            'titulo': 'Pago Vencido',
            'mensaje': 'La boleta de María Rodríguez está vencida desde hace 5 días',
        },
    ]
    
    # Preparar datos para el template
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'notificaciones': notificaciones
    }
    return render(request, 'notificaciones/lista_notificaciones.html', datos)
