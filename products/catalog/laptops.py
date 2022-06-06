import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
from .common_methods import get_product_info

async def get_first_laptops(session, laptops, producer):
	url = f'https://rozetka.com.ua/notebooks/c80004/producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_product_info(soup, laptops, producer)

async def get_other_laptops(page, session, laptops, producer):
	url = 'https://rozetka.com.ua/notebooks/c80004/page={page};producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_product_info(soup, laptops, producer)