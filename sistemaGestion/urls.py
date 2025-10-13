from django.urls import path
from . import views #importa las vistas desde el mismo directorio

app_name = 'sistemaGestion'

urlpatterns = [
    path('', views.login_view, name='login'), # Página de inicio redirige al login
    path('login/', views.login_view, name='login'), # Login
    path('logout/', views.logout_view, name='logout'),  # Logout
    path('inicio/', views.dashboard, name='dashboard'),   # Dashboard o página principal después del login
    # Clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'), #  pagina de lista de clientes
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'), # Página para crear un nuevo cliente
    path('clientes/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'), # Eliminar cliente
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'), # Editar cliente
    # Contratos
    path('contratos/', views.lista_contratos, name='lista_contratos'), # Página de lista de contratos
    path('contratos/crear/', views.crear_contrato, name='crear_contrato'),  # Página para crear un nuevo contrat
    path('contratos/eliminar/<int:contrato_id>/', views.eliminar_contrato, name='eliminar_contrato'), # Eliminar contrato
    path('contratos/editar/<int:contrato_id>/', views.editar_contrato, name='editar_contrato'), # Editar contrato   
    
    # Medidores
    path('medidores/', views.lista_medidores, name='lista_medidores'), # Página de lista de medidores
    path('medidores/crear/', views.crear_medidor, name='crear_medidor'), # Página para crear un nuevo medidor
    
    # Lecturas
    path('lecturas/', views.lista_lecturas, name='lista_lecturas'), # Página de lista de lecturas
    path('lecturas/crear/', views.crear_lectura, name='crear_lectura'), # Página para crear una nueva lectura

    
    # Boletas
    path('boletas/', views.lista_boletas, name='lista_boletas'), # Página de lista de boletas
    path('boletas/crear/', views.crear_boleta, name='crear_boleta'), # Página para crear una nueva boleta
    
    # Pagos
    path('pagos/', views.lista_pagos, name='lista_pagos'), # Página de lista de pagos
    path('pagos/crear/', views.crear_pago, name='crear_pago'),  # Página para crear un nuevo pago
    
    # Usuarios
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'), # Página de lista de usuarios
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'), # Página para crear un nuevo usuario

    # Tarifas
    path('tarifas/', views.lista_tarifas, name='lista_tarifas'), # Página de lista de tarifas
    path('tarifas/crear/', views.crear_tarifa, name='crear_tarifa'), # Página para crear una nueva tarifa
    
    # Notificaciones
    path('notificaciones/', views.lista_notificaciones, name='lista_notificaciones'), # Página de lista de notificaciones
]