Proyecto para la asignatura de Backend, plataforma web de gestión electrica El sistema es una plataforma de gestion electrica para el apoyo en la creacion, registro y visualizacion de datos para la municipalidad de Alto del Carmen, esto en necesidad tanto del departamento electrico como de finanzas.

La plataforma permite el inicio de sesion por medio de roles dependiendo del cargo del empleado, dentro de esta se podran crear datos respecto a los distintos medidores, lecturas, clientes, tarifas, contratos, boletas y pagos. Considerando tambien la inclusion del administrador quien se hara cargo de la creacion de los usuarios.

Este registro de datos se complementa con la idea de poder entregar informacion visual respecto a distintos datos como pueden ser la lectura o la ubicacion de los medidores.

Actualmente la plataforma se encuentra en desarrollo, lo presentado actualmente solo es un ejemplo y prototipo de lo que se desea realizar con este proyecto.

La pagina se encuentra alojada actualmente en: https://sgem.pythonanywhere.com/ para su testeo.

Para usar el proyecto:

-para su instalacion primero clona el repositorio o descarga el zip directamente, luego abrir lo resultante con visual studio code.

-Instala las dependencias por medio de pip isntall -r requeriments.txt

-ejecuta el servidor por medio de python manage.py runserver y accede desde el navegador a http://127.0.0.1:8000/ o http://127.0.0.1:8000/admin/ si deseas ingresar al administrador de django

¿Que permite realizar este sistema?

Puedes acceder al sistema para realizar distintas gestiones administrativas relacionadas a un sistema de gestion electrico a traves de un login que realizas por medio de un usuario con rol de administrador, electrico o finanzas (se puede ingrasar por medio de los usuarios que se muestran an en la pagina de login)

**Gestion de clientes**: Ver, registrar, editar y elimianr
**Gestion de medidores**: Ver, registrar, editar, eliminar y ver su ubicacion.
**Gestion de lectura**: Ver, registrar, editar y eliminar
**Gestion de tarifa**: Ver, registrar, editar y eliminar
**Gestion de boletas y pagos**: Ver, registrar, editar y eliminar
**Gestion de notificaciones**: Ver, registaar, editar y eliminar
**Perfil de usuario** Todos los usuarios pueden acceder a su perfil de usuario y cambiar ya sea el email asociado o contraseña

Se pueden visualizar los datos de distintos datos a traves de un dashboard y acceder a distantas opciones a traves de un acceso rapido en este.
Los elementos que se muestren en este depende de los permisos dado el rol que tiene el usuario
