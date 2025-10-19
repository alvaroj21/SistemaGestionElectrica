//en este main.js van los scripts generales de la aplicacion

// Validación de contraseñas en perfil_usuario.html
// Este bloque se ejecuta solo si existen los campos de contraseña

document.addEventListener('DOMContentLoaded', function() {
    const password = document.getElementById('password');
    const confirmarPassword = document.getElementById('confirmar_password');
    if (password && confirmarPassword) {
        function validarPasswords() {
            if (password.value && confirmarPassword.value) {
                if (password.value !== confirmarPassword.value) {
                    confirmarPassword.setCustomValidity('Las contraseñas no coinciden');
                    confirmarPassword.classList.add('is-invalid');
                } else {
                    confirmarPassword.setCustomValidity('');
                    confirmarPassword.classList.remove('is-invalid');
                    confirmarPassword.classList.add('is-valid');
                }
            } else {
                confirmarPassword.setCustomValidity('');
                confirmarPassword.classList.remove('is-invalid', 'is-valid');
            }
        }
        password.addEventListener('input', validarPasswords);
        confirmarPassword.addEventListener('input', validarPasswords);
    }
});