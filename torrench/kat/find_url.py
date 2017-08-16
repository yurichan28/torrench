## Module for finding KAT Proxies
## URL is fetched from check_config module

from bs4 import BeautifulSoup
import requests	
import sys
import torrench.check_config as check_config

url = check_config.get_kat_url()
raw = requests.get(url)
raw = raw.content
soup = BeautifulSoup(raw, "lxml")
data = soup.find('table', class_='table')
links = data.find_all('td', class_='text-left')

myList = []
def find_url_list():
	for i in links:
		myList.append(i.a["href"]);
	return myList

if __name__ == "__main__":
	print("It's a module")
