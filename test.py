import time
import requests as req
from bs4 import BeautifulSoup as bs

phones = {}

def get_first():
	url = 'https://rozetka.com.ua/mobile-phones/c80003/producer=apple/'
	r = req.get(url)
	soup = bs(r.text, 'lxml')

	model = soup.find_all('span', class_='goods-tile__title')
	price = soup.find_all('span', class_='goods-tile__price-value')

	for idx in range(len(model)):
		m = model[idx].text.strip()
		p = price[idx].text.strip()
		if '&nbsp;' in p:
			p = p.replace('&nbsp;', '')
		if 'Apple' in m and m not in phones:
			phones[m] = p

def get_other(page):
	url = f'https://rozetka.com.ua/mobile-phones/c80003/page={page};producer=apple/'
	r = req.get(url)
	soup = bs(r.text, 'lxml')

	model = soup.find_all('span', class_='goods-tile__title')
	price = soup.find_all('span', class_='goods-tile__price-value')

	if page == 12:
		del model[-3:]

	for idx in range(len(model)):
		m = model[idx].text.strip()
		p = price[idx].text.strip()
		if '&nbsp;' in p:
			p = p.replace('&nbsp;', '')
		if 'Apple' in m and m not in phones:
			phones[m] = p

	print(f'Done with page {page}')

def main():
	for page in range(2, 12+1):
		get_other(page)


if __name__ == '__main__':
	start = time.time()
	main()
	end = round(time.time() - start, 2)
	print(f'Took {end} seconds')

