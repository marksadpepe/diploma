import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
from common_methods import get_product_info

async def get_first_tvs(session, tvs, producer):
	url = f'https://rozetka.com.ua/all-tv/c80037/producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_product_info(soup, tvs, producer)

async def get_other_tvs(page, session, tvs, producer):
	url = 'https://rozetka.com.ua/all-tv/c80037/page={page};producer={producer}/'

	async with session.get(url) as res:
		html = await res.text()
		soup = bs(html, 'lxml')

		get_product_info(soup, tvs, producer)
