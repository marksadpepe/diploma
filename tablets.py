import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
from common_methods import get_product_info

async def get_first_tablets(session, tablets, producer):
	url = f'https://rozetka.com.ua/tablets/c130309/producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_product_info(soup, tablets, producer)

async def get_other_tablets(page, session, tablets, producer):
	url = 'https://rozetka.com.ua/tablets/c130309/page={page};producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_product_info(soup, tablets, producer)