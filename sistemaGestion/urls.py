from django.urls import path
from . import views

app_name = 'sistemaGestion'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('inicio/', views.dashboard, name='dashboard'),  
    # Clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    
    # Contratos
    path('contratos/', views.lista_contratos, name='lista_contratos'),
    path('contratos/crear/', views.crear_contrato, name='crear_contrato'),
    
    # Medidores
    path('medidores/', views.lista_medidores, name='lista_medidores'),
    path('medidores/crear/', views.crear_medidor, name='crear_medidor'),
    
    # Lecturas
    path('lecturas/', views.lista_lecturas, name='lista_lecturas'),
    path('lecturas/crear/', views.crear_lectura, name='crear_lectura'),
    
    # Boletas
    path('boletas/', views.lista_boletas, name='lista_boletas'),
    path('boletas/crear/', views.crear_boleta, name='crear_boleta'),
    
    # Pagos
    path('pagos/', views.lista_pagos, name='lista_pagos'),
    path('pagos/crear/', views.crear_pago, name='crear_pago'),
    
    # Usuarios
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    
    # Tarifas
    path('tarifas/', views.lista_tarifas, name='lista_tarifas'),
    path('tarifas/crear/', views.crear_tarifa, name='crear_tarifa'),
    
    # Notificaciones
    path('notificaciones/', views.lista_notificaciones, name='lista_notificaciones'),
    path('notificaciones/<int:id>/', views.detalle_notificacion, name='detalle_notificacion'),
]