import datab
import asyncio
import config
import telebot
import products
from loguru import logger
from telegram_bot_pagination import InlineKeyboardPaginator

counter = 0
main_table = {}
product, brand = None, None
database_path = './datab/dbs'
bot = telebot.TeleBot(config.TOKEN)

products_info = asyncio.run(products.collect_info.collect_products_info())
table_names = ('tv', 'phone', 'watch', 'tablet', 'laptop', 'display', 'computer', 'headphones')

db = datab.sql.Database()
connection, cursor = db.create_db('rozetka', './datab/dbs')
db.create_categories_table(cursor, connection)
db.create_brands_table(products_info, table_names, cursor, connection)
db.create_models_table(products_info, table_names, cursor, connection)

cursor.execute('SELECT * FROM categories;')
categories = cursor.fetchall()

for item in table_names:
	cursor.execute(f'SELECT * FROM {item}_brands;')
	table = cursor.fetchall()
	cursor.execute(f'SELECT * FROM {item}_models;')
	models = cursor.fetchall()
	if item not in main_table:
		main_table[item] = {}
	for t in table:
		_, b = t
		if b not in main_table[item]:
			main_table[item][b] = {}
		for m in models:
			_, model_name, price, link, _ = m
			if b.lower() in model_name.lower():
				if model_name not in main_table[item][b]:	
					main_table[item][b][model_name] = []
				main_table[item][b][model_name].append(price)
				main_table[item][b][model_name].append(link)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
	bot.send_message(msg.chat.id, 'Доброго дня! Я помічник для швидкого придбання або перегляду товару того бренду, який Вас зацікавить. Для цього напишіть (або натисніть на) команду /buy.')

@bot.message_handler(commands=['buy'])
def get_categories(msg):
	buttons = []
	keyboard = telebot.types.InlineKeyboardMarkup()
	keyboard.row_width = 2
	
	for i, category_tuple in enumerate(categories, start=0):
		_, category_name = category_tuple
		key_category = telebot.types.InlineKeyboardButton(text=f'{category_name}', callback_data=table_names[i])
		buttons.append(key_category)

	for idx in range(len(buttons) - int(len(buttons)/2)):
		if idx != 0:
			idx += idx
		keyboard.row(buttons[idx], buttons[idx + 1])
	bot.send_message(msg.chat.id, text='Оберіть категорію:\n', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in main_table)
def get_brands(call: telebot.types.CallbackQuery):
	keyboard = telebot.types.InlineKeyboardMarkup()
	keyboard.row_width = 2

	btns = []
	b_table = main_table[call.data]
	for b in main_table[call.data]:
		key_brand = telebot.types.InlineKeyboardButton(text=f'{b}', callback_data=f'{call.data}_{b}')
		btns.append(key_brand)

	if len(btns) % 2 == 0:
		for idx in range(len(btns) - int(len(btns) / 2)):
			if idx != 0:
				idx += idx
			keyboard.row(btns[idx], btns[idx + 1])
	else:
		for idx in range(len(btns) - 1 - int((len(btns) - 1) / 2)):
			if idx != 0:
				idx += idx
			keyboard.row(btns[idx], btns[idx + 1])
		keyboard.add(btns[-1])
	bot.send_message(call.message.chat.id, text='Оберіть бренд продукту:\n', reply_markup=keyboard)
	bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] in main_table and call.data.split('_')[1] in main_table[call.data.split('_')[0]])
def get_models(call):
	global counter
	global product
	global brand
	text = 'Оберіть варінт моделі продукту, впишіть його та відправте боту.\n\n'

	product, brand = call.data.split('_')[0], call.data.split('_')[1]
	if len(main_table[product][brand]) == 0:
		bot.send_message(call.message.chat.id, text='Вибачте, але зараз продуктів цього бренду немає в наявності.\n')

	elif 0 < len(main_table[product][brand]) <= 10:
		for i, model in enumerate(main_table[product][brand], start=1):
			text += f'{i}. {model}\n'
		bot.send_message(call.message.chat.id, text=text)

	else:
		for k, key in enumerate(main_table[product][brand], start=1):
			if k > 10 and str(k)[-1] == '1':
				counter = k
				break
			text += f'{k}. {key}\n'
		send_models_page(call.message, product, brand, text)
	bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='model')
def get_next_models(call):
	global counter
	global product
	global brand
	text = 'Оберіть варінт (номер) моделі продукту, впишіть його та відправте боту.\n\n'
	page = int(call.data.split('#')[1])

	for k, key in enumerate(main_table[product][brand], start=1):
		if k > counter and str(k)[-1] == '1':
				counter = k
				break
		if k >= counter:
			text += f'{k}. {key}\n'
	bot.delete_message(call.message.chat.id, call.message.message_id)
	send_models_page(call.message, product, brand, text, page)

@bot.message_handler(content_types=['text'])
def get_model_info(msg):
	global prodcut
	global brand
	price = 0
	keyboard = telebot.types.InlineKeyboardMarkup()
	msg_text = msg.text
	if msg_text.isdigit() is False:
		bot.send_message(msg.chat.id, text=f'Будь ласка, введіть номер моделі або команду.')
	else:
		for i, item in enumerate(main_table[product][brand], start=1):
			if int(i) == int(msg_text):
				price = main_table[product][brand][item][0]
				link = main_table[product][brand][item][1]
				key_link = telebot.types.InlineKeyboardButton(text=item, url=link)
				keyboard.add(key_link)
		bot.send_message(msg.chat.id, text=f'Ціна обраного товару: {price} грн.', reply_markup=keyboard)

def send_models_page(message, pr, br, text, page=1):
	page_len = (len(main_table[pr][br]) // 10) + 1
	paginator = InlineKeyboardPaginator(page_len, current_page=page, data_pattern='model#{page}')
	bot.send_message(message.chat.id, text=text, reply_markup=paginator.markup)

if __name__ == '__main__':
	logger.info(f'\n\tNow u can interact with the bot')
	bot.polling(none_stop=True)
