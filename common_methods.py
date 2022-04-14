def get_product_info(soup, products, producer):
	if producer in ('lg', 'jbl', 'asus', 'hp', 'msi', 'artline', 'aoc'):
		producer = producer.upper()

	elif producer == 'benq':
		producer = 'BenQ'
		
	else:
		producer = producer.capitalize()

	if producer not in products:
		products[producer] = {}

	is_stored = soup.find_all('div', class_='goods-tile__availability goods-tile__availability--available ng-star-inserted')
	if is_stored:
		model = soup.find_all('span', class_='goods-tile__title')
		price = soup.find_all('span', class_='goods-tile__price-value')

		min_len = min(len(model), len(price), len(is_stored))

		for idx in range(min_len):
			m = model[idx].text.strip()
			p = price[idx].text.strip()
			s = is_stored[idx].text.strip()

			if producer in m and m not in products[producer] and s in ('Есть в наличии', 'Готов к отправке'):
				products[producer][m] = p