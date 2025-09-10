// Inicializar todas las categorías como cerradas
document.addEventListener('DOMContentLoaded', function() {
    const contents = document.querySelectorAll('.contenido-categoria-navegacion');
    contents.forEach(content => {
        content.style.display = 'none';
    });
});
