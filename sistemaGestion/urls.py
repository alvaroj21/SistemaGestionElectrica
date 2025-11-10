from django.urls import path
from . import views #importa las vistas desde el mismo directorio

app_name = 'sistemaGestion'

urlpatterns = [
    path('', views.login_view, name='login'), # Página de inicio redirige al login
    path('login/', views.login_view, name='login'), # Login
    path('logout/', views.logout_view, name='logout'),  # Logout
    path('inicio/', views.dashboard, name='dashboard'),   # Dashboard o página principal después del login
    path('perfil/', views.perfil_usuario, name='perfil_usuario'), # Perfil/configuración del usuario
    
    # Clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'), #  pagina de lista de clientes
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'), # Página para crear un nuevo cliente
    path('clientes/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'), # Detalle de cliente
    path('clientes/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'), # Eliminar cliente
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'), # Editar cliente
    
    # Contratos
    path('contratos/', views.lista_contratos, name='lista_contratos'), # Página de lista de contratos
    path('contratos/crear/', views.crear_contrato, name='crear_contrato'),  # Página para crear un nuevo contrato
    path('contratos/<int:contrato_id>/', views.detalle_contrato, name='detalle_contrato'), # Detalle de contrato
    path('contratos/eliminar/<int:contrato_id>/', views.eliminar_contrato, name='eliminar_contrato'), # Eliminar contrato
    path('contratos/editar/<int:contrato_id>/', views.editar_contrato, name='editar_contrato'), # Editar contrato   
    
    # Medidores
    path('medidores/', views.lista_medidores, name='lista_medidores'), # Página de lista de medidores
    path('medidores/crear/', views.crear_medidor, name='crear_medidor'), # Página para crear un nuevo medidor
    path('medidores/<int:medidor_id>/', views.detalle_medidor, name='detalle_medidor'), # Detalle de medidor
    path('medidores/<int:medidor_id>/ubicacion/', views.ubicacion_medidor, name='ubicacion_medidor'), # Ubicación del medidor
    path('medidores/eliminar/<int:medidor_id>/', views.eliminar_medidor, name='eliminar_medidor'), # Eliminar medidor
    path('medidores/editar/<int:medidor_id>/', views.editar_medidor, name='editar_medidor'), # Editar medidor
    
    # Lecturas
    path('lecturas/', views.lista_lecturas, name='lista_lecturas'), # Página de lista de lecturas
    path('lecturas/crear/', views.crear_lectura, name='crear_lectura'), # Página para crear una nueva lectura
    path('lecturas/<int:lectura_id>/', views.detalle_lectura, name='detalle_lectura'), # Detalle de lectura
    path('lecturas/eliminar/<int:lectura_id>/', views.eliminar_lectura, name='eliminar_lectura'), # Eliminar lectura
    path('lecturas/editar/<int:lectura_id>/', views.editar_lectura, name='editar_lectura'), # Editar lectura
    
    # Boletas
    path('boletas/', views.lista_boletas, name='lista_boletas'), # Página de lista de boletas
    path('boletas/crear/', views.crear_boleta, name='crear_boleta'), # Página para crear una nueva boleta
    path('boletas/<int:boleta_id>/', views.detalle_boleta, name='detalle_boleta'), # Detalle de boleta
    path('boletas/eliminar/<int:boleta_id>/', views.eliminar_boleta, name='eliminar_boleta'), # Eliminar boleta
    path('boletas/editar/<int:boleta_id>/', views.editar_boleta, name='editar_boleta'), # Editar boleta
    
    # Pagos
    path('pagos/', views.lista_pagos, name='lista_pagos'), # Página de lista de pagos
    path('pagos/crear/', views.crear_pago, name='crear_pago'),  # Página para crear un nuevo pago
    path('pagos/<int:pago_id>/', views.detalle_pago, name='detalle_pago'), # Detalle de pago
    path('pagos/eliminar/<int:pago_id>/', views.eliminar_pago, name='eliminar_pago'), # Eliminar pago
    path('pagos/editar/<int:pago_id>/', views.editar_pago, name='editar_pago'), # Editar pago
    
    # Usuarios
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'), # Página de lista de usuarios
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'), # Página para crear un nuevo usuario
    path('usuarios/<int:usuario_id>/', views.detalle_usuario, name='detalle_usuario'), # Detalle de usuario
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'), # Eliminar usuario
    path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'), # Editar usuario
    
    # Tarifas
    path('tarifas/', views.lista_tarifas, name='lista_tarifas'), # Página de lista de tarifas
    path('tarifas/crear/', views.crear_tarifa, name='crear_tarifa'), # Página para crear una nueva tarifa
    path('tarifas/<int:tarifa_id>/', views.detalle_tarifa, name='detalle_tarifa'), # Detalle de tarifa
    path('tarifas/eliminar/<int:tarifa_id>/', views.eliminar_tarifa, name='eliminar_tarifa'), # Eliminar tarifa
    path('tarifas/editar/<int:tarifa_id>/', views.editar_tarifa, name='editar_tarifa'), # Editar tarifa
    
    # Notificaciones
    path('notificaciones/', views.lista_notificaciones, name='lista_notificaciones'), # Página de lista de notificaciones
    path('notificaciones/marcar-revisada/<str:tipo>/<int:notificacion_id>/', views.marcar_notificacion_revisada, name='marcar_notificacion_revisada'), # Marcar notificación como revisada
    
    # Notificaciones de Lectura
    path('notificaciones/lectura/crear/', views.crear_notificacion_lectura, name='crear_notificacion_lectura'), # Crear notificación de lectura
    path('notificaciones/lectura/<int:notificacion_id>/', views.detalle_notificacion_lectura, name='detalle_notificacion_lectura'), # Detalle de notificación de lectura
    path('notificaciones/lectura/editar/<int:notificacion_id>/', views.editar_notificacion_lectura, name='editar_notificacion_lectura'), # Editar notificación de lectura
    path('notificaciones/lectura/eliminar/<int:notificacion_id>/', views.eliminar_notificacion_lectura, name='eliminar_notificacion_lectura'), # Eliminar notificación de lectura
    
    # Notificaciones de Pago
    path('notificaciones/pago/crear/', views.crear_notificacion_pago, name='crear_notificacion_pago'), # Crear notificación de pago
    path('notificaciones/pago/<int:notificacion_id>/', views.detalle_notificacion_pago, name='detalle_notificacion_pago'), # Detalle de notificación de pago
    path('notificaciones/pago/editar/<int:notificacion_id>/', views.editar_notificacion_pago, name='editar_notificacion_pago'), # Editar notificación de pago
    path('notificaciones/pago/eliminar/<int:notificacion_id>/', views.eliminar_notificacion_pago, name='eliminar_notificacion_pago'), # Eliminar notificación de pago
    
    # Reportes PDF
    path('boletas/<int:boleta_id>/pdf/', views.generar_pdf_boleta, name='pdf_boleta'), # Generar PDF de boleta
]