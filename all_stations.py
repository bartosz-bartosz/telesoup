import requests
from bs4 import BeautifulSoup
import re
import pickle

hrefs = []
link = 'https://www.telemagazyn.pl/stacje/'
def get_soup():
    source = requests.get(link).text
    soup = BeautifulSoup(source, features='html.parser')	
    return soup


def get_links(soup):
	for div in soup.find_all('div', class_='column'):
		#print(div)
		for li_tag in div.find_all('li'):
			#print(li_tag)
			for href in li_tag.find_all('a', href=True):
				#print(href['href'])
				href = href['href']
				if href != '/':
					hrefs.append(href)


get_links(get_soup())

print(hrefs)

with open('all_links.pkl', 'wb') as links:
	pickle.dump(hrefs, links)
