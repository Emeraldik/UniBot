import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent as ua
import re
import difflib

def main():
	search = input('Input something: ')
	search = search.replace(' ', '%20')

	url = f'https://pepper.ru/search?q={search}'
	#print(url)
	headers = {'user-agent' : ua().chrome}

	adds = {
		'mute--text text--lineThrough size--all-l size--fromW3-xl',
		'thread-price text--b cept-tp size--all-l size--fromW3-xl text--color-greyShade',
		'thread-price text--b cept-tp size--all-l size--fromW3-xl',
	}

	s = requests.Session()
	s.headers = headers

	response = s.get(url)

	if response:
		soup = BS(response.content, 'lxml')
		finder = soup.find_all('article', id = re.compile('^thread'))
		
		if len(finder) == 0:
			print('Found : Nothing')
		
		mb = []
		count = 0
		for v in finder:
			if count >= 10:
				break
			count += 1 

			prices = []
			for j in adds:
				prices.append(v.find('span', attrs={'class':j}))
			prices = [j for j in prices if j != None]
			
			if len(prices) == 0:
				continue
			x = v.find('a', attrs={'class':'cept-tt thread-link linkPlain thread-title--list js-thread-title'})
			#print(x['title'])
			if x: 
				mb.append(x['title'])

		if len(mb) == 0:
			print('Found : Nothing')

		print('\nPossible Options : ')
		for k, v in enumerate(mb, 1):
			print(f'\t{k} | {v}')

		check = int(input('\nInput number: (1 or 2 or 3) : ')) - 1

		question = int(input('Exact search? : (1 = YES || or || Another number = NO) : '))

		search = mb[check]
		search = search.replace(' ', '%20')
		url = f'https://pepper.ru/search?q={search}'

		if question == 1:
			response = s.get(url)

		if response:
			if question == 1:
				soup = BS(response.content, 'lxml')
				finder = soup.find_all('article', id = re.compile('^thread'))

			counter = 0
			for i in finder:
				x = i.find('a', attrs={'class':'cept-tt thread-link linkPlain thread-title--list js-thread-title'}).text
				#print(x)
				
				normalized1 = x.lower()
				normalized2 = search.lower()
				matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
				#print(matcher.real_quick_ratio(), matcher.quick_ratio(), matcher.ratio())
				if matcher.ratio() < 0.35:
					continue

				
				prices = []
				for j in adds:
					prices.append(i.find('span', attrs={'class':j}))

				prices = [j for j in prices if j != None]
				if len(prices) == 0:
					continue
				
				price = prices[0]
				#print(prices)


				discount = i.find('span', attrs={'class':'space--ml-1 size--all-l size--fromW3-xl'})
				#print(discount)
				#print(price)
				ended = i.find('span', attrs={'class':'size--all-s text--color-grey space--l-1 space--r-2 cept-show-expired-threads hide--toW3'})
				if ended:
					continue

				counter += 1

				price = price.text
				price = price.strip('₽')
				price = price.replace(' ', '')
						
				#print(discount)
				if discount != None:
					discount = discount.text
					disc = discount.strip('%()-')
					#print(discount)


					prc = str(round(int(price) * (100 - int(disc))*0.01))
					print(f'\n{x}\nPrice : {price} (Discount : {discount}) || Total : {prc}\n' + '-'*80)
				else:
					print(f'\n{x}\nPrice : {price}\n' + '-'*80)

			if counter != 0:
				print(f'Found : {counter} options')
			else:
				print('Found : Nothing')
if __name__ == '__main__':
	main()