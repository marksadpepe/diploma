import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
from .common_methods import get_product_info

async def get_first_computers(session, computers, producer):
	url = f'https://hard.rozetka.com.ua/computers/c80095/producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_product_info(soup, computers, producer)

async def get_other_computers(page, session, computers, producer):
	url = 'https://hard.rozetka.com.ua/computers/c80095/page={page};producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_product_info(soup, computers, producer)