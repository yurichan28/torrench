## Module for finding TPB/KAT Proxies
## URL is fetched from check_config

from bs4 import BeautifulSoup
import requests	
import torrench.utilities.check_config as config

'''
Function to fetch 'url' page and prepare soup
'''
def http_request(url):
	raw = requests.get(url)
	raw = raw.content
	soup = BeautifulSoup(raw, 'lxml')
	return soup

'''
Function to obtain proxy list and return that list to caller
'''
def get_proxy_list(name, soup):
	urlList = []
	if name == 'tpb':
		links = soup.find_all('td', class_='site')
	elif name == 'kat':
		data = soup.find('table', class_='table')
		links = data.find_all('td', class_='text-left')
		
	for i in links:
		urlList.append(i.a["href"]);
	return urlList

'''
function to obtain web URL from which proxies are fetched
'''
def proxy_list(name):
	if name == 'tpb':
		url = config.get_tpb_url()
	elif name == 'kat':
		url = config.get_kat_url()
	soup = http_request(url)
	output = get_proxy_list(name, soup)
	return output

if __name__ == "__main__":
	print("Its a module")
