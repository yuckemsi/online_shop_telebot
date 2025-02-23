import telebot

from db import DataBase

import kb

from config import TOKEN

db = DataBase()
bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
	db.add_user(tg_id=msg.chat.id, first_name=msg.chat.first_name)
	bot.send_message(msg.chat.id, 'START', reply_markup=kb.main_kb(msg.chat.id))

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):

	msg = call.message
	bot.answer_callback_query(call.id)
	
	if call.data == 'add_product':
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.send_message(msg.chat.id, 'Введите название товара')
		bot.register_next_step_handler(msg, get_price)
	
	elif call.data == 'products':
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.answer_callback_query(call.id)
		bot.send_message(msg.chat.id, 'Наши товары:', reply_markup=kb.products_kb())
	
	elif call.data == 'admin':
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.answer_callback_query(call.id)
		bot.send_message(msg.chat.id, 'Админ-панель', reply_markup=kb.admin_kb())
	
	elif call.data.startswith('product_'):
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.answer_callback_query(call.id)
		product_id = call.data.split('_')[1]
		product = db.get_product(product_id)
		bot.send_photo(msg.chat.id, photo=product[3], caption=f'Название: {product[1]}\n\nЦена: {product[2]}₽', reply_markup=kb.order_product_kb(product_id))

	elif call.data == 'main':
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.answer_callback_query(call.id)
		bot.send_message(msg.chat.id, 'Главное меню', reply_markup=kb.main_kb(msg.chat.id))

	elif call.data.startswith('ordering_'):
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.answer_callback_query(call.id)
		product_id = call.data.split('_')[1]
		get_recipient(msg, product_id)

	elif call.data == 'del_product':
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.send_message(msg.chat.id, 'Выберите товар', reply_markup=kb.delete_product_kb())

	elif call.data.startswith('delete_'):
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.answer_callback_query(call.id)
		product_id = call.data.split('_')[1]
		db.delete_product(product_id)
		bot.send_message(msg.chat.id, 'Товар успешно удален!', reply_markup=kb.admin_kb())

	elif call.data == 'orders':
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.send_message(msg.chat.id, 'Заказы:', reply_markup=kb.orders_kb())

	elif call.data.startswith('order_info_'):
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.answer_callback_query(call.id)
		order_id = call.data.split('_')[2]
		order = db.get_order(order_id)
		product = db.get_product(order[2])
		status = db.get_status(order[6])
		bot.send_message(msg.chat.id, f'Заказ №{order[0]}\n\nТовар: {product[1]}\n\nСтатус: {status[0]}\n\nПолучатель: {order[5]}\n\nАдрес: {order[3]}\n\nТелефон: {order[4]}', reply_markup=kb.manage_order(order_id))

	elif call.data.startswith('del_order_'):
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.answer_callback_query(call.id)
		order_id = call.data.split('_')[2]
		order = db.get_order(order_id)
		bot.send_message(order[1], 'Ваш заказ был удален администратором, чтобы узнать причину обратитесь в поддержку')
		db.delete_order(order_id)
		bot.send_message(msg.chat.id, 'Заказ успешно удален!', reply_markup=kb.orders_kb())
	
	elif call.data.startswith('status_change_'):
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.answer_callback_query(call.id)
		order_id = call.data.split('_')[2]
		status_id = call.data.split('_')[3]
		db.change_status(order_id, status_id)
		order = db.get_order(order_id)
		bot.send_message(order[1], f'Статус вашего заказа был изменен на {db.get_status(status_id)[0]}')
		bot.send_message(msg.chat.id, 'Статус успешно изменен!', reply_markup=kb.orders_kb())
	
	elif call.data.startswith('status_'):
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.answer_callback_query(call.id)
		order_id = call.data.split('_')[1]
		bot.send_message(msg.chat.id, 'Выберите статус', reply_markup=kb.status_kb(order_id))

	elif call.data == 'reviews':
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.send_message(msg.chat.id, 'Отзывы:', reply_markup=kb.reviews_kb())

	elif call.data.startswith('review_'):
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.answer_callback_query(call.id)
		review_id = call.data.split('_')[1]
		revie = db.get_review(review_id)
		bot.send_message(msg.chat.id, f'Отзыв от {revie[2]}:\n\n{revie[3]}', reply_markup=kb.review_kb(id={revie[1]}))

	elif call.data == 'review':
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.send_message(msg.chat.id, 'Напишите отзыв ниже')
		bot.register_next_step_handler(msg, review)

	elif call.data == 'help':
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.answer_callback_query(call.id)
		bot.send_message(msg.chat.id, 'Напишите вопрос ниже')
		bot.register_next_step_handler(msg, add_question)

	elif call.data.startswith('answer_'):
		bot.delete_message(msg.chat.id, msg.message_id)
		bot.answer_callback_query(call.id)
		tg_id = call.data.split('_')[1]
		bot.send_message(msg.chat.id, 'Напишите ваш ответ')
		bot.register_next_step_handler(msg, answer, tg_id)

#HELP FUNCTIONS

def add_question(msg):
	db.add_question(msg.chat.id, msg.text)
	bot.send_message(msg.chat.id, 'Ваш вопрос успешно отправлен!\n\nЖдите ответ от администратора', reply_markup=kb.main_kb(msg.chat.id))
	admins = db.get_admins()
	for admin in admins:
		bot.send_message(admin[1], f'Вопрос от {msg.chat.first_name}:\n\n{msg.text}', reply_markup=kb.answer_kb(msg.chat.id))

def answer(msg, tg_id):
	db.delete_help(tg_id)
	bot.send_message(tg_id, 'Ответ от администратора:\n\n' + msg.text)
	bot.send_message(msg.chat.id, 'Ответ успешно отправлен!', reply_markup=kb.admin_kb())

#REVIEW FUNCTION

def review(msg):
	db.add_review(msg.chat.id, msg.chat.first_name, msg.text)
	bot.send_message(msg.chat.id, 'Спасибо за отзыв!', reply_markup=kb.main_kb(msg.chat.id))
	admins = db.get_admins()
	for admin in admins:
		bot.send_message(admin[1], f'Отзыв от {msg.chat.first_name}:\n\n{msg.text}', reply_markup=kb.admin_kb())
#ORDER FUNCTIONS

def get_recipient(msg, product_id):
	bot.send_message(msg.chat.id, 'Введите получателя')
	bot.register_next_step_handler(msg, get_adress, product_id)

def get_adress(msg, product_id):
	recipient = msg.text
	bot.send_message(msg.chat.id, 'Введите адрес')
	bot.register_next_step_handler(msg, get_phone, recipient, product_id)

def get_phone(msg, recipient, product_id):
	adress = msg.text
	bot.send_message(msg.chat.id, 'Введите номер телефона')
	bot.register_next_step_handler(msg, order, recipient, adress, product_id)

def order(msg, recipient, adress, product_id):
	phone = msg.text
	db.add_order(tg_id=msg.chat.id, product_id=product_id, status_id=1, recipient=recipient, adress=adress, phone=phone)
	bot.send_message(msg.chat.id, 'Заказ успешно оформлен!\n\nПри изменении статуса заказа, вам придет уведомление.', reply_markup=kb.main_kb(msg.chat.id))
	admins = db.get_admins()
	for admin in admins:
		bot.send_message(admin[1], f'Появился новый заказ!', reply_markup=kb.admin_kb())
#PRODUCT FUNCTIONS

def get_price(msg):
	name = msg.text 
	bot.send_message(msg.chat.id, 'Введите цену товара')
	bot.register_next_step_handler(msg, get_img, name)

def get_img(msg, name):
	price = msg.text
	bot.send_message(msg.chat.id, 'Отправьте фото товара')
	bot.register_next_step_handler(msg, adding, name, price)

def adding(msg, name, price):
	photo = max(msg.photo, key=lambda x: x.height)
	img = photo.file_id
	db.add_product(name=name, price=price, img=img)
	bot.send_message(msg.chat.id, 'Товар успешно добавлен!', reply_markup=kb.admin_kb())

if __name__ == '__main__':
	bot.polling(non_stop=True)