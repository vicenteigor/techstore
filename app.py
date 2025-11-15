from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
from flask_session import Session
import os
import re

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

products = [
    {
        'id': 1,
        'name': 'Teclado Gamer Membrana Redragon Shiva Rgb Preto K512rgb V2',
        'price': 199.99,
        'category': 'Teclados',
        'image': 'produto_teclado.jpg',
        'description': 'Teclado full size com acionamento de membrana, iluminação RGB personalizável e carcaça alta em ABS. Conta com teclas dedicadas para atalhos multimídia, teclas macro e funcionalidade para troca entre WASD e setas. Possui apoio de pulso magnético texturizado, ajuste de altura e conexão USB. Inclui software para configuração.'
    },
    {
        'id': 2,
        'name': 'Caixa de Som Portátil Bluetooth Rádio FAM',
        'price': 179.99,
        'category': 'Audiobox',
        'image': 'produto_caixinha fam.jpg',
        'description': 'Caixa de som portátil FAM A15 com conectividade Bluetooth, potência de 10W RMS e autonomia de até 8 horas.'
    },
    {
        'id': 3,
        'name': 'Caixa De Som Jbl Flip 7 Branco',
        'price': 789.90,
        'category': 'Audiobox',
        'image': 'produto_caixa jbl.jpg',
        'description': 'Caixa de som JBL Flip 7 com áudio potente de 25W RMS, certificação IP67, Bluetooth, bateria recarregável com até 16 horas de autonomia e design portátil.'
    },
    {
        'id': 4,
        'name': 'Capinha Case Silicone para iPhone',
        'price': 50.00,
        'category': 'Acessórios',
        'image': 'produto_iphone.jpg',
        'description': 'Capa protetora em silicone com interior em camurça, oferecendo proteção leve contra riscos e impactos do dia a dia. Leve, resistente e com proteção dedicada para a câmera.'
    },

    {
        'id': 5,
        'name': 'MÁQUINA DE CORTAR CABELO GAMA ITALY GCX623 SPORT AMARELA',
        'price': 189.90,
        'category': 'Acessórios',
        'image': 'produto_barbeador.jpg',
        'description': 'Máquina multifuncional ideal para cortes, acabamentos e cuidados pessoais. Com 4 cabeças removíveis e 5 pentes guia, oferece 9 possibilidades de corte para cabelo, barba, nariz e orelhas. Funciona com ou sem fio, possui autonomia de 45 minutos e carregamento via USB.'
    }
]

product_specs = {
    1: [
        {
            'title': 'Especificações principais',
            'rows': [
                ('Marca', 'Redragon'),
                ('Modelo', 'K512RGB V2'),
                ('Acionamento', 'Membrana'),
                ('Cor', 'Preto'),
                ('Formato', 'Fullsize'),
                ('Design', 'Carcaça Alta'),
                ('Layout', 'ABNT2'),
                ('Conectividade', 'USB'),
                ('Software', 'Sim'),
                ('Altura ajustável', 'Sim'),
                ('Materiais do case', 'Plástico ABS'),
                ('Iluminação', 'RGB'),
                ('Rollover', '26 teclas (teclas sublinhadas)'),
                ('Dimensões aproximadas', '464 x 214 x 40 mm'),
            ]
        }
    ],
    2: [
        {
            'title': 'Características gerais',
            'rows': [
                ('Marca', 'FAM'),
                ('Modelo', 'A15'),
                ('Modelo alfanumérico', 'A15'),
                ('Cor', 'Rosa'),
            ]
        },
        {
            'title': 'Acessórios',
            'rows': [
                ('Com base', 'Não'),
                ('Com microfone', 'Não'),
                ('Inclui suporte', 'Não'),
            ]
        },
        {
            'title': 'Outros',
            'rows': [
                ('É à prova d\'água', 'Sim'),
            ]
        },
        {
            'title': 'Conectividade',
            'rows': [
                ('Com Bluetooth', 'Sim'),
                ('Com Wi-Fi', 'Não'),
            ]
        },
        {
            'title': 'Homologação',
            'rows': [
                ('Homologação Anatel Nº', '090442416051'),
                ('Fabricante', 'FAM'),
            ]
        },
        {
            'title': 'Som',
            'rows': [
                ('Potência de saída (RMS)', '10 W'),
            ]
        },
        {
            'title': 'Bateria',
            'rows': [
                ('Autonomia máxima da bateria', '8 h'),
                ('Inclui bateria recarregável', 'Não'),
            ]
        },
        {
            'title': 'Especificações',
            'rows': [
                ('Com luzes LED', 'Não'),
                ('Com controladores DJ integrados', 'Não'),
                ('Com função karaokê', 'Não'),
                ('Com efeito de voz', 'Não'),
                ('Com rádio', 'Não'),
                ('É portátil', 'Sim'),
                ('É sem fio', 'Sim'),
                ('É gamer', 'Não'),
            ]
        }
    ],
    3: [
        {
            'title': 'Informações gerais',
            'rows': [
                ('Tipo de montagem', 'Suporte de mesa'),
                ('Nome do modelo', 'JBLFLIP7WHTBR'),
                ('Tipo de alto-falante', 'Caixa de Som Portátil'),
                ('Adequação do controle por rádio', 'Para Smartphones ou Tablets, Para Atividades ao Ar Livre'),
                ('Dispositivos compatíveis', 'Smartphone'),
                ('Cor', 'Branco'),
                ('Componentes incluídos', 'Cabo de alimentação'),
                ('Dimensões do produto', '10P x 30L x 10A mm'),
                ('É impermeável', 'Sim'),
            ]
        },
        {
            'title': 'Garantia e fabricante',
            'rows': [
                ('Tipo de garantia', 'Limitado'),
                ('Número de itens', '1'),
                ('Fabricante', 'JBL'),
                ('Garantia do fabricante', '12 meses'),
            ]
        },
        {
            'title': 'Conectividade e controle',
            'rows': [
                ('Método de controle', 'Aplicação'),
                ('Tecnologia de comunicação sem fio', 'Auracast'),
                ('Conexões', 'Auracast'),
                ('Fonte de alimentação', 'Fio elétrico'),
            ]
        },
        {
            'title': 'Certificações e energia',
            'rows': [
                ('Certificação', '09899-24-07120 · 10587-24-07120 · 10024-24-07120'),
                ('Tipo do produto', 'Eletrônicos'),
                ('Tipo de amplificação', 'Passivo'),
                ('ENE (Etiqueta Nacional de Eficiência)', 'A+'),
            ]
        },
        {
            'title': 'Bateria e autonomia',
            'rows': [
                ('Duração média da bateria', '16 horas'),
                ('Capacidade da bateria', '16 horas'),
                ('Baterias inclusas', 'Não'),
                ('Funciona com baterias', 'Não'),
            ]
        },
        {
            'title': 'Outros detalhes',
            'rows': [
                ('Cor correspondente', 'Branco'),
                ('Peso do produto', '820 g'),
            ]
        }
    ],
    4: [
        {
            'title': 'Materiais e construção',
            'rows': [
                ('Materiais do exterior', 'Silicone'),
                ('Materiais do interior', 'Silicone'),
            ]
        },
        {
            'title': 'Linha e modelo',
            'rows': [
                ('Linha da capa', 'Case transparente, proteção contra quedas, encaixe perfeito, anti impacto'),
                ('Modelo da capa', 'Case compatível com iPhone com proteção anti impacto'),
            ]
        }
    ],
    5: [
        {
            'title': 'Informações principais',
            'rows': [
                ('Nome do produto', 'Multi-Styler Ga.Ma Gcx623 Sport - USB'),
                ('Marca', 'GA.MA Italy Professional'),
                ('Tipo de cabelo', 'Todos'),
                ('Fabricante', 'GA.MA Italy'),
                ('Número do modelo', 'BECCP0000000816'),
                ('ASIN', 'B07VQWPRRD'),
                ('Funciona a bateria ou pilha?', 'Sim'),
                ('EAN', '7898496354447'),
            ]
        },
        {
            'title': 'Informações adicionais',
            'rows': [
                ('Dimensões do pacote', '19.4 x 13.4 x 9 cm'),
                ('Bateria', '1 íon de lítio (inclusa)'),
            ]
        }
    ]
}

COUPONS = {
    'EXEMPLO1': {
        'code': 'EXEMPLO1',
        'label': '10% OFF em todo o carrinho',
        'type': 'percentage',
        'value': 0.10
    }
}


def find_product(product_id):
    return next((product for product in products if product['id'] == product_id), None)


def get_cart():
    if 'cart' not in session:
        session['cart'] = {}
    return session['cart']


def get_cart_count():
    cart = session.get('cart', {})
    return sum(cart.values())


def apply_coupon_code(code):
    coupon = COUPONS.get(code.upper())
    if not coupon:
        return None
    session['coupon'] = coupon
    session.modified = True
    return coupon


def clear_coupon():
    if 'coupon' in session:
        session.pop('coupon')
        session.modified = True


def set_shipping(cep, cost, eta):
    session['shipping'] = {
        'cep': cep,
        'cost': cost,
        'eta': eta
    }
    session.modified = True


def clear_shipping():
    if 'shipping' in session:
        session.pop('shipping')
        session.modified = True


def sanitize_cep(raw_cep):
    return re.sub(r'\D', '', raw_cep or '')


def format_cep(cep_numbers):
    if len(cep_numbers) == 8:
        return f'{cep_numbers[:5]}-{cep_numbers[5:]}'
    return cep_numbers


def estimate_shipping_cost(cep):
    cep_numbers = sanitize_cep(cep)
    if len(cep_numbers) != 8:
        raise ValueError('CEP inválido. Informe 8 dígitos.')

    # Simple pseudo-calculation for demo purposes
    base = 19.9
    modifier = int(cep_numbers[-3:]) % 5
    cost = round(base + modifier * 3.5, 2)
    eta_days = 3 + (int(cep_numbers[-1]) % 4)
    return cost, f'{eta_days} dias úteis'


def build_cart_snapshot():
    cart = get_cart()
    items = []
    subtotal = 0.0

    invalid_ids = []
    for product_id_str, quantity in cart.items():
        try:
            product_id = int(product_id_str)
        except ValueError:
            invalid_ids.append(product_id_str)
            continue

        product = find_product(product_id)
        if not product:
            invalid_ids.append(product_id_str)
            continue

        quantity = max(1, int(quantity))
        line_total = product['price'] * quantity
        subtotal += line_total
        items.append({
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'quantity': quantity,
            'line_total': line_total,
            'image': product['image'],
            'category': product['category']
        })

    for invalid_id in invalid_ids:
        cart.pop(invalid_id, None)
    if invalid_ids:
        session.modified = True

    coupon = session.get('coupon')
    discount = 0.0
    if coupon:
        if coupon['type'] == 'percentage':
            discount = subtotal * coupon['value']
        elif coupon['type'] == 'fixed':
            discount = coupon['value']
    discount = round(discount, 2)

    shipping = session.get('shipping', {})
    shipping_cost = round(shipping.get('cost', 0.0), 2)

    total = max(subtotal - discount + shipping_cost, 0.0)

    return {
        'items': items,
        'subtotal': round(subtotal, 2),
        'discount': discount,
        'shipping': shipping,
        'shipping_cost': shipping_cost,
        'total': round(total, 2),
        'savings': discount,
        'coupon': coupon
    }


@app.context_processor
def inject_globals():
    return {
        'cart_count': get_cart_count()
    }

@app.route('/')
def index():
    return render_template('index.html', products_list=products)

@app.route('/products')
def products_page():
    return render_template('index.html', products_list=products)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/politica-de-privacidade')
def privacy():
    return render_template('privacy.html')


@app.route('/trocas-e-devolucoes')
def returns_policy():
    return render_template('returns.html')


@app.route('/garantia')
def warranty():
    return render_template('warranty.html')


@app.route('/produto/<int:product_id>')
def product_detail(product_id):
    product = find_product(product_id)
    if not product:
        abort(404)
    specs = product_specs.get(product_id, [])
    return render_template('product_detail.html', product=product, specs=specs)


@app.route('/cart')
def view_cart():
    cart_snapshot = build_cart_snapshot()
    feedback = session.pop('cart_feedback', None)
    return render_template('cart.html', cart=cart_snapshot, feedback=feedback)


@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json(silent=True) or request.form
    product_id = int(data.get('product_id', 0))
    quantity = max(1, int(data.get('quantity', 1)))

    product = find_product(product_id)
    if not product:
        message = 'Produto não encontrado.'
        if request.is_json:
            return jsonify({'success': False, 'message': message}), 404
        session['cart_feedback'] = {'status': 'error', 'message': message}
        return redirect(url_for('view_cart'))

    cart = get_cart()
    cart_key = str(product_id)
    cart[cart_key] = cart.get(cart_key, 0) + quantity
    session.modified = True

    if request.is_json:
        snapshot = build_cart_snapshot()
        return jsonify({
            'success': True,
            'cart_count': get_cart_count(),
            'product_name': product['name'],
            'cart': snapshot
        })

    session['cart_feedback'] = {'status': 'success', 'message': f"{product['name']} adicionado ao carrinho."}
    return redirect(url_for('view_cart'))


@app.route('/cart/update', methods=['POST'])
def update_cart():
    data = request.get_json(silent=True) or request.form
    product_id = int(data.get('product_id', 0))
    quantity = int(data.get('quantity', 1))

    cart = get_cart()
    key = str(product_id)
    if key not in cart:
        message = 'Produto não está no carrinho.'
        if request.is_json:
            return jsonify({'success': False, 'message': message}), 404
        session['cart_feedback'] = {'status': 'error', 'message': message}
        return redirect(url_for('view_cart'))

    if quantity <= 0:
        cart.pop(key)
    else:
        cart[key] = quantity
    session.modified = True

    if request.is_json:
        snapshot = build_cart_snapshot()
        return jsonify({'success': True, 'cart': snapshot, 'cart_count': get_cart_count()})

    session['cart_feedback'] = {'status': 'success', 'message': 'Carrinho atualizado.'}
    return redirect(url_for('view_cart'))


@app.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    data = request.get_json(silent=True) or request.form
    product_id = int(data.get('product_id', 0))
    cart = get_cart()
    key = str(product_id)
    if key in cart:
        cart.pop(key)
        session.modified = True

    if request.is_json:
        snapshot = build_cart_snapshot()
        return jsonify({'success': True, 'cart_count': get_cart_count(), 'cart': snapshot})

    session['cart_feedback'] = {'status': 'success', 'message': 'Item removido do carrinho.'}
    return redirect(url_for('view_cart'))


@app.route('/cart/apply-coupon', methods=['POST'])
def apply_coupon():
    code = (request.form.get('coupon') or '').strip()
    try:
        coupon = apply_coupon_code(code)
    except Exception:
        coupon = None

    if coupon:
        session['cart_feedback'] = {'status': 'success', 'message': f"Cupom {coupon['code']} aplicado."}
    else:
        session['cart_feedback'] = {'status': 'error', 'message': 'Cupom inválido.'}
    return redirect(url_for('view_cart'))


@app.route('/cart/remove-coupon', methods=['POST'])
def remove_coupon():
    clear_coupon()
    session['cart_feedback'] = {'status': 'success', 'message': 'Cupom removido.'}
    return redirect(url_for('view_cart'))


@app.route('/cart/shipping', methods=['POST'])
def calculate_shipping():
    cep = request.form.get('cep')
    try:
        cep_numbers = sanitize_cep(cep)
        cost, eta = estimate_shipping_cost(cep_numbers)
        set_shipping(format_cep(cep_numbers), cost, eta)
        session['cart_feedback'] = {'status': 'success', 'message': 'Frete calculado com sucesso.'}
    except ValueError as exc:
        session['cart_feedback'] = {'status': 'error', 'message': str(exc)}
        clear_shipping()
    return redirect(url_for('view_cart'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
