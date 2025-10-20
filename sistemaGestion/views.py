"""
Este módulo contiene todas las vistas del sistema de gestión eléctrica desarrollado en Django.
El sistema permite gestionar clientes, contratos, medidores, lecturas, boletas, pagos, tarifas,
usuarios y notificaciones con un sistema de autenticación por roles.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Cliente, Contrato, Tarifa, Medidor, Lectura, Boleta, Pago, Usuario, NotificacionPago, NotificacionLectura
from .forms import ClienteForm, ContratoForm, MedidorForm, LecturaForm, BoletaForm, PagoForm, TarifaForm, UsuarioForm, NotificacionLecturaForm, NotificacionPagoForm


# ============================================================================
# CONFIGURACIÓN DEL SISTEMA
# ============================================================================

# Diccionario que define qué módulos puede acceder cada rol de usuario
PERMISOS_ROL = {
    'Administrador': ['medidores', 'lecturas', 'clientes', 'contratos', 'tarifas', 'boletas', 'pagos', 'usuarios', 'notificaciones'],
    'Eléctrico': ['medidores', 'lecturas', 'notificaciones'],
    'Finanzas': ['clientes', 'contratos', 'tarifas', 'boletas', 'pagos', 'notificaciones'],
}


# ============================================================================
# FUNCIONES AUXILIARES DE AUTENTICACIÓN Y PAGINACIÓN
# ============================================================================

def usuario_logueado(request):
    return request.session.get('user_logged', False)

def tiene_permiso(request, modulo):
    if not usuario_logueado(request):
        return False
    rol = request.session.get('rol', '')
    permisos = PERMISOS_ROL.get(rol, [])
    return modulo in permisos

#esto permite paginar los objetos en las vistas
#es decir, dividir la lista de objetos en varias paginas
def paginar_objetos(request, objetos, elementos_por_pagina=5):
    """
    Función auxiliar para paginar objetos
    """
    paginator = Paginator(objetos, elementos_por_pagina)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


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
    
    # Obtener estadísticas clave para el dashboard
    datos = {
        'total_clientes': Cliente.objects.count(),
        'total_contratos': Contrato.objects.count(),
        'total_medidores': Medidor.objects.count(),
        'lecturas_pendientes': Lectura.objects.count(), 
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
    
    # Obtener todos los clientes inicialmente 
    clientes = Cliente.objects.all()
    
    # Filtros de búsqueda para los clientes en la lista_clientes.html
    search_numero = request.GET.get('numero_cliente', '')
    search_nombre = request.GET.get('nombre', '')
    search_email = request.GET.get('email', '')
    search_telefono = request.GET.get('telefono', '')
    
    # Aplicar filtros si existen los parámetros de búsqueda
    if search_numero:
        clientes = clientes.filter(numero_cliente__icontains=search_numero)
    if search_nombre:
        clientes = clientes.filter(nombre__icontains=search_nombre)
    if search_email:
        clientes = clientes.filter(email__icontains=search_email)
    if search_telefono:
        clientes = clientes.filter(telefono__icontains=search_telefono)
    
    # Ordenar los resultados por número de cliente
    clientes = clientes.order_by('numero_cliente')
    page_obj = paginar_objetos(request, clientes,)
    
    #en datos se pasa el username quien esta logueado el nombre de la persona que esta logueada
    #los clientes usando la paginacion, la pagina actual y los filtros de busqueda aplicados
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'clientes': page_obj,
        'page_obj': page_obj,
        'search_numero': search_numero,
        'search_nombre': search_nombre,
        'search_email': search_email,
        'search_telefono': search_telefono,
    }
    return render(request, 'clientes/lista_clientes.html', datos)

def crear_cliente(request):
    # Verificar autenticación
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'clientes'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Procesar formulario de creación de cliente
    # Si es POST, validar y guardar el cliente
    #(post es cuando se envía el formulario)
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            # Guardar el cliente
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nombre}" creado exitosamente con número {cliente.numero_cliente}')
            return redirect('sistemaGestion:lista_clientes')
    else:
        # generar un formulario vacío
        form = ClienteForm()
    
    # Preparar datos para el template
    #se pasan el username quien esta logueado el nombre de la persona que esta logueada
    #y el formulario para crear un cliente
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'form': form
    }
    return render(request, 'clientes/crear_cliente.html', datos)

#editar cliente ocupa el mismo formulario que crear cliente
#solo que se carga con la información del cliente a editar, esto se hace con el parámetro instance
#el cual recibe el objeto cliente a editar como instancia
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
    #se pasan el username quien esta logueado el nombre de la persona que esta logueada
    #el formulario con la información del cliente a editar y el cliente, es decir
    #el objeto cliente con los datos actuales
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'form': form,
        'cliente': cliente
    }
    return render(request, 'clientes/editar_cliente.html', datos)

#eliminar cliente
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
        cliente.delete() #elimina el cliente de la base de datos
        messages.success(request, f'Cliente "{nombre_cliente}" eliminado exitosamente')
        return redirect('sistemaGestion:lista_clientes')
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'cliente': cliente
    }
    return render(request, 'clientes/eliminar_cliente.html', datos)

#detalle cliente muestra la información detallada de un cliente
#es similar a editar cliente pero sin el formulario y sin instance ya que no se edita
#solo se muestra la información
def detalle_cliente(request, cliente_id):
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
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'cliente': cliente
    }
    return render(request, 'clientes/detalle_cliente.html', datos)


# ============================================================================
# VISTAS PARA GESTIÓN DE CONTRATOS
# ============================================================================

def lista_contratos(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'contratos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Obtener todos los contratos inicialmente
    contratos = Contrato.objects.all()
    
    # Filtros de búsqueda
    search_numero = request.GET.get('numero_contrato', '')
    search_estado = request.GET.get('estado', '')
    search_fecha_inicio = request.GET.get('fecha_inicio', '')
    search_fecha_fin = request.GET.get('fecha_fin', '')
    
    # Aplicar filtros si existen
    if search_numero:
        contratos = contratos.filter(numero_contrato__icontains=search_numero)
    if search_estado:
        contratos = contratos.filter(estado__icontains=search_estado)
    if search_fecha_inicio:
        contratos = contratos.filter(fecha_inicio__gte=search_fecha_inicio)
    if search_fecha_fin:
        contratos = contratos.filter(fecha_fin__lte=search_fecha_fin)
    
    # Ordenar los resultados por número de contrato
    contratos = contratos.order_by('numero_contrato')
    page_obj = paginar_objetos(request, contratos)
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'contratos': page_obj,
        'page_obj': page_obj,
        'search_numero': search_numero,
        'search_estado': search_estado,
        'search_fecha_inicio': search_fecha_inicio,
        'search_fecha_fin': search_fecha_fin,
    }
    return render(request, 'contratos/lista_contratos.html', datos)

#crear contrato
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

#editar contrato
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

#eliminar contrato
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

#detalle contrato
def detalle_contrato(request, contrato_id):
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
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'contrato': contrato
    }
    return render(request, 'contratos/detalle_contrato.html', datos)


# ============================================================================
# VISTAS PARA GESTIÓN DE MEDIDORES
# ============================================================================

def lista_medidores(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'medidores'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Obtener todos los medidores inicialmente
    medidores = Medidor.objects.all()
    
    # Filtros de búsqueda
    search_numero = request.GET.get('numero_medidor', '')
    search_ubicacion = request.GET.get('ubicacion', '')
    search_estado = request.GET.get('estado_medidor', '')
    search_fecha = request.GET.get('fecha_instalacion', '')
    
    # Aplicar filtros si existen
    if search_numero:
        medidores = medidores.filter(numero_medidor__icontains=search_numero)
    if search_ubicacion:
        medidores = medidores.filter(ubicacion__icontains=search_ubicacion)
    if search_estado:
        medidores = medidores.filter(estado_medidor__icontains=search_estado)
    if search_fecha:
        medidores = medidores.filter(fecha_instalacion__gte=search_fecha)
    
    # Ordenar los resultados
    medidores = medidores.order_by('numero_medidor')
    page_obj = paginar_objetos(request, medidores)
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'medidores': page_obj,
        'page_obj': page_obj,
        'search_numero': search_numero,
        'search_ubicacion': search_ubicacion,
        'search_estado': search_estado,
        'search_fecha': search_fecha,
    }
    return render(request, 'medidores/lista_medidores.html', datos)

#crear medidor
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

#editar medidor
def editar_medidor(request, medidor_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    if not tiene_permiso(request, 'medidores'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        medidor = Medidor.objects.get(id=medidor_id)
    except Medidor.DoesNotExist:
        messages.error(request, 'El medidor no existe')
        return redirect('sistemaGestion:lista_medidores')

    if request.method == 'POST':
        form = MedidorForm(request.POST, instance=medidor)
        if form.is_valid():
            medidor_actualizado = form.save()
            messages.success(request, f'Medidor "{medidor_actualizado.numero_medidor}" actualizado exitosamente')
            return redirect('sistemaGestion:lista_medidores')
    else:
        form = MedidorForm(instance=medidor)

    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'form': form,
        'medidor': medidor
    }
    return render(request, 'medidores/editar_medidor.html', datos)

#eliminar medidor
def eliminar_medidor(request, medidor_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')

    if not tiene_permiso(request, 'medidores'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        medidor = Medidor.objects.get(id=medidor_id)
    except Medidor.DoesNotExist:
        messages.error(request, 'El medidor no existe')
        return redirect('sistemaGestion:lista_medidores')
    if request.method == 'POST':
        numero_medidor = medidor.numero_medidor
        medidor.delete()
        messages.success(request, f'Medidor "{numero_medidor}" eliminado exitosamente')
        return redirect('sistemaGestion:lista_medidores')
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'medidor': medidor
    }
    return render(request, 'medidores/eliminar_medidor.html', datos)

#detalle medidor
def detalle_medidor(request, medidor_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')

    if not tiene_permiso(request, 'medidores'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        medidor = Medidor.objects.get(id=medidor_id)
    except Medidor.DoesNotExist:
        messages.error(request, 'El medidor no existe')
        return redirect('sistemaGestion:lista_medidores')
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'medidor': medidor
    }
    return render(request, 'medidores/detalle_medidor.html', datos)

#ubicacion medidor muestra la ubicación e información completa del medidor con imágenes
#similar a detalle medidor pero con más información mas la ubicación tanto en texto como en mapa
def ubicacion_medidor(request, medidor_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')

    if not tiene_permiso(request, 'medidores'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        medidor = Medidor.objects.get(id=medidor_id)
    except Medidor.DoesNotExist:
        messages.error(request, 'El medidor no existe')
        return redirect('sistemaGestion:lista_medidores')
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'medidor': medidor,
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
    
    # Obtener todas las lecturas inicialmente
    lecturas = Lectura.objects.all()
    
    # Filtros de búsqueda
    search_fecha = request.GET.get('fecha_lectura', '')
    search_tipo = request.GET.get('tipo_lectura', '')
    search_consumo_min = request.GET.get('consumo_min', '')
    search_consumo_max = request.GET.get('consumo_max', '')
    
    # Aplicar filtros si existen
    if search_fecha:
        lecturas = lecturas.filter(fecha_lectura__gte=search_fecha)
    if search_tipo:
        lecturas = lecturas.filter(tipo_lectura__icontains=search_tipo)
    if search_consumo_min:
        lecturas = lecturas.filter(consumo_energetico__gte=search_consumo_min)
    if search_consumo_max:
        lecturas = lecturas.filter(consumo_energetico__lte=search_consumo_max)
    
    # Ordenar los resultados
    lecturas = lecturas.order_by('-fecha_lectura')
    page_obj = paginar_objetos(request, lecturas)
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'lecturas': page_obj,
        'page_obj': page_obj,
        'search_fecha': search_fecha,
        'search_tipo': search_tipo,
        'search_consumo_min': search_consumo_min,
        'search_consumo_max': search_consumo_max,
    }
    return render(request, 'lecturas/lista_lecturas.html', datos)

#crear lectura
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

#editar lectura
def editar_lectura(request, lectura_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    if not tiene_permiso(request, 'lecturas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')

    try:
        lectura = Lectura.objects.get(id=lectura_id)
    except Lectura.DoesNotExist:
        messages.error(request, 'La lectura no existe')
        return redirect('sistemaGestion:lista_lecturas')

    if request.method == 'POST':
        form = LecturaForm(request.POST, instance=lectura)
        if form.is_valid():
            lectura_actualizada = form.save()
            messages.success(request, f'Lectura actualizada exitosamente')
            return redirect('sistemaGestion:lista_lecturas')
    else:
        form = LecturaForm(instance=lectura)

    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'form': form,
        'lectura': lectura
    }
    return render(request, 'lecturas/editar_lectura.html', datos)

#eliminar lectura
def eliminar_lectura(request, lectura_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')

    if not tiene_permiso(request, 'lecturas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        lectura = Lectura.objects.get(id=lectura_id)
    except Lectura.DoesNotExist:
        messages.error(request, 'La lectura no existe')
        return redirect('sistemaGestion:lista_lecturas')
    if request.method == 'POST':
        lectura.delete()
        messages.success(request, f'Lectura eliminada exitosamente')
        return redirect('sistemaGestion:lista_lecturas')
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'lectura': lectura
    }
    return render(request, 'lecturas/eliminar_lectura.html', datos)

#detalle lectura
def detalle_lectura(request, lectura_id):
    """Vista de detalle para una lectura específica"""
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'lecturas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        lectura = Lectura.objects.get(id=lectura_id)
    except Lectura.DoesNotExist:
        messages.error(request, 'La lectura no existe')
        return redirect('sistemaGestion:lista_lecturas')
    
    datos = {
        'rol': request.session.get('rol'),
        'nombre': request.session.get('nombre'),
        'lectura': lectura
    }
    return render(request, 'lecturas/detalle_lectura.html', datos)

# ============================================================================
# VISTAS PARA GESTIÓN DE BOLETAS
# ============================================================================

def lista_boletas(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'boletas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Obtener todas las boletas inicialmente
    boletas = Boleta.objects.all()
    
    # Filtros de búsqueda
    search_fecha_emision = request.GET.get('fecha_emision', '')
    search_fecha_vencimiento = request.GET.get('fecha_vencimiento', '')
    search_estado = request.GET.get('estado', '')
    search_monto_min = request.GET.get('monto_min', '')
    search_monto_max = request.GET.get('monto_max', '')
    
    # Aplicar filtros si existen
    if search_fecha_emision:
        boletas = boletas.filter(fecha_emision__gte=search_fecha_emision)
    if search_fecha_vencimiento:
        boletas = boletas.filter(fecha_vencimiento__lte=search_fecha_vencimiento)
    if search_estado:
        boletas = boletas.filter(estado__icontains=search_estado)
    if search_monto_min:
        boletas = boletas.filter(monto_total__gte=search_monto_min)
    if search_monto_max:
        boletas = boletas.filter(monto_total__lte=search_monto_max)
    
    # Ordenar los resultados
    boletas = boletas.order_by('-fecha_emision')
    page_obj = paginar_objetos(request, boletas)
    
    # Estadísticas usando información de boletas
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
        'boletas': page_obj,
        'page_obj': page_obj,
        'estadisticas': estadisticas,
        'search_fecha_emision': search_fecha_emision,
        'search_fecha_vencimiento': search_fecha_vencimiento,
        'search_estado': search_estado,
        'search_monto_min': search_monto_min,
        'search_monto_max': search_monto_max,
    }
    return render(request, 'boletas/lista_boletas.html', datos)

#crear boleta
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

#editar boleta
def editar_boleta(request, boleta_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    if not tiene_permiso(request, 'boletas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')

    try:
        boleta = Boleta.objects.get(id=boleta_id)
    except Boleta.DoesNotExist:
        messages.error(request, 'La boleta no existe')
        return redirect('sistemaGestion:lista_boletas')

    if request.method == 'POST':
        form = BoletaForm(request.POST, instance=boleta)
        if form.is_valid():
            boleta_actualizada = form.save()
            messages.success(request, f'Boleta actualizada exitosamente')
            return redirect('sistemaGestion:lista_boletas')
    else:
        form = BoletaForm(instance=boleta)

    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'form': form,
        'boleta': boleta
    }
    return render(request, 'boletas/editar_boleta.html', datos)

#eliminar boleta
def eliminar_boleta(request, boleta_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')

    if not tiene_permiso(request, 'boletas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        boleta = Boleta.objects.get(id=boleta_id)
    except Boleta.DoesNotExist:
        messages.error(request, 'La boleta no existe')
        return redirect('sistemaGestion:lista_boletas')
    if request.method == 'POST':
        boleta.delete()
        messages.success(request, f'Boleta eliminada exitosamente')
        return redirect('sistemaGestion:lista_boletas')
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'boleta': boleta
    }
    return render(request, 'boletas/eliminar_boleta.html', datos)

#detalle boleta
def detalle_boleta(request, boleta_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'boletas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        boleta = Boleta.objects.get(id=boleta_id)
    except Boleta.DoesNotExist:
        messages.error(request, 'La boleta no existe')
        return redirect('sistemaGestion:lista_boletas')
    
    datos = {
        'rol': request.session.get('rol'),
        'nombre': request.session.get('nombre'),
        'boleta': boleta
    }
    return render(request, 'boletas/detalle_boleta.html', datos)

# ============================================================================
# VISTAS PARA GESTIÓN DE TARIFAS
# ============================================================================

def lista_tarifas(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'tarifas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Obtener todas las tarifas inicialmente
    tarifas = Tarifa.objects.all()
    
    # Filtros de búsqueda
    search_tipo_cliente = request.GET.get('tipo_cliente', '')
    search_tipo_tarifa = request.GET.get('tipo_tarifa', '')
    search_precio_min = request.GET.get('precio_min', '')
    search_precio_max = request.GET.get('precio_max', '')
    search_fecha = request.GET.get('fecha_vigencia', '')
    
    # Aplicar filtros si existen
    if search_tipo_cliente:
        tarifas = tarifas.filter(tipo_cliente__icontains=search_tipo_cliente)
    if search_tipo_tarifa:
        tarifas = tarifas.filter(tipo_tarifa__icontains=search_tipo_tarifa)
    if search_precio_min:
        tarifas = tarifas.filter(precio__gte=search_precio_min)
    if search_precio_max:
        tarifas = tarifas.filter(precio__lte=search_precio_max)
    if search_fecha:
        tarifas = tarifas.filter(fecha_vigencia__gte=search_fecha)
    
    # Ordenar los resultados
    tarifas = tarifas.order_by('tipo_cliente', 'tipo_tarifa')
    page_obj = paginar_objetos(request, tarifas)
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'tarifas': page_obj,
        'page_obj': page_obj,
        'search_tipo_cliente': search_tipo_cliente,
        'search_tipo_tarifa': search_tipo_tarifa,
        'search_precio_min': search_precio_min,
        'search_precio_max': search_precio_max,
        'search_fecha': search_fecha,
    }
    return render(request, 'tarifas/lista_tarifas.html', datos)

#crear tarifa
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

#editar tarifa
def editar_tarifa(request, tarifa_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    if not tiene_permiso(request, 'tarifas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')

    try:
        tarifa = Tarifa.objects.get(id=tarifa_id)
    except Tarifa.DoesNotExist:
        messages.error(request, 'La tarifa no existe')
        return redirect('sistemaGestion:lista_tarifas')

    if request.method == 'POST':
        form = TarifaForm(request.POST, instance=tarifa)
        if form.is_valid():
            tarifa_actualizada = form.save()
            messages.success(request, f'Tarifa actualizada exitosamente')
            return redirect('sistemaGestion:lista_tarifas')
    else:
        form = TarifaForm(instance=tarifa)

    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'form': form,
        'tarifa': tarifa
    }
    return render(request, 'tarifas/editar_tarifa.html', datos)

#eliminar tarifa
def eliminar_tarifa(request, tarifa_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')

    if not tiene_permiso(request, 'tarifas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        tarifa = Tarifa.objects.get(id=tarifa_id)
    except Tarifa.DoesNotExist:
        messages.error(request, 'La tarifa no existe')
        return redirect('sistemaGestion:lista_tarifas')
    if request.method == 'POST':
        tarifa.delete()
        messages.success(request, f'Tarifa eliminada exitosamente')
        return redirect('sistemaGestion:lista_tarifas')
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'tarifa': tarifa
    }
    return render(request, 'tarifas/eliminar_tarifa.html', datos)

#detalle tarifa
def detalle_tarifa(request, tarifa_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'tarifas'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        tarifa = Tarifa.objects.get(id=tarifa_id)
    except Tarifa.DoesNotExist:
        messages.error(request, 'La tarifa no existe')
        return redirect('sistemaGestion:lista_tarifas')
    
    datos = {
        'rol': request.session.get('rol'),
        'nombre': request.session.get('nombre'),
        'tarifa': tarifa
    }
    return render(request, 'tarifas/detalle_tarifa.html', datos)

# ============================================================================
# VISTAS PARA GESTIÓN DE USUARIOS DEL SISTEMA
# ============================================================================

def lista_usuarios(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'usuarios'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Obtener todos los usuarios inicialmente
    usuarios = Usuario.objects.all()
    
    # Filtros de búsqueda
    search_username = request.GET.get('username', '')
    search_email = request.GET.get('email', '')
    search_telefono = request.GET.get('telefono', '')
    search_rol = request.GET.get('rol', '')
    
    # Aplicar filtros si existen
    if search_username:
        usuarios = usuarios.filter(username__icontains=search_username)
    if search_email:
        usuarios = usuarios.filter(email__icontains=search_email)
    if search_telefono:
        usuarios = usuarios.filter(telefono__icontains=search_telefono)
    if search_rol:
        usuarios = usuarios.filter(rol__icontains=search_rol)
    
    # Ordenar los resultados
    usuarios = usuarios.order_by('username')
    page_obj = paginar_objetos(request, usuarios)
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'usuarios': page_obj,
        'page_obj': page_obj,
        'search_username': search_username,
        'search_email': search_email,
        'search_telefono': search_telefono,
        'search_rol': search_rol,
    }
    return render(request, 'usuarios/lista_usuarios.html', datos)

#crear usuario
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

#editar usuario
def editar_usuario(request, usuario_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    if not tiene_permiso(request, 'usuarios'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')

    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, 'El usuario no existe')
        return redirect('sistemaGestion:lista_usuarios')

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario_actualizado = form.save()
            messages.success(request, f'Usuario "{usuario_actualizado.username}" actualizado exitosamente')
            return redirect('sistemaGestion:lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)

    datos = {
        'username': request.session.get('username'),
        'form': form,
        'usuario': usuario
    }
    return render(request, 'usuarios/editar_usuario.html', datos)

#eliminar usuario
def eliminar_usuario(request, usuario_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')

    if not tiene_permiso(request, 'usuarios'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, 'El usuario no existe')
        return redirect('sistemaGestion:lista_usuarios')
    if request.method == 'POST':
        username = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario "{username}" eliminado exitosamente')
        return redirect('sistemaGestion:lista_usuarios')
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'usuario': usuario
    }
    return render(request, 'usuarios/eliminar_usuario.html', datos)

#detalle usuario
def detalle_usuario(request, usuario_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'usuarios'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, 'El usuario no existe')
        return redirect('sistemaGestion:lista_usuarios')
    
    datos = {
        'rol': request.session.get('rol'),
        'nombre': request.session.get('nombre'),
        'usuario': usuario
    }
    return render(request, 'usuarios/detalle_usuario.html', datos)

# ============================================================================
# VISTAS PARA GESTIÓN DE PAGOS
# ============================================================================

def lista_pagos(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'pagos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Obtener todos los pagos inicialmente
    pagos = Pago.objects.all()
    
    # Filtros de búsqueda
    search_fecha = request.GET.get('fecha_pago', '')
    search_metodo = request.GET.get('metodo_pago', '')
    search_estado = request.GET.get('estado_pago', '')
    search_referencia = request.GET.get('numero_referencia', '')
    search_monto_min = request.GET.get('monto_min', '')
    search_monto_max = request.GET.get('monto_max', '')
    
    # Aplicar filtros si existen
    if search_fecha:
        pagos = pagos.filter(fecha_pago__gte=search_fecha)
    if search_metodo:
        pagos = pagos.filter(metodo_pago__icontains=search_metodo)
    if search_estado:
        pagos = pagos.filter(estado_pago__icontains=search_estado)
    if search_referencia:
        pagos = pagos.filter(numero_referencia__icontains=search_referencia)
    if search_monto_min:
        pagos = pagos.filter(monto_pagado__gte=search_monto_min)
    if search_monto_max:
        pagos = pagos.filter(monto_pagado__lte=search_monto_max)
    
    # Ordenar los resultados
    pagos = pagos.order_by('-fecha_pago')
    page_obj = paginar_objetos(request, pagos)
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'pagos': page_obj,
        'page_obj': page_obj,
        'search_fecha': search_fecha,
        'search_metodo': search_metodo,
        'search_estado': search_estado,
        'search_referencia': search_referencia,
        'search_monto_min': search_monto_min,
        'search_monto_max': search_monto_max,
    }
    return render(request, 'pagos/lista_pagos.html', datos)

#crear pago
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

#editar pago
def editar_pago(request, pago_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    if not tiene_permiso(request, 'pagos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')

    try:
        pago = Pago.objects.get(id=pago_id)
    except Pago.DoesNotExist:
        messages.error(request, 'El pago no existe')
        return redirect('sistemaGestion:lista_pagos')

    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            pago_actualizado = form.save()
            messages.success(request, f'Pago actualizado exitosamente')
            return redirect('sistemaGestion:lista_pagos')
    else:
        form = PagoForm(instance=pago)

    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'form': form,
        'pago': pago
    }
    return render(request, 'pagos/editar_pago.html', datos)

#eliminar pago
def eliminar_pago(request, pago_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')

    if not tiene_permiso(request, 'pagos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        pago = Pago.objects.get(id=pago_id)
    except Pago.DoesNotExist:
        messages.error(request, 'El pago no existe')
        return redirect('sistemaGestion:lista_pagos')
    if request.method == 'POST':
        pago.delete()
        messages.success(request, f'Pago eliminado exitosamente')
        return redirect('sistemaGestion:lista_pagos')
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'pago': pago
    }
    return render(request, 'pagos/eliminar_pago.html', datos)

#detalle pago
def detalle_pago(request, pago_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'pagos'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        pago = Pago.objects.get(id=pago_id)
    except Pago.DoesNotExist:
        messages.error(request, 'El pago no existe')
        return redirect('sistemaGestion:lista_pagos')
    
    datos = {
        'rol': request.session.get('rol'),
        'nombre': request.session.get('nombre'),
        'pago': pago
    }
    return render(request, 'pagos/detalle_pago.html', datos)


# ============================================================================
# VISTAS PARA SISTEMA DE NOTIFICACIONES
# ============================================================================
 
def lista_notificaciones(request):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'notificaciones'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    # Filtros de búsqueda
    search_tipo = request.GET.get('tipo', '')
    search_mensaje = request.GET.get('mensaje', '')
    
    # Obtener notificaciones de ambos tipos con filtros
    notificaciones_lectura = NotificacionLectura.objects.all().order_by('id')
    notificaciones_pago = NotificacionPago.objects.all().order_by('id')
    
    # Aplicar filtros de texto en el mensaje
    if search_mensaje:
        notificaciones_lectura = notificaciones_lectura.filter(registro_consumo__icontains=search_mensaje)
        notificaciones_pago = notificaciones_pago.filter(deuda_pendiente__icontains=search_mensaje)
    
    # Combinar ambos tipos de notificaciones con su ID para acciones CRUD
    notificaciones = []
    
    # Agregar notificaciones de lectura si no se filtra por tipo o si es "Lectura"
    if not search_tipo or search_tipo == 'Lectura':
        for notif in notificaciones_lectura:
            notificaciones.append({
                'id': notif.id,
                'tipo': 'Lectura',
                'titulo': 'Notificación de Lectura',
                'mensaje': notif.registro_consumo,
                'url_detalle': f'/notificaciones/lectura/{notif.id}/',
                'url_editar': f'/notificaciones/lectura/editar/{notif.id}/',
                'url_eliminar': f'/notificaciones/lectura/eliminar/{notif.id}/'
            })
    
    # Agregar notificaciones de pago si no se filtra por tipo o si es "Pago"
    if not search_tipo or search_tipo == 'Pago':
        for notif in notificaciones_pago:
            notificaciones.append({
                'id': notif.id,
                'tipo': 'Pago',
                'titulo': 'Notificación de Pago',
                'mensaje': notif.deuda_pendiente,
                'url_detalle': f'/notificaciones/pago/{notif.id}/',
                'url_editar': f'/notificaciones/pago/editar/{notif.id}/',
                'url_eliminar': f'/notificaciones/pago/eliminar/{notif.id}/'
            })
    
    # Paginar la lista combinada de notificaciones
    page_obj = paginar_objetos(request, notificaciones)
    
    datos = {
        'username': request.session.get('username'),
        'nombre': request.session.get('nombre'),
        'rol': request.session.get('rol'),
        'notificaciones': page_obj,
        'page_obj': page_obj,
        'search_tipo': search_tipo,
        'search_mensaje': search_mensaje,
    }
    return render(request, 'notificaciones/lista_notificaciones.html', datos)

# ============================================================================
# VISTA PARA NOTIFICACIONES DE PAGO
# ============================================================================

#crear notificacion lectura
def crear_notificacion_lectura(request):
    """Vista para crear una nueva notificación de lectura"""
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'notificaciones'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    if request.method == 'POST':
        form = NotificacionLecturaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notificación de lectura creada exitosamente')
            return redirect('sistemaGestion:lista_notificaciones')
        else:
            messages.error(request, 'Error al crear la notificación. Revisa los datos.')
    else:
        form = NotificacionLecturaForm()
    
    datos = {
        'rol': request.session.get('rol'),
        'nombre': request.session.get('nombre'),
        'form': form
    }
    return render(request, 'notificaciones/crear_notificacion_lectura.html', datos)

#detalle notificacion lectura
def detalle_notificacion_lectura(request, notificacion_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'notificaciones'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        notificacion = NotificacionLectura.objects.get(id=notificacion_id)
    except NotificacionLectura.DoesNotExist:
        messages.error(request, 'La notificación no existe')
        return redirect('sistemaGestion:lista_notificaciones')
    
    datos = {
        'rol': request.session.get('rol'),
        'nombre': request.session.get('nombre'),
        'notificacion': notificacion
    }
    return render(request, 'notificaciones/detalle_notificacion_lectura.html', datos)

#editar notificacion lectura
def editar_notificacion_lectura(request, notificacion_id):
    """Vista para editar una notificación de lectura existente"""
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'notificaciones'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        notificacion = NotificacionLectura.objects.get(id=notificacion_id)
    except NotificacionLectura.DoesNotExist:
        messages.error(request, 'La notificación no existe')
        return redirect('sistemaGestion:lista_notificaciones')
    
    if request.method == 'POST':
        form = NotificacionLecturaForm(request.POST, instance=notificacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notificación de lectura actualizada exitosamente')
            return redirect('sistemaGestion:detalle_notificacion_lectura', notificacion_id=notificacion.id)
        else:
            messages.error(request, 'Error al actualizar la notificación. Revisa los datos.')
    else:
        form = NotificacionLecturaForm(instance=notificacion)
    
    datos = {
        'rol': request.session.get('rol'),
        'nombre': request.session.get('nombre'),
        'form': form,
        'notificacion': notificacion
    }
    return render(request, 'notificaciones/editar_notificacion_lectura.html', datos)

#eliminar notificacion lectura
def eliminar_notificacion_lectura(request, notificacion_id):
    """Vista para eliminar una notificación de lectura"""
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'notificaciones'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        notificacion = NotificacionLectura.objects.get(id=notificacion_id)
    except NotificacionLectura.DoesNotExist:
        messages.error(request, 'La notificación no existe')
        return redirect('sistemaGestion:lista_notificaciones')
    
    if request.method == 'POST':
        notificacion.delete()
        messages.success(request, 'Notificación de lectura eliminada exitosamente')
        return redirect('sistemaGestion:lista_notificaciones')
    
    datos = {
        'rol': request.session.get('rol'),
        'nombre': request.session.get('nombre'),
        'notificacion': notificacion
    }
    return render(request, 'notificaciones/eliminar_notificacion_lectura.html', datos)

# ============================================================================
# VISTA PARA NOTIFICACIONES DE PAGO
# ============================================================================

def crear_notificacion_pago(request):
    """Vista para crear una nueva notificación de pago"""
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'notificaciones'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    if request.method == 'POST':
        form = NotificacionPagoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notificación de pago creada exitosamente')
            return redirect('sistemaGestion:lista_notificaciones')
        else:
            messages.error(request, 'Error al crear la notificación. Revisa los datos.')
    else:
        form = NotificacionPagoForm()
    
    datos = {
        'rol': request.session.get('rol'),
        'nombre': request.session.get('nombre'),
        'form': form
    }
    return render(request, 'notificaciones/crear_notificacion_pago.html', datos)

#detalle notificacion pago
def detalle_notificacion_pago(request, notificacion_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'notificaciones'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        notificacion = NotificacionPago.objects.get(id=notificacion_id)
    except NotificacionPago.DoesNotExist:
        messages.error(request, 'La notificación no existe')
        return redirect('sistemaGestion:lista_notificaciones')
    
    datos = {
        'rol': request.session.get('rol'),
        'nombre': request.session.get('nombre'),
        'notificacion': notificacion
    }
    return render(request, 'notificaciones/detalle_notificacion_pago.html', datos)

#editar notificacion pago
def editar_notificacion_pago(request, notificacion_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'notificaciones'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        notificacion = NotificacionPago.objects.get(id=notificacion_id)
    except NotificacionPago.DoesNotExist:
        messages.error(request, 'La notificación no existe')
        return redirect('sistemaGestion:lista_notificaciones')
    
    if request.method == 'POST':
        form = NotificacionPagoForm(request.POST, instance=notificacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notificación de pago actualizada exitosamente')
            return redirect('sistemaGestion:detalle_notificacion_pago', notificacion_id=notificacion.id)
        else:
            messages.error(request, 'Error al actualizar la notificación. Revisa los datos.')
    else:
        form = NotificacionPagoForm(instance=notificacion)
    
    datos = {
        'rol': request.session.get('rol'),
        'nombre': request.session.get('nombre'),
        'form': form,
        'notificacion': notificacion
    }
    return render(request, 'notificaciones/editar_notificacion_pago.html', datos)

#eliminar notificacion pago
def eliminar_notificacion_pago(request, notificacion_id):
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    if not tiene_permiso(request, 'notificaciones'):
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('sistemaGestion:dashboard')
    
    try:
        notificacion = NotificacionPago.objects.get(id=notificacion_id)
    except NotificacionPago.DoesNotExist:
        messages.error(request, 'La notificación no existe')
        return redirect('sistemaGestion:lista_notificaciones')
    
    if request.method == 'POST':
        notificacion.delete()
        messages.success(request, 'Notificación de pago eliminada exitosamente')
        return redirect('sistemaGestion:lista_notificaciones')
    
    datos = {
        'rol': request.session.get('rol'),
        'nombre': request.session.get('nombre'),
        'notificacion': notificacion
    }
    return render(request, 'notificaciones/eliminar_notificacion_pago.html', datos)


# ============================================================================
# VISTA DE PERFIL/CONFIGURACIÓN DE USUARIO
# ============================================================================

#esta vista permite al usuario ver y editar su perfil
#esto se realiza mediante un formulario simple que permite cambiar el email y la contraseña

def perfil_usuario(request):
    """
    Vista para mostrar y editar el perfil del usuario logueado
    """
    if not usuario_logueado(request):
        return redirect('sistemaGestion:login')
    
    username = request.session.get('username')
    
    try:
        usuario = Usuario.objects.get(username=username)
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('sistemaGestion:dashboard')
    
    if request.method == 'POST':
        # Obtener datos del formulario
        #se usa strip() para eliminar espacios en blanco al inicio y final
        # de los campos
        nuevo_email = request.POST.get('email', '').strip()
        nueva_password = request.POST.get('password', '').strip()
        confirmar_password = request.POST.get('confirmar_password', '').strip()
        
        # Validaciones especificas para el formulario de perfil
        if nuevo_email:
            usuario.email = nuevo_email
            request.session['email'] = nuevo_email
            
        if nueva_password:
            if nueva_password != confirmar_password:
                messages.error(request, 'Las contraseñas no coinciden')
            elif len(nueva_password) < 6:
                messages.error(request, 'La contraseña debe tener al menos 6 caracteres')
            else:
                usuario.password = nueva_password
                messages.success(request, 'Contraseña actualizada exitosamente')
        
        try:
            usuario.save()
            if nuevo_email:
                messages.success(request, 'Email actualizado exitosamente')
        except Exception as e:
            messages.error(request, f'Error al actualizar el perfil: {str(e)}')
    
    datos = {
        'rol': request.session.get('rol'),
        'nombre': request.session.get('nombre'),
        'usuario': usuario
    }
    
    return render(request, 'usuarios/perfil_usuario.html', datos)