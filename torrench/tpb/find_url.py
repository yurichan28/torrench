'''
Copyright (C) 2017 Rijul Gulati <kryptxy@protonmail.com>

'''

from bs4 import BeautifulSoup
import requests	
import sys
import torrench.Torrench as tpb

url = tpb.verify_tpb()
raw = requests.get(url)
raw = raw.content
soup = BeautifulSoup(raw, "lxml")
links = soup.find_all('td', {'title': 'URL'}, limit=2)
links = soup.find_all('td', class_='site', limit=2)
myList = []
def find_url_list():
	for i in links:
		myList.append(i.a["href"]);
	return myList

if __name__ == "__main__":
	print("It's a module. Can only be imported!");
