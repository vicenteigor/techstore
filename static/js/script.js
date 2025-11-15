const storageKey = 'techstore-cart-count';

document.addEventListener('DOMContentLoaded', () => {
    initMobileNav();
    initCategoryFilter();
    initCartInteractions();
    initNewsletterForms();
    initContactForms();
});

function initMobileNav() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.getElementById('nav-menu');

    if (!hamburger || !navMenu) return;

    hamburger.addEventListener('click', () => {
        const isOpen = navMenu.classList.toggle('active');
        hamburger.setAttribute('aria-expanded', String(isOpen));
        document.body.classList.toggle('nav-open', isOpen);
    });

    navMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            hamburger.setAttribute('aria-expanded', 'false');
            document.body.classList.remove('nav-open');
        });
    });
}

function initCategoryFilter() {
    const chips = document.querySelectorAll('.chip');
    const cards = document.querySelectorAll('.product-card');

    if (!chips.length) return;

    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            chips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');

            const filter = chip.dataset.filter;
            cards.forEach(card => {
                const matches = filter === 'all' || card.dataset.category === filter;
                card.style.display = matches ? 'flex' : 'none';
            });
        });
    });
}

function initCartInteractions() {
    const cartCountElement = document.querySelector('.cart-count');
    const addButtons = document.querySelectorAll('.add-to-cart');

    if (!cartCountElement) return;

    const savedCount = readCartCount();
    updateCartCount(cartCountElement, savedCount);

    addButtons.forEach(button => {
        button.addEventListener('click', () => {
            const currentCount = readCartCount() + 1;
            writeCartCount(currentCount);
            updateCartCount(cartCountElement, currentCount);

            const name = button.dataset.productName || 'Produto';
            showNotification(`${name} adicionado ao carrinho.`);
        });
    });
}

function updateCartCount(element, value) {
    element.textContent = value;
}

function showNotification(message) {
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();

    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('hide');
        notification.addEventListener('transitionend', () => notification.remove(), { once: true });
        setTimeout(() => notification.remove(), 400); // fallback
    }, 2600);
}

function initNewsletterForms() {
    const forms = document.querySelectorAll('.newsletter-form');
    if (!forms.length) return;

    forms.forEach(form => {
        form.addEventListener('submit', event => {
            event.preventDefault();
            form.reset();
            showNotification('Obrigado! Em breve você receberá nossas novidades.');
        });
    });
}

function initContactForms() {
    const forms = document.querySelectorAll('.contact-form');
    if (!forms.length) return;

    forms.forEach(form => {
        form.addEventListener('submit', event => {
            event.preventDefault();
            form.reset();
            showNotification('Recebemos sua mensagem. Responderemos em breve!');
        });
    });
}

function readCartCount() {
    try {
        return Number(localStorage.getItem(storageKey) || 0);
    } catch (_error) {
        return 0;
    }
}

function writeCartCount(value) {
    try {
        localStorage.setItem(storageKey, String(value));
    } catch (_error) {
        /* ignore */
    }
}
