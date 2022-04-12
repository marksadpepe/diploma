import time
import asyncio
import aiohttp
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

from config import rozetka_url
from phones import get_first_phones, get_other_phones
from tvs import get_first_tvs, get_other_tvs

tvs = {}
phones = {}
tv_producers = ('lg', 'philips', 'samsung', 'sony', 'xiaomi')
phone_producers = ('apple', 'huawei', 'oppo', 'oneplus', 'samsung', 'xiaomi')

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

		for phone_producer in tqdm(phone_producers):
			await get_first_phones(session, phones, phone_producer)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(get_other_phones(page, session, phones, phone_producer))
				tasks.append(task)

		for tv in tqdm(tv_producers):
			await get_first_tvs(session, tvs, tv)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(get_other_tvs(page, session, tvs, tv))
				tasks.append(task)

		await asyncio.gather(*tasks)

	for producer in phones:
		print(producer, len(phones.get(producer)))

	for tv in tvs:
		print(tv, len(tvs.get(tv)))


if __name__ == '__main__':
	start = time.time()
	asyncio.run(main())

	end = round(time.time() - start, 2)
	print(f'{end} seconds passed')