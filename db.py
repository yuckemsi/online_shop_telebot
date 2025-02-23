import sqlite3 as sq

class DataBase():
	def __init__(self) -> None:
		global db, cur
		db = sq.connect('database.db', check_same_thread=False)
		cur = db.cursor()

		cur.execute('''
			CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY,
			tg_id INTEGER,
			first_name TEXT
			)
			''')
		
		cur.execute('''
			CREATE TABLE IF NOT EXISTS products (
			id INTEGER PRIMARY KEY,
			name TEXT,
			price INTEGER,
			img TEXT
			)
			''')

		cur.execute('''
			CREATE TABLE IF NOT EXISTS admins (
			id INTEGER PRIMARY KEY,
			tg_id INTEGER,
			first_name TEXT
			)
			''')

		cur.execute('''
			CREATE TABLE IF NOT EXISTS order_statuses (
			id INTEGER PRIMARY KEY,
			name TEXT
			)
			''')

		cur.execute('''
			CREATE TABLE IF NOT EXISTS orders (
			id INTEGER PRIMARY KEY,
			tg_id INTEGER,
			product_id INTEGER,
			adress TEXT,
			phone TEXT,
			recipient TEXT,
			status_id INTEGER,
			FOREIGN KEY (tg_id) REFERENCES users (tg_id),
			FOREIGN KEY (product_id) REFERENCES products (id),
			FOREIGN KEY (status_id) REFERENCES order_statuses (name)
			)
			''')
		
		cur.execute('''
			CREATE TABLE IF NOT EXISTS reviews (
			id INTEGER PRIMARY KEY,
			tg_id INTEGER,
			first_name TEXT,
			text TEXT,
			FOREIGN KEY (tg_id) REFERENCES users (tg_id)
			)
			''')

		cur.execute('''
			CREATE TABLE IF NOT EXISTS help (
			id INTEGER PRIMARY KEY,
			tg_id INTEGER,
			question TEXT,
			FOREIGN KEY (tg_id) REFERENCES users (tg_id)
			)
			''')

		# cur.execute('INSERT INTO order_statuses (name) VALUES ("В обработке")')
		# cur.execute('INSERT INTO order_statuses (name) VALUES ("Отправлено")')
		# cur.execute('INSERT INTO order_statuses (name) VALUES ("Доставлено")')
		# cur.execute('INSERT INTO admins (tg_id, first_name) VALUES (1175527638, "Matvey")')

		# db.commit()
	
	#ADD REQUESTS

	# HELP 

	def add_question(self, tg_id, question):
		cur.execute('INSERT INTO help (tg_id, question) VALUES (?, ?)', (tg_id, question))
		db.commit()

	# REVIEWS

	def add_review(self, tg_id, first_name, text):
		cur.execute('INSERT INTO reviews (tg_id, first_name, text) VALUES (?, ?, ?)', (tg_id, first_name, text))
		db.commit()

	# USERS

	def add_user(self, tg_id, first_name):
		user = cur.execute('SELECT * FROM users WHERE tg_id = ?', (tg_id,)).fetchone()
		if user is None:
			cur.execute('INSERT INTO users (tg_id, first_name) VALUES (?, ?)', (tg_id, first_name))
		db.commit()
	
	# PRODUCTS

	def add_product(self, name, price, img):
		cur.execute('INSERT INTO products (name, price, img) VALUES (?, ?, ?)', (name, price, img))
		db.commit()
	
	def delete_product(self, id):
		cur.execute('DELETE FROM products WHERE id = ?', (id,))
		db.commit()

	# ORDERS

	def add_order(self, tg_id, product_id, status_id, recipient, adress, phone):
		cur.execute('INSERT INTO orders (tg_id, product_id, status_id, recipient, adress, phone) VALUES (?, ?, ?, ?, ?, ?)', (tg_id, product_id, status_id, recipient, adress, phone))
		db.commit()

	# STATUS

	def change_status(self, order_id, status_id):
		cur.execute('UPDATE orders SET status_id = ? WHERE id = ?', (status_id, order_id))
		db.commit()

	#GET REQUESTS

	# ADMINS

	def get_admins(self):
		admins = cur.execute('SELECT * FROM admins')
		db.commit()
		return admins

	# REVIEWS

	def get_reviews(self):
		reviews = cur.execute('SELECT * FROM reviews')
		db.commit()
		return reviews

	def get_review(self, id):
		review = cur.execute('SELECT * FROM reviews WHERE id = ?', (id,)).fetchone()
		db.commit()
		return review

	# PRODUCTS

	def get_products(self):
		products = cur.execute('SELECT * FROM products')
		db.commit()
		return products
	
	def get_product(self, id):
		product = cur.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()
		db.commit()
		return product

	# ORDERS

	def get_orders(self):
		orders = cur.execute('SELECT * FROM orders')
		db.commit()
		return orders
	
	def get_order(self, id):
		order = cur.execute('SELECT * FROM orders WHERE id = ?', (id,)).fetchone()
		db.commit()
		return order

	# STATUSES

	def get_status(self, id):
		status = cur.execute('SELECT name FROM order_statuses WHERE id = ?', (id,)).fetchone()
		return status
	#CHECK REQUESTS

	def check_admin(self, tg_id):
		user = cur.execute('SELECT * FROM admins WHERE tg_id = ?', (tg_id,)).fetchone()
		db.commit()

		if not user:
			return False
		else:
			return True

	#DELETE REQUESTS

	def delete_order(self, id):
		cur.execute('DELETE FROM orders WHERE id = ?', (id,))
		db.commit()