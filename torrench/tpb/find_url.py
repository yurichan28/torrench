'''
Copyright (C) 2017 Rijul Gulati <kryptxy@protonmail.com>
Licence: GPL(3)
'''

## Module for finding TPB Proxies
## URL is fetched from check_config module

from bs4 import BeautifulSoup
import requests	
import sys
import torrench.check_config as check_config

url = check_config.get_tpb_url()
raw = requests.get(url)
raw = raw.content
soup = BeautifulSoup(raw, "lxml")
links = soup.find_all('td', class_='site', limit=7)
myList = []
def find_url_list():
	for i in links:
		myList.append(i.a["href"]);
	return myList

if __name__ == "__main__":
	print("It's a module. Can only be imported!");
