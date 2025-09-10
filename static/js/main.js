/*
 * Alterna el estado de visibilidad de una categoría (expandir/colapsar)
 * * Funcionamiento:
 * - Si la categoría está cerrada: la abre, cambia flecha a ▲, añade clase 'active'
 * - Si la categoría está abierta: la cierra, cambia flecha a ▼, quita clase 'active'
 */

function alternarCategoria(element) {
    const content = element.nextElementSibling;
    const arrow = element.querySelector('.flecha');
    
    if (content.style.display === 'none' || content.style.display === '') {
        content.style.display = 'block';
        arrow.textContent = '▲';
        element.classList.add('active');
    } else {
        content.style.display = 'none';
        arrow.textContent = '▼';
        element.classList.remove('active');
    }
}

// Inicializar todas las categorías como cerradas
document.addEventListener('DOMContentLoaded', function() {
    const contents = document.querySelectorAll('.contenido-categoria-navegacion');
    contents.forEach(content => {
        content.style.display = 'none';
    });
});
