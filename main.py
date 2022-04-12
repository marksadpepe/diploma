import time
import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs

from config import rozetka_url
from phones import get_first_phones, get_other_phones

phones = {}
brands = ('apple', 'huawei', 'oppo', 'oneplus', 'samsung', 'xiaomi')

async def get_catalog(url, session):
	res = await session.get(url)
	html = await res.text()
	soup = bs(html, 'lxml')
	categories = soup.find_all('a', class_='menu-categories__link')[0:3]
	return categories

async def main():
	tasks = []
	async with aiohttp.ClientSession() as session:
		categories = await get_catalog(rozetka_url, session)

		for brand in brands:
			await get_first_phones(session, phones, brand)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(get_other_phones(page, session, phones, brand))
				tasks.append(task)

		await asyncio.gather(*tasks)

	for key in phones:
		print(key)

if __name__ == '__main__':
	start = time.time()
	asyncio.run(main())
	end = round(time.time() - start, 2)
	print(f'{end} seconds passed')