import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
from .common_methods import get_product_info

async def get_first_watches(session, watches, producer):
	url = f'https://rozetka.com.ua/smartwatch/c651392/producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_product_info(soup, watches, producer)

async def get_other_watches(page, session, watches, producer):
	url = 'https://rozetka.com.ua/smartwatch/c651392/page={page};producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_product_info(soup, watches, producer)