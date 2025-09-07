from django.shortcuts import render, redirect
from django.contrib import messages
from functools import wraps

# Definir roles y permisos como diccionarios
ROLES_PERMISOS = {
    'admin': ['medidores', 'lecturas', 'clientes', 'contratos', 'tarifas', 'boletas', 'pagos', 'usuarios', 'notificaciones'],
    'electrico': ['medidores', 'lecturas', 'notificaciones'],
    'finanzas': ['clientes', 'contratos', 'tarifas', 'boletas', 'pagos', 'notificaciones'],
}

# Usuarios predefinidos
USUARIOS = {
    'admin': {'password': 'admin123', 'rol': 'admin', 'nombre': 'Administrador'},
    'electrico1': {'password': 'elec123', 'rol': 'electrico', 'nombre': 'Juan Pérez - Eléctrico'},
    'finanzas1': {'password': 'fin123', 'rol': 'finanzas', 'nombre': 'María García - Finanzas'},
}

# Función helper para crear contexto común
def get_base_context(request):
    """Retorna el contexto base que necesitan todos los templates"""
    username = request.session.get('username', 'Usuario')
    rol = request.session.get('rol', 'invitado')
    nombre = request.session.get('nombre', username)
    
    return {
        'username': username,
        'nome': nombre,  # Variable que usa el template
        'nombre': nombre,
        'rol': rol,
        'permisos': ROLES_PERMISOS.get(rol, []),
        'notifications_count': 0,  # Placeholder para notificaciones
    }

# Decorador personalizado para verificar login
def requiere_login(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_logged'):
            return redirect('sistemaGestion:login')
        return view_func(request, *args, **kwargs)
    return wrapper

# Decorador para verificar permisos de módulo
def requiere_permiso(modulo):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.session.get('user_logged'):
                return redirect('sistemaGestion:login')
            
            rol_usuario = request.session.get('rol')
            permisos = ROLES_PERMISOS.get(rol_usuario, [])
            
            if modulo not in permisos:
                messages.error(request, 'No tienes permisos para acceder a esta sección')
                return redirect('sistemaGestion:dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if username in USUARIOS and USUARIOS[username]['password'] == password:
            # Guardar datos del usuario en la sesión
            request.session['user_logged'] = True
            request.session['username'] = username
            request.session['rol'] = USUARIOS[username]['rol']
            request.session['nombre'] = USUARIOS[username]['nombre']
            
            messages.success(request, f'Bienvenido {USUARIOS[username]["nombre"]}')
            return redirect('sistemaGestion:dashboard')
        else:
            messages.error(request, f'Credenciales inválidas. Usuario: {username}')
    
    return render(request, 'auth/login.html')

def logout_view(request):
    request.session.flush()  # Elimina toda la sesión
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('sistemaGestion:login')

@requiere_login
def dashboard(request):
    context = get_base_context(request)
    context.update({
        'total_clientes': 120,
        'total_contratos': 98,
        'total_medidores': 98,
        'lecturas_pendientes': 15,
        'boletas_emitidas': 45,
        'gastos_pagados': 32,
        'consumo_total_mes': 45678.5,
        'gasto_total_mes': 4256780,
    })
    return render(request, 'dashboard.html', context)

# Dashboard (función legacy, ahora se usa dashboard)
def interfaz(request):
    return redirect('sistemaGestion:dashboard')

# Clientes
@requiere_permiso('clientes')
def lista_clientes(request):
    clientes = [
        {'id': 1, 'nombre': 'Juan Pérez', 'email': 'juan@email.com', 'telefono': '123456789', 'estado': 'Activo'},
        {'id': 2, 'nombre': 'María Rodríguez', 'email': 'maria@email.com', 'telefono': '987654321', 'estado': 'Activo'},
        {'id': 3, 'nombre': 'Carlos Sánchez', 'email': 'carlos@email.com', 'telefono': '111222333', 'estado': 'Inactivo'},
    ]
    context = get_base_context(request)
    context['clientes'] = clientes
    return render(request, 'clientes/lista_clientes.html', context)

@requiere_permiso('clientes')
def crear_cliente(request):
    if request.method == 'POST':
        messages.success(request, 'Cliente creado exitosamente!')
        return redirect('sistemaGestion:lista_clientes')
    
    context = get_base_context(request)
    return render(request, 'clientes/crear_cliente.html', context)

# Contratos
@requiere_permiso('contratos')
def lista_contratos(request):
    contratos = [
        {'id': 1, 'numero': 'CON-001', 'cliente': 'Juan Pérez', 'tarifa': 'Residencial', 'estado': 'Activo'},
        {'id': 2, 'numero': 'CON-002', 'cliente': 'María Rodríguez', 'tarifa': 'Comercial', 'estado': 'Activo'},
    ]
    context = get_base_context(request)
    context['contratos'] = contratos
    return render(request, 'contratos/lista_contratos.html', context)

@requiere_permiso('contratos')
def crear_contrato(request):
    if request.method == 'POST':
        messages.success(request, 'Contrato creado exitosamente!')
        return redirect('sistemaGestion:lista_contratos')
    
    context = get_base_context(request)
    return render(request, 'contratos/crear_contrato.html', context)

# Medidores
@requiere_permiso('medidores')
def lista_medidores(request):
    medidores = [
        {'id': 1, 'numero': 'MED-001', 'cliente': 'Juan Pérez', 'tipo': 'Electrónico', 'estado': 'Activo'},
        {'id': 2, 'numero': 'MED-002', 'cliente': 'María Rodríguez', 'tipo': 'Digital', 'estado': 'Activo'},
    ]
    context = {
        'medidores': medidores,
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'rol': request.session.get('rol'),
        'permisos': ROLES_PERMISOS.get(request.session.get('rol'), []),
    }
    return render(request, 'medidores/lista_medidores.html', context)

@requiere_permiso('medidores')
def crear_medidor(request):
    if request.method == 'POST':
        messages.success(request, 'Medidor creado exitosamente!')
        return redirect('sistemaGestion:lista_medidores')
    
    context = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'rol': request.session.get('rol'),
        'permisos': ROLES_PERMISOS.get(request.session.get('rol'), []),
    }
    return render(request, 'medidores/crear_medidor.html', context)

# Lecturas
@requiere_permiso('lecturas')
def lista_lecturas(request):
    lecturas = [
        {
            'id': 1, 
            'medidor': 'MED-001', 
            'fecha_lectura': '2024-09-01', 
            'lectura_anterior': 1125,
            'lectura_actual': 1250,
            'consumo_energetico': 125,
            'tipo_lectura': 'Manual',
            'estado': 'Procesada'
        },
        {
            'id': 2, 
            'medidor': 'MED-002', 
            'fecha_lectura': '2024-09-01', 
            'lectura_anterior': 882,
            'lectura_actual': 980,
            'consumo_energetico': 98,
            'tipo_lectura': 'Automática',
            'estado': 'Pendiente'
        },
    ]
    context = {
        'lecturas': lecturas,
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'rol': request.session.get('rol'),
        'permisos': ROLES_PERMISOS.get(request.session.get('rol'), []),
    }
    return render(request, 'lecturas/lista_lecturas.html', context)

@requiere_permiso('lecturas')
def crear_lectura(request):
    if request.method == 'POST':
        messages.success(request, 'Lectura registrada exitosamente!')
        return redirect('sistemaGestion:lista_lecturas')
    
    context = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'rol': request.session.get('rol'),
        'permisos': ROLES_PERMISOS.get(request.session.get('rol'), []),
    }
    return render(request, 'lecturas/crear_lectura.html', context)

# Boletas
@requiere_permiso('boletas')
def lista_boletas(request):
    boletas = [
        {'id': 1, 'numero': 'BOL-001', 'cliente': 'Juan Pérez', 'monto': '45000', 'fecha': '2024-09-01', 'estado': 'Pendiente'},
        {'id': 2, 'numero': 'BOL-002', 'cliente': 'María Rodríguez', 'monto': '32000', 'fecha': '2024-09-01', 'estado': 'Pagada'},
    ]
    context = {
        'boletas': boletas,
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'rol': request.session.get('rol'),
        'permisos': ROLES_PERMISOS.get(request.session.get('rol'), []),
    }
    return render(request, 'boletas/lista_boletas.html', context)

@requiere_permiso('boletas')
def crear_boleta(request):
    if request.method == 'POST':
        messages.success(request, 'Boleta creada exitosamente!')
        return redirect('sistemaGestion:lista_boletas')
    
    context = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'rol': request.session.get('rol'),
        'permisos': ROLES_PERMISOS.get(request.session.get('rol'), []),
    }
    return render(request, 'boletas/crear_boleta.html', context)

# Pagos
@requiere_permiso('pagos')
def lista_pagos(request):
    pagos = [
        {'id': 1, 'boleta': 'BOL-002', 'cliente': 'María Rodríguez', 'monto': '32000', 'fecha': '2024-09-05', 'metodo': 'Transferencia'},
    ]
    context = {
        'pagos': pagos,
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'rol': request.session.get('rol'),
        'permisos': ROLES_PERMISOS.get(request.session.get('rol'), []),
    }
    return render(request, 'pagos/lista_pagos.html', context)

@requiere_permiso('pagos')
def crear_pago(request):
    if request.method == 'POST':
        messages.success(request, 'Pago registrado exitosamente!')
        return redirect('sistemaGestion:lista_pagos')
    
    context = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'rol': request.session.get('rol'),
        'permisos': ROLES_PERMISOS.get(request.session.get('rol'), []),
    }
    return render(request, 'pagos/crear_pago.html', context)

@requiere_permiso('contratos')
def detalle_contrato(request, id):
    """Vista para mostrar detalles de un contrato"""
    contrato = {
        'id': id,
        'numero_contrato': 'CTR-001',
        'cliente': 'Juan Pérez González',
        'fecha_inicio': '2024-01-15',
        'fecha_fin': '2025-01-15',
        'estado': 'Activo',
        'tarifa_asociada': 'Residencial Básica'
    }
    
    context = {
        'contrato': contrato,
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'rol': request.session.get('rol'),
        'permisos': ROLES_PERMISOS.get(request.session.get('rol'), []),
    }
    return render(request, 'contratos/detalle_contrato.html', context)

# ============================
# VISTAS PARA TARIFAS
# ============================

@requiere_permiso('tarifas')
def lista_tarifas(request):
    """Vista para listar todas las tarifas"""
    tarifas = [
        {
            'id': 1,
            'tipo_tarifa': 'Residencial Básica',
            'tipo_cliente': 'Residencial',
            'precio': 120.50,
            'fecha_vigencia': '2024-01-01',
            'estado': 'Vigente',
            'contratos_asociados': 150
        },
        {
            'id': 2,
            'tipo_tarifa': 'Comercial Standard',
            'tipo_cliente': 'Comercial',
            'precio': 95.75,
            'fecha_vigencia': '2024-01-01',
            'estado': 'Vigente',
            'contratos_asociados': 89
        }
    ]
    
    context = get_base_context(request)
    context['tarifas'] = tarifas
    return render(request, 'tarifas/lista_tarifas.html', context)

@requiere_permiso('tarifas')
def crear_tarifa(request):
    """Vista para crear una nueva tarifa"""
    if request.method == 'POST':
        messages.success(request, 'Tarifa creada exitosamente!')
        return redirect('sistemaGestion:lista_tarifas')
    
    context = get_base_context(request)
    return render(request, 'tarifas/crear_tarifa.html', context)

@requiere_permiso('tarifas')
def detalle_tarifa(request, id):
    """Vista para mostrar detalles de una tarifa"""
    tarifa = {
        'id': id,
        'tipo_tarifa': 'Residencial Básica',
        'tipo_cliente': 'Residencial',
        'precio': 120.50,
        'fecha_vigencia': '2024-01-01',
        'estado': 'Vigente'
    }
    
    context = {
        'tarifa': tarifa,
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'rol': request.session.get('rol'),
        'permisos': ROLES_PERMISOS.get(request.session.get('rol'), []),
    }
    return render(request, 'tarifas/detalle_tarifa.html', context)

# ============================
# VISTAS PARA MEDIDORES
# ============================

@requiere_permiso('medidores')
def lista_medidores(request):
    """Vista para listar todos los medidores"""
    medidores = [
        {
            'id': 1,
            'numero': 'MED-001',
            'cliente': 'Juan Pérez González',
            'tipo': 'Eléctrico',
            'estado': 'Activo',
            'fecha_instalacion': '2024-01-20',
            'ubicacion': 'Av. Principal 123',
            'ultima_lectura': '2024-09-01'
        },
        {
            'id': 2,
            'numero': 'MED-002',
            'cliente': 'María Rodríguez Silva',
            'tipo': 'Digital',
            'estado': 'Activo',
            'fecha_instalacion': '2024-02-15',
            'ubicacion': 'Calle Los Pinos 456',
            'ultima_lectura': '2024-09-02'
        }
    ]
    
    context = get_base_context(request)
    context['medidores'] = medidores
    return render(request, 'medidores/lista_medidores.html', context)

@requiere_permiso('medidores')
def crear_medidor(request):
    """Vista para crear un nuevo medidor"""
    if request.method == 'POST':
        messages.success(request, 'Medidor creado exitosamente!')
        return redirect('sistemaGestion:lista_medidores')
    
    context = get_base_context(request)
    return render(request, 'medidores/crear_medidor.html', context)

def detalle_medidor(request, id):
    """Vista para mostrar detalles de un medidor"""
    medidor = {
        'id': id,
        'numero_medidor': 'MED-001',
        'contrato': 'CTR-001',
        'fecha_instalacion': '2024-01-20',
        'ubicacion': 'Av. Principal 123',
        'estado_medidor': 'Activo'
    }
    
    context = {'medidor': medidor}
    return render(request, 'medidores/detalle_medidor.html', context)

# ============================
# VISTAS PARA LECTURAS
# ============================

@requiere_permiso('lecturas')
def lista_lecturas(request):
    """Vista para listar todas las lecturas"""
    lecturas = [
        {
            'id': 1,
            'medidor': 'MED-001',
            'fecha_lectura': '2024-09-01',
            'consumo_energetico': 450.5,
            'tipo_lectura': 'Mensual',
            'lectura_actual': 12450,
            'lectura_anterior': 12000,
            'estado': 'Procesada'
        }
    ]
    
    context = get_base_context(request)
    context['lecturas'] = lecturas
    return render(request, 'lecturas/lista_lecturas.html', context)

@requiere_permiso('lecturas')
def crear_lectura(request):
    """Vista para crear una nueva lectura"""
    if request.method == 'POST':
        messages.success(request, 'Lectura registrada exitosamente!')
        return redirect('sistemaGestion:lista_lecturas')
    
    context = get_base_context(request)
    return render(request, 'lecturas/crear_lectura.html', context)

def detalle_lectura(request, id):
    """Vista para mostrar detalles de una lectura"""
    lectura = {
        'id': id,
        'medidor': 'MED-001',
        'fecha_lectura': '2024-09-01',
        'consumo_energetico': 450.5,
        'tipo_lectura': 'Mensual',
        'lectura_actual': 12450,
        'lectura_anterior': 12000
    }
    
    context = {'lectura': lectura}
    return render(request, 'lecturas/detalle_lectura.html', context)

# ============================
# VISTAS PARA BOLETAS
# ============================

@requiere_permiso('boletas')
def lista_boletas(request):
    """Vista para listar gastos eléctricos municipales - Datos de ejemplo para demostración del sistema"""
    boletas = [
        {
            'id': 1,
            'numero_boleta': '452381496',
            'nic': '9168691',
            'cliente_nombre': 'BIBLIOTECA (GERONIMO GODOY)',
            'gestion': 1,
            'codigo_interno': '2',
            'consumo_kwh': 102,
            'monto_total': 28400,
            'fecha_emision': '2025-06-17',
            'hora_emision': '09:30',
            'fecha_vencimiento': '2025-07-22',
            'periodo_facturacion': 'Junio 2025',
            'estado': 'Pendiente',
            'dias_vencimiento': 10
        },
        {
            'id': 2,
            'numero_boleta': '452337837',
            'nic': '9168691',
            'cliente_nombre': 'BIBLIOTECA (GERONIMO GODOY)',
            'gestion': 1,
            'codigo_interno': '2',
            'consumo_kwh': 80,
            'monto_total': 23600,
            'fecha_emision': '2025-06-17',
            'hora_emision': '09:35',
            'fecha_vencimiento': '2025-07-22',
            'periodo_facturacion': 'Junio 2025',
            'estado': 'Pagada',
            'dias_vencimiento': 10
        },
        {
            'id': 3,
            'numero_boleta': '452406606',
            'nic': '9255389',
            'cliente_nombre': 'LOS PERALES',
            'gestion': 1,
            'codigo_interno': '3',
            'consumo_kwh': 0,
            'monto_total': 1000,
            'fecha_emision': '2025-06-17',
            'hora_emision': '09:40',
            'fecha_vencimiento': '2025-07-22',
            'periodo_facturacion': 'Junio 2025',
            'estado': 'Pendiente',
            'dias_vencimiento': 10
        },
        {
            'id': 4,
            'numero_boleta': '451893413',
            'nic': '9351251',
            'cliente_nombre': 'ANTONIA FAJARDO (VETERINARIO)',
            'gestion': 1,
            'codigo_interno': '40',
            'consumo_kwh': 73,
            'monto_total': 21500,
            'fecha_emision': '2025-06-17',
            'hora_emision': '09:45',
            'fecha_vencimiento': '2025-07-22',
            'periodo_facturacion': 'Junio 2025',
            'estado': 'Pagada',
            'dias_vencimiento': 10
        },
        {
            'id': 5,
            'numero_boleta': '452321237',
            'nic': '9352282',
            'cliente_nombre': 'P. ALONSO GARCIA S/N EX RENE CORTES P',
            'gestion': 1,
            'codigo_interno': '157',
            'consumo_kwh': 76,
            'monto_total': 22600,
            'fecha_emision': '2025-06-17',
            'hora_emision': '09:50',
            'fecha_vencimiento': '2025-07-22',
            'periodo_facturacion': 'Junio 2025',
            'estado': 'Pagada',
            'dias_vencimiento': 10
        },
        {
            'id': 6,
            'numero_boleta': '452363943',
            'nic': '9354332',
            'cliente_nombre': 'MULTICANCHA J. GODOY',
            'gestion': 1,
            'codigo_interno': '5',
            'consumo_kwh': 161,
            'monto_total': 45600,
            'fecha_emision': '2025-06-17',
            'hora_emision': '09:55',
            'fecha_vencimiento': '2025-07-22',
            'periodo_facturacion': 'Junio 2025',
            'estado': 'Pendiente',
            'dias_vencimiento': 10
        },
        {
            'id': 7,
            'numero_boleta': '452347671',
            'nic': '9364004',
            'cliente_nombre': 'CENTRAL DE SERVICIOS',
            'gestion': 1,
            'codigo_interno': '47',
            'consumo_kwh': 1115,
            'monto_total': 284000,
            'fecha_emision': '2025-06-17',
            'hora_emision': '10:00',
            'fecha_vencimiento': '2025-07-22',
            'periodo_facturacion': 'Junio 2025',
            'estado': 'Pendiente',
            'dias_vencimiento': 10
        }

    ]
    
    # Calcular estadísticas (enfoque de gastos municipales)
    total_servicios = len(boletas)
    servicios_pagados = len([b for b in boletas if b['estado'] == 'Pagada'])
    servicios_pendientes = len([b for b in boletas if b['estado'] == 'Pendiente'])
    servicios_vencidos = len([b for b in boletas if b['estado'] == 'Vencida'])
    
    total_gasto_presupuestado = sum(b['monto_total'] for b in boletas)
    total_pagado = sum(b['monto_total'] for b in boletas if b['estado'] == 'Pagada')
    total_por_pagar = total_gasto_presupuestado - total_pagado
    porcentaje_pagado = (total_pagado / total_gasto_presupuestado * 100) if total_gasto_presupuestado > 0 else 0
    
    context = get_base_context(request)
    context.update({
        'boletas': boletas,
        'total_servicios': total_servicios,
        'servicios_pagados': servicios_pagados,
        'servicios_pendientes': servicios_pendientes,
        'servicios_vencidos': servicios_vencidos,
        'total_gasto_presupuestado': total_gasto_presupuestado,
        'total_pagado': total_pagado,
        'total_por_pagar': total_por_pagar,
        'porcentaje_pagado': porcentaje_pagado
    })
    return render(request, 'boletas/lista_boletas.html', context)

@requiere_permiso('boletas')
def crear_boleta(request):
    """Vista para crear una nueva boleta"""
    if request.method == 'POST':
        messages.success(request, 'Boleta creada exitosamente!')
        return redirect('sistemaGestion:lista_boletas')
    
    context = get_base_context(request)
    return render(request, 'boletas/crear_boleta.html', context)

def detalle_boleta(request, id):
    """Vista para mostrar detalles de una boleta"""
    boleta = {
        'id': id,
        'numero_boleta': 'BOL-001',
        'lectura': 'LEC-001',
        'cliente': 'Juan Pérez González',
        'fecha_emision': '2024-09-05',
        'fecha_vencimiento': '2024-10-05',
        'monto_total': 54260,
        'consumo_energetico': 450.5,
        'estado': 'Emitida'
    }
    
    context = {'boleta': boleta}
    return render(request, 'boletas/detalle_boleta.html', context)

# ============================
# VISTAS PARA PAGOS
# ============================

@requiere_permiso('pagos')
def lista_pagos(request):
    """Vista para listar todos los pagos"""
    pagos = [
        {
            'id': 1,
            'numero_pago': 'PAG-001',
            'boleta': 'BOL-001',
            'cliente': 'Juan Pérez González',
            'fecha_pago': '2024-09-15',
            'monto_pagado': 54260,
            'metodo_pago': 'Transferencia',
            'numero_referencia': 'TRF-123456',
            'estado_pago': 'Completado'
        }
    ]
    
    context = get_base_context(request)
    context['pagos'] = pagos
    return render(request, 'pagos/lista_pagos.html', context)

@requiere_permiso('pagos')
def crear_pago(request):
    """Vista para crear un nuevo pago"""
    if request.method == 'POST':
        messages.success(request, 'Pago registrado exitosamente!')
        return redirect('sistemaGestion:lista_pagos')
    
    context = get_base_context(request)
    return render(request, 'pagos/crear_pago.html', context)

def detalle_pago(request, id):
    """Vista para mostrar detalles de un pago"""
    pago = {
        'id': id,
        'numero_pago': 'PAG-001',
        'boleta': 'BOL-001',
        'fecha_pago': '2024-09-15',
        'monto_pagado': 54260,
        'metodo_pago': 'Transferencia',
        'numero_referencia': 'TRF-123456',
        'estado_pago': 'Completado'
    }
    
    context = {'pago': pago}
    return render(request, 'pagos/detalle_pago.html', context)

# ============================
# VISTAS PARA USUARIOS
# ============================

@requiere_permiso('usuarios')
@requiere_permiso('usuarios')
def lista_usuarios(request):
    """Vista para listar todos los usuarios"""
    usuarios = [
        {
            'id': 1,
            'nombre': 'Admin Principal',
            'email': 'admin@sistemaelectrico.com',
            'telefono': '+56912345678',
            'rol': 'administrador',
            'estado': 'Activo',
            'ultimo_acceso': '2024-09-06 08:30'
        },
        {
            'id': 2,
            'nombre': 'Juan Eléctrico',
            'email': 'juan@sistemaelectrico.com',
            'telefono': '+56987654321',
            'rol': 'electrico',
            'estado': 'Activo',
            'ultimo_acceso': '2024-09-05 14:15'
        },
        {
            'id': 3,
            'nombre': 'María Finanzas',
            'email': 'maria@sistemaelectrico.com',
            'telefono': '+56911223344',
            'rol': 'finanzas',
            'estado': 'Activo',
            'ultimo_acceso': '2024-09-04 10:45'
        },
        {
            'id': 4,
            'nombre': 'Carlos Admin',
            'email': 'carlos@sistemaelectrico.com',
            'telefono': '+56933445566',
            'rol': 'administrador',
            'estado': 'Inactivo',
            'ultimo_acceso': '2024-08-30 16:20'
        }
    ]
    
    context = get_base_context(request)
    context['usuarios'] = usuarios
    return render(request, 'usuarios/lista_usuarios.html', context)

@requiere_permiso('usuarios')
def crear_usuario(request):
    """Vista para crear un nuevo usuario"""
    if request.method == 'POST':
        messages.success(request, 'Usuario creado exitosamente!')
        return redirect('sistemaGestion:lista_usuarios')
    
    context = get_base_context(request)
    return render(request, 'usuarios/crear_usuario.html', context)

def detalle_usuario(request, id):
    """Vista para mostrar detalles de un usuario"""
    usuario = {
        'id': id,
        'nombre': 'Admin Principal',
        'email': 'admin@sistemaelectrico.com',
        'telefono': '+56912345678',
        'rol': 'administrador',
        'estado': 'Activo',
        'fecha_creacion': '2024-01-01',
        'ultimo_acceso': '2024-09-06 08:30'
    }
    
    context = {'usuario': usuario}
    return render(request, 'usuarios/detalle_usuario.html', context)

# ============================
# VISTAS PARA NOTIFICACIONES
# ============================

@requiere_permiso('notificaciones')
@requiere_login
def lista_notificaciones(request):
    """Vista para listar todas las notificaciones"""
    notificaciones = [
        {
            'id': 1,
            'tipo': 'Lectura',
            'titulo': 'Consumo Alto Detectado',
            'mensaje': 'El cliente Juan Pérez ha superado el consumo promedio en un 150%',
            'fecha_creacion': '2024-09-06 09:00',
            'estado': 'Pendiente',
            'prioridad': 'Alta'
        }
    ]
    
    context = get_base_context(request)
    context['notificaciones'] = notificaciones
    return render(request, 'notificaciones/lista_notificaciones.html', context)

@requiere_permiso('notificaciones')
def crear_notificacion(request):
    """Vista para crear una nueva notificación"""
    if request.method == 'POST':
        messages.success(request, 'Notificación creada exitosamente!')
        return redirect('sistemaGestion:lista_notificaciones')
    
    context = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'rol': request.session.get('rol'),
        'permisos': ROLES_PERMISOS.get(request.session.get('rol'), []),
    }
    return render(request, 'notificaciones/crear_notificacion.html', context)

@requiere_permiso('notificaciones')
def detalle_notificacion(request, id):
    """Vista para mostrar detalles de una notificación"""
    notificacion = {
        'id': id,
        'tipo': 'Lectura',
        'titulo': 'Consumo Alto Detectado',
        'mensaje': 'El cliente Juan Pérez ha superado el consumo promedio en un 150%',
        'fecha_creacion': '2024-09-06 09:00',
        'estado': 'Pendiente',
        'prioridad': 'Alta'
    }
    
    context = {'notificacion': notificacion}
    return render(request, 'notificaciones/detalle_notificacion.html', context)

