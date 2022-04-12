import asyncio
import aiohttp
from loguru import logger
from bs4 import BeautifulSoup as bs

def get_phone_info(soup, phones, producer):
	if producer not in phones:
		phones[producer] = {}

	is_stored = soup.find_all('div', class_='goods-tile__availability goods-tile__availability--available ng-star-inserted')
	if is_stored:
		model = soup.find_all('span', class_='goods-tile__title')
		price = soup.find_all('span', class_='goods-tile__price-value')

		for idx in range(len(is_stored)):
			m = model[idx].text.strip()
			p = price[idx].text.strip()
			s = is_stored[idx].text.strip()

			if '&nbsp;' in p:
				p = p.replace('&nbsp;', '')
			if 'Apple' in m and m not in phones and s in ('Есть в наличии', 'Готов к отправке'):
				phones[producer][m] = p

async def get_first_phones(session, phones, producer):
	url = f'https://rozetka.com.ua/mobile-phones/c80003/producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_phone_info(soup, phones, producer)

async def get_other_phones(page, session, phones, producer):
	url = f'https://rozetka.com.ua/mobile-phones/c80003/page={page};producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_phone_info(soup, phones, producer)
