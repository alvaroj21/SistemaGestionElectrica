// ============================================
// SISTEMA DE GESTIÓN ELÉCTRICA - INTERACCIONES ÚNICAS
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ============================================
    // ANIMACIONES DE ENTRADA
    // ============================================
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('fade-in-up');
                }, index * 100);
            }
        });
    }, observerOptions);

    // Observar cards, gráficos y widgets
    document.querySelectorAll('.card-neo, .chart-container, .dashboard-widget, .stat-card').forEach(el => {
        observer.observe(el);
    });

    // ============================================
    // EFECTO PARALLAX SUAVE EN HEADER
    // ============================================
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const scrolled = window.pageYOffset;
                const header = document.querySelector('.header-custom');
                if (header && scrolled < 500) {
                    header.style.transform = `translateY(${scrolled * 0.3}px)`;
                    header.style.opacity = 1 - (scrolled / 800);
                }
                ticking = false;
            });
            ticking = true;
        }
    });

    // ============================================
    // HOVER EFFECTS PARA TABLAS
    // ============================================
    const tableRows = document.querySelectorAll('.table-modern tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        });
    });

    // ============================================
    // EFECTO RIPPLE EN BOTONES
    // ============================================
    function createRipple(event) {
        const button = event.currentTarget;
        const ripple = document.createElement('span');
        const diameter = Math.max(button.clientWidth, button.clientHeight);
        const radius = diameter / 2;

        ripple.style.width = ripple.style.height = `${diameter}px`;
        ripple.style.left = `${event.clientX - button.offsetLeft - radius}px`;
        ripple.style.top = `${event.clientY - button.offsetTop - radius}px`;
        ripple.classList.add('ripple');

        const rippleEffect = button.getElementsByClassName('ripple')[0];
        if (rippleEffect) {
            rippleEffect.remove();
        }

        button.appendChild(ripple);
    }

    const buttons = document.querySelectorAll('.btn-electric, .btn-energy, .btn-success, .btn-danger');
    buttons.forEach(button => {
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.addEventListener('click', createRipple);
    });

    // CSS para el efecto ripple
    const style = document.createElement('style');
    style.textContent = `
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    // ============================================
    // TOOLTIP PERSONALIZADO
    // ============================================
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function(e) {
            const tooltip = document.createElement('div');
            tooltip.className = 'custom-tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            document.body.appendChild(tooltip);

            const rect = this.getBoundingClientRect();
            tooltip.style.cssText = `
                position: fixed;
                top: ${rect.top - tooltip.offsetHeight - 10}px;
                left: ${rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)}px;
                background: rgba(10, 35, 66, 0.95);
                color: white;
                padding: 8px 15px;
                border-radius: 8px;
                font-size: 0.875rem;
                z-index: 1000;
                animation: fadeInUp 0.3s ease-out;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            `;

            this._tooltip = tooltip;
        });

        element.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });

    // ============================================
    // CONFIRMACIÓN PERSONALIZADA PARA ELIMINACIONES
    // ============================================
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const message = this.getAttribute('data-confirm-delete') || '¿Estás seguro de eliminar este elemento?';
            
            if (confirm(message)) {
                if (this.href) {
                    window.location.href = this.href;
                } else if (this.form) {
                    this.form.submit();
                }
            }
        });
    });

    // ============================================
    // BÚSQUEDA EN TIEMPO REAL EN TABLAS
    // ============================================
    const searchInputs = document.querySelectorAll('[data-table-search]');
    searchInputs.forEach(input => {
        const tableId = input.getAttribute('data-table-search');
        const table = document.getElementById(tableId);
        
        if (table) {
            input.addEventListener('keyup', function() {
                const filter = this.value.toLowerCase();
                const rows = table.querySelectorAll('tbody tr');
                
                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(filter) ? '' : 'none';
                });
            });
        }
    });

    // ============================================
    // CONTADOR ANIMADO PARA ESTADÍSTICAS
    // ============================================
    function animateValue(element, start, end, duration) {
        const range = end - start;
        const increment = end > start ? 1 : -1;
        const stepTime = Math.abs(Math.floor(duration / range));
        let current = start;
        
        const timer = setInterval(() => {
            current += increment;
            element.textContent = current.toLocaleString('es-CL');
            if (current === end) {
                clearInterval(timer);
            }
        }, stepTime);
    }

    const statValues = document.querySelectorAll('.stat-value[data-count]');
    const statObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                const target = parseInt(entry.target.getAttribute('data-count'));
                animateValue(entry.target, 0, target, 1000);
                entry.target.classList.add('counted');
            }
        });
    }, { threshold: 0.5 });

    statValues.forEach(stat => statObserver.observe(stat));

    // ============================================
    // SMOOTH SCROLL
    // ============================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // ============================================
    // SIDEBAR RESPONSIVE
    // ============================================
    const sidebarToggle = document.querySelector('[data-sidebar-toggle]');
    const sidebar = document.querySelector('.sidebar-diagonal');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }

    // ============================================
    // MARCAR ENLACE ACTIVO EN NAVEGACIÓN
    // ============================================
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar-diagonal nav a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // ============================================
    // AUTOCOMPLETAR MEJORADO
    // ============================================
    const autocompleteInputs = document.querySelectorAll('[data-autocomplete]');
    autocompleteInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Aquí puedes agregar lógica de autocompletado con AJAX
            console.log('Autocompletando:', this.value);
        });
    });

    // ============================================
    // FORMATO AUTOMÁTICO PARA NÚMEROS
    // ============================================
    const numberInputs = document.querySelectorAll('input[type="number"], .format-number');
    numberInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value) {
                const formatted = parseFloat(this.value).toLocaleString('es-CL');
                if (this.classList.contains('format-number')) {
                    this.textContent = formatted;
                }
            }
        });
    });

    // ============================================
    // VALIDACIÓN DE FORMULARIOS EN TIEMPO REAL
    // ============================================
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });

        form.addEventListener('submit', function(e) {
            let isValid = true;
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                e.preventDefault();
                showNotification('Por favor, corrige los errores en el formulario', 'danger');
            }
        });
    });

    function validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let message = '';

        if (field.hasAttribute('required') && !value) {
            isValid = false;
            message = 'Este campo es requerido';
        }

        if (field.type === 'email' && value && !isValidEmail(value)) {
            isValid = false;
            message = 'Email inválido';
        }

        if (field.type === 'number') {
            const min = field.getAttribute('min');
            const max = field.getAttribute('max');
            const numValue = parseFloat(value);

            if (min && numValue < parseFloat(min)) {
                isValid = false;
                message = `El valor mínimo es ${min}`;
            }
            if (max && numValue > parseFloat(max)) {
                isValid = false;
                message = `El valor máximo es ${max}`;
            }
        }

        showFieldValidation(field, isValid, message);
        return isValid;
    }

    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function showFieldValidation(field, isValid, message) {
        let feedback = field.parentElement.querySelector('.field-feedback');
        
        if (!feedback) {
            feedback = document.createElement('div');
            feedback.className = 'field-feedback';
            field.parentElement.appendChild(feedback);
        }

        field.style.borderColor = isValid ? '' : 'var(--danger-red)';
        feedback.textContent = message;
        feedback.style.cssText = `
            color: var(--danger-red);
            font-size: 0.875rem;
            margin-top: 0.25rem;
            display: ${isValid ? 'none' : 'block'};
        `;
    }

    // ============================================
    // NOTIFICACIONES TOAST
    // ============================================
    window.showNotification = function(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            z-index: 10000;
            animation: slideInRight 0.5s ease-out;
            max-width: 300px;
        `;

        const colors = {
            success: 'var(--success-green)',
            danger: 'var(--danger-red)',
            warning: 'var(--warning-orange)',
            info: 'var(--primary-electric)'
        };

        toast.style.borderLeft = `5px solid ${colors[type] || colors.info}`;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.5s ease-out';
            setTimeout(() => toast.remove(), 500);
        }, duration);
    };

    // Agregar animaciones para las notificaciones
    const toastStyle = document.createElement('style');
    toastStyle.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(toastStyle);

    // ============================================
    // MODO OSCURO (OPCIONAL)
    // ============================================
    const darkModeToggle = document.querySelector('[data-dark-mode-toggle]');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        });

        // Cargar preferencia guardada
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
        }
    }

    console.log('🔌 Sistema de Gestión Eléctrica - Diseño único cargado correctamente');
});
