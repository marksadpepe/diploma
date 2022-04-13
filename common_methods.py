def get_product_info(soup, products, producer):
	if producer in ('lg', 'jbl'):
		producer = producer.upper()
	else:
		producer = producer.capitalize()

	if producer not in products:
		products[producer] = {}

	is_stored = soup.find_all('div', class_='goods-tile__availability goods-tile__availability--available ng-star-inserted')
	if is_stored:
		model = soup.find_all('span', class_='goods-tile__title')
		price = soup.find_all('span', class_='goods-tile__price-value')

		for idx in range(len(is_stored)):
			m = model[idx].text.strip()
			p = price[idx].text.strip()
			s = is_stored[idx].text.strip()

			if producer in m and m not in products and s in ('Есть в наличии', 'Готов к отправке'):
				products[producer][m] = p