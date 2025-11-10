/**
 * Sistema de Tema Oscuro/Claro
 * Maneja el cambio entre modo oscuro y claro con persistencia en localStorage
 */

(function() {
    'use strict';

    // Elementos del DOM
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const htmlElement = document.documentElement;

    // Clave para localStorage
    const THEME_KEY = 'sge-theme-preference';

    /**
     * Obtiene el tema guardado o retorna 'light' por defecto
     */
    function getSavedTheme() {
        const savedTheme = localStorage.getItem(THEME_KEY);
        
        if (savedTheme) {
            return savedTheme;
        }

        // Por defecto siempre usar tema claro
        return 'light';
    }

    /**
     * Aplica el tema especificado
     */
    function applyTheme(theme) {
        if (theme === 'dark') {
            htmlElement.setAttribute('data-theme', 'dark');
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
            themeToggle.setAttribute('title', 'Cambiar a modo claro');
        } else {
            htmlElement.setAttribute('data-theme', 'light');
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
            themeToggle.setAttribute('title', 'Cambiar a modo oscuro');
        }

        // Guardar preferencia
        localStorage.setItem(THEME_KEY, theme);
    }

    /**
     * Alterna entre tema claro y oscuro
     */
    function toggleTheme() {
        const currentTheme = htmlElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Agregar animación suave
        htmlElement.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        
        applyTheme(newTheme);

        // Remover transición después de aplicar el tema
        setTimeout(() => {
            htmlElement.style.transition = '';
        }, 300);
    }

    /**
     * Inicializa el tema al cargar la página
     */
    function initTheme() {
        const savedTheme = getSavedTheme();
        applyTheme(savedTheme);
    }

    // Inicializar tema al cargar
    initTheme();

    // Event listener para el botón de cambio de tema
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    // Escuchar cambios en la preferencia del sistema (opcional)
    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            // Solo aplicar si el usuario no ha establecido una preferencia manual
            const savedTheme = localStorage.getItem(THEME_KEY);
            if (!savedTheme) {
                applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    // Agregar atajo de teclado (Ctrl + Shift + D para Dark/Light)
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.shiftKey && e.key === 'D') {
            e.preventDefault();
            toggleTheme();
        }
    });

})();
