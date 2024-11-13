import stripe
from forex_python.converter import CurrencyRates

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(name):
    """ Создает продукт в stripe. """
    product = stripe.Product.create(name=name)
    return product.get('id')


# def convert_rub_to_dollars(amount):
#     """
#      Переводит доллары в рубли. Для этого устанавливаем
#      библиотеку forex-python.
#      poetry add forex-python
#     """
#     c = CurrencyRates()
#     rate = c.get_rate('RUB', 'USD')
#     return int(amount * rate)


def create_stripe_price(payment_object):
    """ Создает цену в stripe. """

    price = stripe.Price.create(
        currency="rub",
        # переводим из копеек в руб / из центов доллары
        unit_amount=int(payment_object.price * 100),
        # recurring={"interval": "month"}, # ежемесячная оплата
        product_data={"name": payment_object.name},
    )
    return price.get('id')


def create_stripe_sessions(price_id):
    """ Создает сессию на оплату в stripe. """
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        # если одноразовая покупка, то payment, если recurring,
        # то mode="subscription"
        mode="payment",
    )
    return session.get('id'), session.get('url')


def check_payment_status(session_id):
    """ Проверяет статус платежа в Stripe по session_id. """
    session = stripe.checkout.Session.retrieve(session_id)
    return session.get("payment_status")
