import datab
import asyncio
import config
import telebot
import products
from loguru import logger
from telegram_bot_pagination import InlineKeyboardPaginator

brand_tables = {}
database_path = './datab/dbs'
bot = telebot.TeleBot(config.TOKEN)
products_info = asyncio.run(products.collect_info.collect_products_info())
table_names = ('tv', 'phone', 'watch', 'tablet', 'laptop', 'display', 'computer', 'headphones')

@bot.message_handler(commands=['ok'])
def send_keyboard(msg):
	keyboard = telebot.types.InlineKeyboardMarkup()
	btn1 = telebot.types.InlineKeyboardButton(text='1', callback_data='1')
	btn2 = telebot.types.InlineKeyboardButton(text='2', callback_data='2')
	keyboard.add(btn1)
	keyboard.add(btn2)
	bot.send_message(msg.chat.id, text='Choose', reply_markup=keyboard)

# @bot.callback_query_handler(func=lambda call: call.data == '1' or call.data == '2')
# def callback_category(call: telebot.types.CallbackQuery):
# 	keyboard1 = telebot.types.InlineKeyboardMarkup()
# 	btn1 = telebot.types.InlineKeyboardButton(text='3', callback_data='3')
# 	btn2 = telebot.types.InlineKeyboardButton(text='4', callback_data='4')
# 	keyboard1.add(btn1)
# 	keyboard1.add(btn2)
# 	bot.send_message(call.message.chat.id, text='Choose_v2', reply_markup=keyboard1)

# @bot.callback_query_handler(func=lambda call: call.data in ('3', '4'))
# def first(call: telebot.types.CallbackQuery):
# 	keyboard1 = telebot.types.InlineKeyboardMarkup()
# 	btn1 = telebot.types.InlineKeyboardButton(text='5', callback_data='5')
# 	btn2 = telebot.types.InlineKeyboardButton(text='6', callback_data='6')
# 	keyboard1.add(btn1)
# 	keyboard1.add(btn2)
# 	bot.send_message(call.message.chat.id, text='Choose_v3', reply_markup=keyboard1)
# @bot.message_handler(commands=['ok'])
# def send_keyboard(msg):
# 	keyboard = telebot.types.InlineKeyboardMarkup()
# 	btn1 = telebot.types.InlineKeyboardButton(text='1', callback_data='1')
# 	btn2 = telebot.types.InlineKeyboardButton(text='2', callback_data='2')
# 	keyboard.add(btn1)
# 	keyboard.add(btn2)
# 	bot.send_message(msg.chat.id, text='Choose', reply_markup=keyboard)

# @bot.callback_query_handler(func=lambda call: call.data == '1')
# def callback_category(call: telebot.types.CallbackQuery):
# 	keyboard1 = telebot.types.InlineKeyboardMarkup()
# 	btn1 = telebot.types.InlineKeyboardButton(text='3', callback_data='3')
# 	btn2 = telebot.types.InlineKeyboardButton(text='4', callback_data='4')
# 	keyboard1.add(btn1)
# 	keyboard1.add(btn2)
# 	bot.send_message(call.message.chat.id, text='Choose_v2', reply_markup=keyboard1)

# @bot.callback_query_handler(func=lambda call: call.data in ('3', '4'))
# def first(call: telebot.types.CallbackQuery):
# 	keyboard1 = telebot.types.InlineKeyboardMarkup()
# 	btn1 = telebot.types.InlineKeyboardButton(text='5', callback_data='5')
# 	btn2 = telebot.types.InlineKeyboardButton(text='6', callback_data='6')
# 	keyboard1.add(btn1)
# 	keyboard1.add(btn2)
# 	bot.send_message(call.message.chat.id, text='Choose_v3', reply_markup=keyboard1)

db = datab.sql.Database()
connection, cursor = db.create_db('rozetka', './datab/dbs')
db.create_categories_table(cursor, connection)
db.create_products_table(products_info, table_names, cursor, connection)
db.create_models_table(products_info, table_names, cursor, connection)

cursor.execute('SELECT * FROM categories;')
categories = cursor.fetchall()

for item in table_names:
	cursor.execute(f'SELECT * FROM {item}_brands;')
	table = cursor.fetchall()
	cursor.execute(f'SELECT * FROM {item}_models;')
	models = cursor.fetchall()
	if item not in brand_tables:
		brand_tables[item] = {}
	for t in table:
		_, b = t
		if b not in brand_tables[item]:
			brand_tables[item][b] = {}
		for m in models:
			_, model_name, price, link, _ = m
			if b.lower() in model_name.lower():
				if model_name not in brand_tables[item][b]:	
					brand_tables[item][b][model_name] = []
				brand_tables[item][b][model_name].append(price)
				brand_tables[item][b][model_name].append(link)

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

@bot.callback_query_handler(func=lambda call: call.data in brand_tables)
def get_brands(call: telebot.types.CallbackQuery):
	keyboard = telebot.types.InlineKeyboardMarkup()
	keyboard.row_width = 2

	btns = []
	b_table = brand_tables[call.data]
	for b in brand_tables[call.data]:
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
	# bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] in brand_tables and call.data.split('_')[1] in brand_tables[call.data.split('_')[0]])
def get_models(call):
	text = ''
	product, brand = call.data.split('_')[0], call.data.split('_')[1]
	for i, model in enumerate(brand_tables[product][brand], start=1):
		text += f'{i}. {model}\n'

	if text == '':
		bot.send_message(call.message.chat.id, text='Вибачте, але зараз продуктів цього бренду немає в наявності.\n')
	else:
		bot.send_message(call.message.chat.id, text=text)

if __name__ == '__main__':
	logger.info(f'\n\tNow u can interact with the bot')
	bot.polling(none_stop=True)

