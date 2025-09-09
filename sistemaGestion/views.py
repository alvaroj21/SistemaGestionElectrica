from django.shortcuts import render, redirect
from django.contrib import messages

# ============================
# DATOS DE CONFIGURACIÓN DEL SISTEMA
# ============================

# Usuarios del sistema con sus credenciales y roles.
USUARIOS = {
    'admin': {'password': 'admin123', 'rol': 'admin', 'nombre': 'Administrador'},
    'prueba': {'password': '1234', 'rol': 'admin', 'nombre': 'Alvaro Pinto - Administrador'},
    'electrico1': {'password': 'elec123', 'rol': 'electrico', 'nombre': 'Juan Pérez - Eléctrico'},
    'finanzas1': {'password': 'fin123', 'rol': 'finanzas', 'nombre': 'María García - Finanzas'},
}

# Definición de permisos por rol
# Determina qué módulos puede acceder cada tipo de usuario
# - admin: acceso completo a todos los módulos
# - electrico: solo medidores, lecturas y notificaciones
# - finanzas: clientes, contratos, tarifas, boletas, pagos y notificaciones
PERMISOS_ROL = {
    'admin': ['medidores', 'lecturas', 'clientes', 'contratos', 'tarifas', 'boletas', 'pagos', 'usuarios', 'notificaciones'],
    'electrico': ['medidores', 'lecturas', 'notificaciones'],
    'finanzas': ['clientes', 'contratos', 'tarifas', 'boletas', 'pagos', 'notificaciones'],
}

# ============================
# VISTAS PARA LOGIN Y LOGOUT
# ============================

def usuario_logueado(request):
    return request.session.get('user_logged', False)

def tiene_permiso(request, modulo):
    if not usuario_logueado(request):
        return False
    
    rol = request.session.get('rol', '')
    permisos = PERMISOS_ROL.get(rol, [])
    return modulo in permisos

def login_view(request):
    # Si ya está logueado, ir al dashboard
    if usuario_logueado(request):
        return redirect('sistemaGestion:dashboard')
    
    # Si es un formulario enviado (POST)
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Verificar si el usuario existe y la contraseña es correcta
        if username in USUARIOS and USUARIOS[username]['password'] == password:
            # Guardar datos del usuario en la sesión
            request.session['user_logged'] = True
            request.session['username'] = username
            request.session['rol'] = USUARIOS[username]['rol']
            request.session['nombre'] = USUARIOS[username]['nombre']
            
            messages.success(request, f'Bienvenido {USUARIOS[username]["nombre"]}')
            return redirect('sistemaGestion:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    # Mostrar la página de login
    return render(request, 'auth/login.html')

def logout_view(request):
    # Limpiar toda la sesión
    request.session.flush()
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('sistemaGestion:login')

# ============================
# VISTAS PARA DASHBOARD PRINCIPAL
# ============================

def dashboard(request):
    # Verificar si está logueado
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
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
    
    Args:
        request: Objeto HttpRequest de Django
    
    Returns:
        HttpResponse: Redirige al dashboard
    """
    return redirect('sistemaGestion:dashboard')

# ============================
# VISTAS PARA GESTIÓN DE CLIENTES
# ============================

def lista_clientes(request):
    # Verificar login
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'clientes'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de clientes de ejemplo
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
    
    # Datos para el template
    datos = {
        'clientes': clientes
    }
    return render(request, 'clientes/lista_clientes.html', datos)

def crear_cliente(request):
    # Verificar login
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'clientes'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    # Datos para el template
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre')
    }
    return render(request, 'clientes/crear_cliente.html', datos)

# ============================
# VISTAS PARA GESTIÓN DE CONTRATOS
# ============================

def lista_contratos(request):
    # Verificar login
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'contratos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de contratos de ejemplo
    contratos = [
        {
            'idContrato': 1, 
            'numero_contrato': 'CON-001', 
            'fecha_inicio': '21-05-2025', 
            'fecha_fin': '21-09-2025', 
            'estado': 'Activo',
            'cliente_nombre': 'Juan Pérez'
        },
        {
            'idContrato': 2, 
            'numero_contrato': 'CON-002', 
            'fecha_inicio': '21-05-2025', 
            'fecha_fin': '21-09-2025', 
            'estado': 'Activo',
            'cliente_nombre': 'María Rodríguez'  
        },
        {
            'idContrato': 3, 
            'numero_contrato': 'CON-003', 
            'fecha_inicio': '21-05-2025', 
            'fecha_fin': '21-09-2025', 
            'estado': 'Vencido',
            'cliente_nombre': 'Carlos Sánchez'  
        },
    ]
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'contratos': contratos
    }
    return render(request, 'contratos/lista_contratos.html', datos)

def crear_contrato(request):
    # Verificar login
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'contratos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de clientes para el select
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
    
    # Lista de tarifas para el select
    tarifas = [
        {
            'tipo_tarifa': 'Invierno',
            'tipo_cliente': 'Residencial',
        },
        {
            'tipo_tarifa': 'Invierno',
            'tipo_cliente': 'Comercial',
        },
        {
            'tipo_tarifa': 'Invierno',
            'tipo_cliente': 'Industrial',
        }
    ]
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'clientes': clientes,
        'tarifas': tarifas
    }
    return render(request, 'contratos/crear_contrato.html', datos)

# ============================
# VISTAS PARA GESTIÓN DE MEDIDORES
# ============================

def lista_medidores(request):
    # Verificar login
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
            'fecha_instalacion': '2021-01-15',
            'ubicacion': 'Calle Principal 123, Casa Juan Pérez',
            'estado_medidor': 'Activo',
            'cliente_nombre': 'Juan Perez'  # Para mostrar en template, borrar luego 
        },
        {
            'id_medidor': 2, 
            'numero_medidor': 'MED-002', 
            'fecha_instalacion': '2021-03-20',
            'ubicacion': 'Av. Comercial 456, Local María Rodríguez',
            'estado_medidor': 'Activo',
            'cliente_nombre': 'Maria Rodríguez'  
        },
        {
            'id_medidor': 3, 
            'numero_medidor': 'MED-003', 
            'fecha_instalacion': '2023-12-01',
            'ubicacion': 'Barrio Industrial 789, Empresa Carlos Sánchez',
            'estado_medidor': 'Mantenimiento',
            'cliente_nombre': 'Carlos Castillo'  
        },
    ]
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'medidores': medidores
    }
    return render(request, 'medidores/lista_medidores.html', datos)

def crear_medidor(request):
    # Verificar login
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'medidores'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de clientes para el select
    clientes = [
        {
            'idCliente': 1,
            'nombre': 'Juan Pérez', 
            'email': 'juan@email.com', 
            'telefono': '123456789', 
            'numero_cliente': 'CL-001'
        },
        {
            'idCliente': 2,
            'nombre': 'María Rodríguez', 
            'email': 'maria@email.com', 
            'telefono': '987654321', 
            'numero_cliente': 'CL-002'
        },
        {
            'idCliente': 3,
            'nombre': 'Carlos Sánchez', 
            'email': 'carlos@email.com', 
            'telefono': '111222333', 
            'numero_cliente': 'CL-003'
        },
        {
            'idCliente': 4,
            'nombre': 'Ana Gomez', 
            'email': 'ana@email.com', 
            'telefono': '14262333', 
            'numero_cliente': 'CL-004'
        },
    ]
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'clientes': clientes
    }
    return render(request, 'medidores/crear_medidor.html', datos)

def ubicacion_medidor(request, id_medidor):
    # Verificar login
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'medidores'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Datos simulados del medidor
    medidor = {
        'id_medidor': id_medidor,
        'numero_medidor': f'MED-{str(id_medidor).zfill(3)}',
        'cliente_nombre': 'Cliente Simulado',
        'ubicacion': 'Ubicación de Prueba - Sistema de Gestión Eléctrica',
        'direccion': 'Calle Principal 123, Ciudad Ejemplo',
        'estado_medidor': 'Activo',
        'fecha_instalacion': '2024-01-15'
    }
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'medidor': medidor
    }
    return render(request, 'medidores/ubicacion_medidor.html', datos)

# ============================
# VISTAS PARA GESTIÓN DE LECTURAS
# ============================

def lista_lecturas(request):
    # Verificar login
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'lecturas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de lecturas de ejemplo con cálculos de consumo
    lecturas = [
        {
            'id_lectura': 1, 
            'fecha_lectura': '01-09-2025', 
            'consumo_energetico': 125,  # Calculado: lectura_actual - lectura_anterior
            'tipo_lectura': 'Manual',
            'lectura_actual': 1250,
            'medidor_numero': 'MED-001'  # Para mostrar en template
        },
        {
            'id_lectura': 2, 
            'fecha_lectura': '01-09-2025', 
            'consumo_energetico': 98,   # Calculado: lectura_actual - lectura_anterior
            'tipo_lectura': 'Automatica',
            'lectura_actual': 980,
            'medidor_numero': 'MED-002'  # Para mostrar en template
        },
        {
            'id_lectura': 3, 
            'fecha_lectura': '01-08-2025', 
            'consumo_energetico': 156,
            'tipo_lectura': 'Manual',
            'lectura_actual': 1125,
            'medidor_numero': 'MED-001'  # Para mostrar en template
        },
    ]
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'lecturas': lecturas
    }
    return render(request, 'lecturas/lista_lecturas.html', datos)

def crear_lectura(request):
    # Verificar login
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'lecturas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')

    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre')
    }
    return render(request, 'lecturas/crear_lectura.html', datos)

# ============================
# VISTAS PARA GESTIÓN DE BOLETAS
# ============================

def lista_boletas(request):
    # Verificar login
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'boletas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de boletas de ejemplo con información completa de facturación
    
    boletas = [
        {
            'id_boleta': 1,
            'fecha_emision': '17-09-2025',
            'fecha_vencimiento': '22-10-2025',
            'monto_total': 28400,                       # Monto total en pesos
            'consumo_energetico': 125,                  # Consumo en kWh
            'estado': 'Pendiente',
            'cliente_nombre': 'Juan Pérez'  # Para mostrar en template
        },
        {
            'id_boleta': 2,
            'fecha_emision': '17-09-2025',
            'fecha_vencimiento': '22-10-2025',
            'monto_total': 23600,
            'consumo_energetico': 98,
            'estado': 'Pagada',
            'cliente_nombre': 'María Rodríguez'  # Para mostrar en template
        },
        {
            'id_boleta': 3,
            'fecha_emision': '17-07-2025',
            'fecha_vencimiento': '22-08-2025',
            'monto_total': 35200,
            'consumo_energetico': 156,
            'estado': 'Vencida',
            'cliente_nombre': 'Juan Pérez'  # Para mostrar en template
        },
    ]

    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'boletas': boletas
    }
    return render(request, 'boletas/lista_boletas.html', datos)
    
def crear_boleta(request):
    # Verificar login
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'boletas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')

    clientes = [
        {'id': 1, 'nombre': 'Juan Pérez', 'email': 'juan@email.com', 'telefono': '123456789', 'estado': 'Activo'},
        {'id': 2, 'nombre': 'María Rodríguez', 'email': 'maria@email.com', 'telefono': '987654321', 'estado': 'Activo'},
        {'id': 3, 'nombre': 'Carlos Sánchez', 'email': 'carlos@email.com', 'telefono': '111222333', 'estado': 'Inactivo'},
        {'id': 4, 'nombre': 'Ana Gomez', 'email': 'ana@email.com', 'telefono': '14262333', 'estado': 'Activo'},
    ]
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'clientes': clientes
    }
    return render(request, 'boletas/crear_boleta.html', datos)

# ============================
# VISTAS PARA GESTIÓN DE PAGOS
# ============================

def lista_pagos(request):
    # Verificar login
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'pagos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de pagos registrados

    pagos = [
        {
            'idpago': 1,
            'fecha_pago': '2024-09-20',
            'monto_pagado': 23600,                      # Monto en pesos
            'metodo_pago': 'Transferencia Bancaria',    # Método de pago utilizado
            'numero_referencia': 'TRF001',             # Referencia de la transacción
            'estado_pago': 'Confirmado',               # Estado del pago
            'cliente_nombre': 'María Rodríguez'  # Para mostrar en template
        },
        {
            'idpago': 2,
            'fecha_pago': '2024-08-15',
            'monto_pagado': 31500,
            'metodo_pago': 'Efectivo',
            'numero_referencia': 'EFE001',
            'estado_pago': 'Confirmado',
            'cliente_nombre': 'Juan Pérez'  # Para mostrar en template
        },
        {
            'idpago': 3,
            'fecha_pago': '2024-09-01',
            'monto_pagado': 15000,
            'metodo_pago': 'Tarjeta de Crédito',
            'numero_referencia': 'TDC001',
            'estado_pago': 'Pendiente',
            'cliente_nombre': 'Carlos Mendoza'  # Para mostrar en template
        },
    ]
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'pagos': pagos
    }
    return render(request, 'pagos/lista_pagos.html', datos)

def crear_pago(request):
    # Verificar login
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'pagos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre')
    }
    return render(request, 'pagos/crear_pago.html', datos)

# ============================
# VISTAS PARA GESTIÓN DE TARIFAS
# ============================

def lista_tarifas(request):
    # Verificar login
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'tarifas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Lista de tarifas
    tarifas = [
        {
            'id_tarifa': 1,
            'tipo_tarifa': 'Invierno',
            'tipo_cliente': 'Residencial',
            'precio': 120,                           
            'fecha_vigencia': '09-09-2025'
        },
        {
            'id_tarifa': 2,
            'tipo_tarifa': 'Invierno',
            'tipo_cliente': 'Comercial',
            'precio': 95,                            
            'fecha_vigencia': '09-09-2025'
        },
        {
            'id_tarifa': 3,
            'tipo_tarifa': 'Invierno',
            'tipo_cliente': 'Industrial',
            'precio': 85,                            
            'fecha_vigencia': '09-09-2025'
        }
    ]
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'tarifas': tarifas
    }
    return render(request, 'tarifas/lista_tarifas.html', datos)

def crear_tarifa(request):
    # Verificar login
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'tarifas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')

    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre')
    }
    return render(request, 'tarifas/crear_tarifa.html', datos)

# ============================
# VISTAS PARA GESTIÓN DE USUARIOS
# ============================

def lista_usuarios(request):
    # Verificar login
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'usuarios'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    usuarios = [
        {
            'idUsuario': 1,
            'nombreUsuario': 'electrico1',
            'nombre': 'Juan Eléctrico',
            'email': 'juan@sistemaelectrico.com',
            'telefono': '+56987654321',
            'rol': 'electrico',                         # Rol que determina permisos
            'estado': 'Activo',                         # Estado del usuario (campo adicional para template)
            'ultimo_acceso': '2024-09-06 14:30'        # Última vez que ingresó al sistema (campo adicional)
        },
        {
            'idUsuario': 2,
            'nombreUsuario': 'admin',
            'nombre': 'Admin Sistema',
            'email': 'admin@sistemaelectrico.com',
            'telefono': '+56912345678',
            'rol': 'admin',
            'estado': 'Activo',
            'ultimo_acceso': '2024-09-06 08:15'
        },
        {
            'idUsuario': 3,
            'nombreUsuario': 'finanzas1',
            'nombre': 'Ana Finanzas',
            'email': 'ana@sistemaelectrico.com',
            'telefono': '+56923456789',
            'rol': 'finanzas',
            'estado': 'Activo',
            'ultimo_acceso': '2024-09-05 16:45'
        },
    ]
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'usuarios': usuarios
    }
    return render(request, 'usuarios/lista_usuarios.html', datos)

def crear_usuario(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    # Verificar permisos
    if not tiene_permiso(request, 'usuarios'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre')
    }
    return render(request, 'usuarios/crear_usuario.html', datos)

# ============================
# VISTAS PARA SISTEMA DE NOTIFICACIONES
# ============================

def lista_notificaciones(request):
    """
    Vista que muestra las notificaciones del sistema.
    Args:
        request: Objeto HttpRequest de Django
    
    Returns:
        HttpResponse: Renderiza lista_notificaciones.html con notificaciones
    """
    # Verificar login
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
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'notificaciones': notificaciones
    }
    return render(request, 'notificaciones/lista_notificaciones.html', datos)
