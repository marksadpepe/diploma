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

	def create_brands_table(self, product_info, db_names:tuple, cursor, connection):
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

	def create_models_table(self, info, db_names, cursor, connection):
		logger.info('\n\tCreating model table for each brand\n')
		for i, item in enumerate(info, start=0):
			model_id = 1
			tablename = f'{db_names[i]}_models'
			parent_table = f'{db_names[i]}_brands'
			cursor.execute(
					f"""
						CREATE TABLE IF NOT EXISTS {tablename}(
							id INT PRIMARY KEY,
							model TEXT,
							price TEXT,
							link TEXT,
							brand TEXT
						);
					"""
				)
			connection.commit()

			for brand in item:
				if item.get(brand):
					for model, values in item.get(brand).items():
						cursor.execute(f'INSERT INTO {tablename} VALUES (?, ?, ?, ?, ?);', (model_id, model, values[0], values[1], brand))
						model_id += 1
			connection.commit()
