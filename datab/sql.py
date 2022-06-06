import sqlite3
from loguru import logger

class Database():
	def create_db(self, name, db_path):
		connection = sqlite3.connect(str(f'{db_path}/{name}.db'))
		cursor = connection.cursor()
		return (connection, cursor)

	def create_categories_table(self, cursor, connection):
		logger.info(f'\n\tCreating table with categories\n')
		products = ('Телевізори', 'Телефони', 'Годинники', 'Планшети', 'Ноутбуки', 'Монітори', "Комп'ютери", 'Навушники')
		cursor.execute(
				"""
					CREATE TABLE IF NOT EXISTS categories(
						id INT PRIMARY KEY,
						name TEXT
					);
				"""
			)
		connection.commit()

		for i, p in enumerate(products, start=1):
			cursor.execute('INSERT INTO categories VALUES (?, ?);', (i, p))
		connection.commit()

	def create_products_table(self, product_info, db_names:tuple, cursor, connection):
		logger.info('\n\tCreating brand table for each category\n')
		for i, item in enumerate(product_info, start=0):
			brands = []
			for brand in item:
				if brand not in brands:
					brands.append(brand)

			tablename = f'{db_names[i]}_brands'
			cursor.execute(
				f"""
					CREATE TABLE IF NOT EXISTS {tablename}(
						id INT PRIMARY KEY,
						brand_name TEXT
					);
				"""
			)
			connection.commit()

			for j, b in enumerate(brands, start=1):
				cursor.execute(f'INSERT INTO {tablename} VALUES (?, ?);', (j, b))
			connection.commit()