document.addEventListener('DOMContentLoaded', () => {
    initMobileNav();
    initCategoryFilter();
    initCartInteractions();
    initCartForms();
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

    if (!cartCountElement || !addButtons.length) return;

    addButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const productId = Number(button.dataset.productId);
            const productName = button.dataset.productName || 'Produto';

            if (!productId) {
                showNotification('Produto inválido.');
                return;
            }

            button.disabled = true;
            try {
                const response = await fetch('/cart/add', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ product_id: productId, quantity: 1 })
                });

                const data = await response.json();
                if (!response.ok || !data.success) {
                    throw new Error(data.message || 'Não foi possível adicionar.');
                }

                cartCountElement.textContent = data.cart_count;
                showNotification(`${productName} adicionado ao carrinho.`);
            } catch (error) {
                console.error(error);
                showNotification(error.message || 'Erro ao adicionar ao carrinho.');
            } finally {
                button.disabled = false;
            }
        });
    });
}

function initCartForms() {
    const quantityForms = document.querySelectorAll('.cart-form[data-auto-submit="quantity"]');
    if (!quantityForms.length) return;

    quantityForms.forEach(form => {
        const input = form.querySelector('input[name="quantity"]');
        if (!input) return;
        input.addEventListener('change', () => {
            if (Number(input.value) > 0) {
                form.submit();
            }
        });
    });
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
        setTimeout(() => notification.remove(), 400);
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
