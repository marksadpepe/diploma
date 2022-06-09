import time
import asyncio
import aiohttp
from . import catalog
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

rozetka_url = 'https://rozetka.com.ua/'

tvs = {}
phones = {}
watches = {}
tablets = {}
laptops = {}
displays = {}
computers = {}
headphones = {}

tv_producers = ('lg', 'philips', 'samsung', 'sony', 'xiaomi') # 5
phone_producers = ('apple', 'huawei', 'oppo', 'oneplus', 'samsung', 'xiaomi') # 6
watch_producers = ('amazfit', 'apple', 'honor', 'huawei', 'samsung', 'xiaomi') # 6
tablet_producers = ('alcatel', 'apple', 'huawei', 'lenovo', 'microsoft', 'samsung') # 6
laptop_producers = ('asus', 'acer', 'apple', 'dell', 'hp', 'lenovo', 'msi', 'microsoft') # 8
display_producers = ('aoc', 'asus', 'acer', 'benq', 'dell', 'hp', 'lg', 'msi', 'philips', 'samsung') # 10
computer_producers = ('artline', 'asus', 'acer', 'apple', 'cobra', 'dell', 'everest', 'hp', 'lenovo') # 9
headphone_producers = ('apple', 'huawei', 'jbl', 'logitech', 'panasonic', 'razer', 'samsung', 'sony', 'xiaomi') # 9

def print_product(product):
	for key in product:
		for model, price in product.get(key).items():
			print(f'{key}: {model} ----> {price}')
	print('--------------------------------------------------------------')

async def collect_products_info():
	tasks = []
	async with aiohttp.ClientSession() as session:

		for phone_producer in tqdm(phone_producers, desc='Collecting phones'):
			await catalog.phones.get_first_phones(session, phones, phone_producer)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(catalog.phones.get_other_phones(page, session, phones, phone_producer))
				tasks.append(task)

		for tv in tqdm(tv_producers, desc='Collecting tvs'):
			await catalog.tvs.get_first_tvs(session, tvs, tv)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(catalog.tvs.get_other_tvs(page, session, tvs, tv))
				tasks.append(task)

		for watch in tqdm(watch_producers, desc='Collecting watches'):
			await catalog.watches.get_first_watches(session, watches, watch)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(catalog.watches.get_other_watches(page, session, watches, watch))
				tasks.append(task)

		for headphone in tqdm(headphone_producers, desc='Collecting headphones'):
			await catalog.headphones.get_first_headphones(session, headphones, headphone)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(catalog.headphones.get_other_headphones(page, session, headphones, headphone))
				tasks.append(task)

		for tablet in tqdm(tablet_producers, desc='Collecting tablets'):
			await catalog.tablets.get_first_tablets(session, tablets, tablet)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(catalog.tablets.get_other_tablets(page, session, tablets, tablet))
				tasks.append(task)

		for laptop in tqdm(laptop_producers, desc='Collecting laptops'):
			await catalog.laptops.get_first_laptops(session, laptops, laptop)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(catalog.laptops.get_other_laptops(page, session, laptops, laptop))
				tasks.append(task)

		for computer in tqdm(computer_producers, desc='Collecting computers'):
			await catalog.computers.get_first_computers(session, computers, computer)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(catalog.computers.get_other_computers(page, session, computers, computer))
				tasks.append(task)

		for display in tqdm(display_producers, desc='Collecting monitors'):
			await catalog.displays.get_first_displays(session, displays, display)
			for page in range(2, 6 + 1):
				task = asyncio.create_task(catalog.displays.get_other_displays(page, session, displays, display))
				tasks.append(task)

		await asyncio.gather(*tasks)
	return (tvs, phones, watches, tablets, laptops, displays, computers, headphones)