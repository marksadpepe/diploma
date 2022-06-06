import datab
import asyncio
import config
import telebot
import products
from loguru import logger

database_path = './datab/dbs'
bot = telebot.TeleBot(config.TOKEN)
products_info = asyncio.run(products.collect_info.collect_products_info())
table_names = ('tv', 'phone', 'watch', 'tablet', 'laptop', 'display', 'computer', 'headphones')

db = datab.sql.Database()
connection, cursor = db.create_db('rozetka', './datab/dbs')
db.create_categories_table(cursor, connection)
db.create_products_table(products_info, table_names, cursor, connection)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
	bot.send_message(msg.chat.id, 'Доброго дня! Я помічник для швидкого придбання або перегляду товару того бренду, який Вас зацікавить. Для цього напишіть команду /buy')

if __name__ == '__main__':
	logger.info(f'\n\tNow u can interact with the bot')
	bot.polling(none_stop=True)

