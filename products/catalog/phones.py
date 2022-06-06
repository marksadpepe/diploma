import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
from .common_methods import get_product_info

async def get_first_phones(session, phones, producer):
	url = f'https://rozetka.com.ua/mobile-phones/c80003/producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_product_info(soup, phones, producer)

async def get_other_phones(page, session, phones, producer):
	url = f'https://rozetka.com.ua/mobile-phones/c80003/page={page};producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_product_info(soup, phones, producer)
