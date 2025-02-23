from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from main import db

def main_kb(tg_id):
    admin = db.check_admin(tg_id)
    kb = InlineKeyboardMarkup()
    if admin is False:
        b1 = InlineKeyboardButton(text='Товары', callback_data='products')
        b2 = InlineKeyboardButton(text='Отзывы', callback_data='reviews')
        b3 = InlineKeyboardButton(text='Оставить отзыв⭐', callback_data='review')
        b4 = InlineKeyboardButton(text='Поддержка⚙', callback_data='help')

        kb.add(b1)
        kb.add(b2)
        kb.add(b3)
        kb.add(b4)

    if admin is True:
        b1 = InlineKeyboardButton(text='Товары', callback_data='products')
        b2 = InlineKeyboardButton(text='Поддержка⚙', callback_data='help')
        b3 = InlineKeyboardButton(text='Админ-панель', callback_data='admin')
        b4 = InlineKeyboardButton(text='Отзывы', callback_data='reviews')

        kb.add(b1)
        kb.add(b2)
        kb.add(b3)
        kb.add(b4)

    return kb

def reviews_kb():
    reviews = db.get_reviews()
    kb = InlineKeyboardMarkup()
    if not reviews:
        b = InlineKeyboardButton(text='У нас пока нет отзывов :(')
        b1 = InlineKeyboardButton(text='⬅️ Назад', callback_data='main')
        kb.add(b)
        kb.add(b1)
    else:
        for review in reviews:
            b = InlineKeyboardButton(text=f'Отзыв от {review[2]}', callback_data=f'review_{review[0]}')
            kb.add(b)
        b1 = InlineKeyboardButton(text='⬅️ Назад', callback_data='main')
        kb.add(b1)
    return kb

def review_kb(id):
    kb = InlineKeyboardMarkup()
    b = InlineKeyboardButton(text='👤 Ссылка на пользователя', url=f'tg://user?id={id}')
    b1 = InlineKeyboardButton(text='⬅️ Назад', callback_data='reviews')
    kb.add(b)
    kb.add(b1)
    return kb

def products_kb():
    products = db.get_products()
    kb = InlineKeyboardMarkup()
    if not products:
        b = InlineKeyboardButton(text='У нас пока нет товаров :(')
        b1 = InlineKeyboardButton(text='⬅️ Назад', callback_data='main')
        kb.add(b)
        kb.add(b1)
    else:
        for product in products:
            b = InlineKeyboardButton(text=product[1], callback_data=f'product_{product[0]}')
            
            kb.add(b)
        b1 = InlineKeyboardButton(text='⬅️ Назад', callback_data='main')
        kb.add(b1)
    return kb

def order_product_kb(id):
    kb = InlineKeyboardMarkup()
    b = InlineKeyboardButton(text='Заказать', callback_data=f'ordering_{id}')
    b1 = InlineKeyboardButton(text='⬅️ Назад', callback_data=f'products')
    kb.add(b)
    kb.add(b1)
    return kb

def admin_kb():
    kb = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton(text='Добавить товар', callback_data='add_product')
    b2 = InlineKeyboardButton(text='Удалить товар', callback_data='del_product')
    b3 = InlineKeyboardButton(text='Заказы', callback_data='orders')
    b4 = InlineKeyboardButton(text='⬅️ Назад', callback_data='main')

    kb.add(b1)
    kb.add(b2)
    kb.add(b3)
    kb.add(b4)
    return kb

def delete_product_kb():
    products = db.get_products()
    kb = InlineKeyboardMarkup()
    if not products:
        b = InlineKeyboardButton(text='У нас пока нет товаров :(')
        b1 = InlineKeyboardButton(text='⬅️ Назад', callback_data='admin')
        kb.add(b)
        kb.add(b1)
    else:
        for product in products:
            b = InlineKeyboardButton(text=product[1], callback_data=f'delete_{product[0]}')
            
            kb.add(b)
        b1 = InlineKeyboardButton(text='⬅️ Назад', callback_data='admin')
        kb.add(b1)
    return kb

def orders_kb():
    orders = db.get_orders()
    kb = InlineKeyboardMarkup()
    if not orders:
        b = InlineKeyboardButton(text='У нас пока нет заказов :(')
        b1 = InlineKeyboardButton(text='⬅️ Назад', callback_data='admin')
        kb.add(b)
        kb.add(b1)
    else:
        for order in orders:
            b = InlineKeyboardButton(text=f'Заказ №{order[0]}', callback_data=f'order_info_{order[0]}')
            kb.add(b)
        b1 = InlineKeyboardButton(text='⬅️ Назад', callback_data='admin')
        kb.add(b1)
    return kb


def manage_order(id):
    kb = InlineKeyboardMarkup()
    b = InlineKeyboardButton(text='Удалить заказ', callback_data=f'del_order_{id}')
    b1 = InlineKeyboardButton(text='Изменить статус', callback_data=f'status_{id}')
    b2 = InlineKeyboardButton(text='⬅️ Назад', callback_data='orders')
    kb.add(b)
    kb.add(b1)
    kb.add(b2)
    return kb

def status_kb(id):
    kb = InlineKeyboardMarkup()
    b = InlineKeyboardButton(text='В обработке', callback_data=f'status_change_{id}_1')
    b1 = InlineKeyboardButton(text='Отправлен', callback_data=f'status_change_{id}_2')
    b2 = InlineKeyboardButton(text='Доставлен', callback_data=f'status_change_{id}_3')
    b3 = InlineKeyboardButton(text='⬅️ Назад', callback_data=f'order_info_{id}')
    kb.add(b)
    kb.add(b1)
    kb.add(b2)
    kb.add(b3)
    return kb