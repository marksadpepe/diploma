import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
from .common_methods import get_product_info

async def get_first_displays(session, displays, producer):
	url = f'https://hard.rozetka.com.ua/monitors/c80089/producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_product_info(soup, displays, producer)

async def get_other_displays(page, session, displays, producer):
	url = 'https://hard.rozetka.com.ua/monitors/c80089/page={page};producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_product_info(soup, displays, producer)