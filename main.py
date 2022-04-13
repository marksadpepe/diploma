import time
import asyncio
import aiohttp
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

from config import rozetka_url
from phones import get_first_phones, get_other_phones
from tvs import get_first_tvs, get_other_tvs
from watches import get_first_watches, get_other_watches
from tablets import get_first_tablets, get_other_tablets
from headphones import get_first_headphones, get_other_headphones

tvs = {}
phones = {}
watches = {}
tablets = {}
headphones = {}

tv_producers = ('lg', 'philips', 'samsung', 'sony', 'xiaomi')
phone_producers = ('apple', 'huawei', 'oppo', 'oneplus', 'samsung', 'xiaomi')
watch_producers = ('amazfit', 'apple', 'honor', 'huawei', 'samsung', 'xiaomi')
tablet_producers = ('alcatel', 'apple', 'huawei', 'lenovo', 'microsoft', 'samsung')
headphone_producers = ('apple', 'huawei', 'jbl', 'logitech', 'panasonic', 'razer', 'samsung', 'sony', 'xiaomi')

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

		for phone_producer in tqdm(phone_producers, desc='Collecting phones'):
			await get_first_phones(session, phones, phone_producer)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(get_other_phones(page, session, phones, phone_producer))
				tasks.append(task)

		for tv in tqdm(tv_producers, desc='Collecting tvs'):
			await get_first_tvs(session, tvs, tv)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(get_other_tvs(page, session, tvs, tv))
				tasks.append(task)

		for watch in tqdm(watch_producers, desc='Collecting watches'):
			await get_first_watches(session, watches, watch)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(get_other_watches(page, session, watches, watch))
				tasks.append(task)

		for headphone in tqdm(headphone_producers, desc='Collecting headphones'):
			await get_first_headphones(session, headphones, headphone)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(get_other_headphones(page, session, headphones, headphone))
				tasks.append(task)

		for tablet in tqdm(tablet_producers, desc='Collecting tablets'):
			await get_first_tablets(session, tablets, tablet)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(get_other_tablets(page, session, tablets, tablet))

		await asyncio.gather(*tasks)

	for key in tablets:
		print(f'{key}: {len(tablets.get(key))}')

if __name__ == '__main__':
	start = time.time()
	asyncio.run(main())

	end = round(time.time() - start, 2)
	print(f'{end} seconds passed')