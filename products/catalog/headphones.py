import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
from .common_methods import get_product_info

async def get_first_headphones(session, headphones, producer):
	url = f'https://rozetka.com.ua/naushniki-i-aksessuari/c4660594/producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_product_info(soup, headphones, producer)

async def get_other_headphones(page, session, headphones, producer):
	url = 'https://rozetka.com.ua/naushniki-i-aksessuari/c4660594/page={page};producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_product_info(soup, headphones, producer)