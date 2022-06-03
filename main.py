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
from laptops import get_first_laptops, get_other_laptops
from displays import get_first_displays, get_other_displays
from computers import get_first_computers, get_other_computers
from headphones import get_first_headphones, get_other_headphones

tvs = {}
phones = {}
watches = {}
tablets = {}
laptops = {}
displays = {}
computers = {}
headphones = {}

tv_producers = ('lg', 'philips', 'samsung', 'sony', 'xiaomi')
phone_producers = ('apple', 'huawei', 'oppo', 'oneplus', 'samsung', 'xiaomi')
watch_producers = ('amazfit', 'apple', 'honor', 'huawei', 'samsung', 'xiaomi')
tablet_producers = ('alcatel', 'apple', 'huawei', 'lenovo', 'microsoft', 'samsung')
laptop_producers = ('asus', 'acer', 'apple', 'dell', 'hp', 'lenovo', 'msi', 'microsoft')
display_producers = ('aoc', 'asus', 'acer', 'benq', 'dell', 'hp', 'lg', 'msi', 'philips', 'samsung')
computer_producers = ('artline', 'asus', 'acer', 'apple', 'cobra', 'dell', 'everest', 'hp', 'lenovo')
headphone_producers = ('apple', 'huawei', 'jbl', 'logitech', 'panasonic', 'razer', 'samsung', 'sony', 'xiaomi')

def print_product(product):
	for key in product:
		for model, price in product.get(key).items():
			print(f'{key}: {model} ----> {price}')
	print('--------------------------------------------------------------')

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
				tasks.append(task)

		for laptop in tqdm(laptop_producers, desc='Collecting laptops'):
			await get_first_laptops(session, laptops, laptop)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(get_other_laptops(page, session, laptops, laptop))
				tasks.append(task)

		for computer in tqdm(computer_producers, desc='Collecting computers'):
			await get_first_computers(session, computers, computer)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(get_other_computers(page, session, computers, computer))
				tasks.append(task)

		for display in tqdm(display_producers, desc='Collecting monitors'):
			await get_first_displays(session, displays, display)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(get_other_displays(page, session, displays, display))
				tasks.append(task)

		await asyncio.gather(*tasks)

if __name__ == '__main__':
	start = time.time()
	asyncio.run(main())

	end = round(time.time() - start, 2)
	print(f'{end} seconds passed')