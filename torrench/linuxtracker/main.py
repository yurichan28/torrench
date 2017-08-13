'''
Copyright (C) 2017 Rijul Gulati <kryptxy@protonmail.com>
Licence: GPL(3)
'''

## LinuxTracker.org Module

import os
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

print("""
######################
#                    #
#    LinuxTracker    #                       
#                    #
######################
""")

URL = "http://linuxtracker.org/"
mylist = []
masterlist = []
index_to_name = {}
index_to_dload = {}
categories_dict = {}
categories_dict2 = {}
categ_url_code = 9999

def main(title):
	try:
		print("Fetching...")
		raw = requests.get("http://linuxtracker.org/index.php?page=torrents")
		raw = raw.content
		soup = BeautifulSoup(raw, 'lxml')
		
		# Storing all categories in a dictationary
		count = 1
		categories = soup.find('select', {'name':'category'}).find_all('option')
		categ_len = len(categories)
		show_categ = input("\nView categories? (~700) [y/n]: ")
		
		if show_categ == 'y' or show_categ == 'Y':
			for i in range(categ_len):
				categ_name = categories[i].string
				categ_code = categories[i]['value']
				print("[%d] %s" %(count, categ_name))
				categories_dict[count] = categ_name # Mapping name with index number
				categories_dict2[categ_name] = categ_code # Mapping name with category code
				count+=1
		
			selected_categ = int(input("\nSelect category (0=none) : "))
			try:
				if selected_categ < 0 or selected_categ > categ_len:
					print("Bad input")
				elif selected_categ == 0:
					categ_url_code = 0
					print("category: none\n")
				else:
					selected = categories_dict[selected_categ]
					categ_url_code = int(categories_dict2[selected])
					print("Selected : "+selected)
			except ValueError:
				print("Bad Input!")
				return
		elif show_categ == 'n' or show_categ == 'N':
			categ_url_code = 0
		else:
			print("Bad Input!")
			return
		
		# Content Fetch begins here
		search = "index.php?page=torrents&search=%s&category=%d&active=1" %(title, categ_url_code)
		print("Fetching results...")
		raw = requests.get(URL+search)
		raw = raw.content
		soup = BeautifulSoup(raw, 'lxml')
		content = soup.find_all('table', {'class':'lista', 'width':'100%'})
		search_results = content[4]
		index = 0
		
		for i in search_results:
			try:
				
				name = i.font.a.string
				date = i.find_all('tr')[0].get_text().split(' ')[-2]
				size = i.find_all('tr')[1].td.find(recursive=False, text=True).replace(' ','') 
				seeds = i.find_all('tr')[2].get_text().split(' ')[-2]
				leeches = i.find_all('tr')[3].get_text().split(' ')[-2]
				completed = i.find_all('tr')[4].get_text().split(' ')[-3]
				dload = i.find_all('td', {'align':'right'})[0].find_all('a')[1]['href']
				#thash = i.font.a['href'].split('=')[-1]
				index += 1
				index_to_name[str(index)] = name
				index_to_dload[str(index)] = dload
				mylist = [name, "--"+str(index)+"--", size, seeds, leeches, completed, date]
				masterlist.append(mylist)
					
			except AttributeError:
				pass
		
		if index == 0:
			print("\nNo results for give input!\n")
			return
		print("\nS=Seeds; L=Leeches; C=Completed")
		output = tabulate(masterlist, headers = ['NAME', 'INDEX','SIZE', 'S','L','C', 'ADDED ON',], tablefmt="grid")
		print(output)
		print("\n\nTorrent can be downloaded directly through index\n")
		
		opt = 9999
		while(opt!=0):
			try:
				opt = int(input("(0 = exit)\nindex > "))
				if opt == 0:
					print("\nBye!")
					break
				elif opt < 0 or opt > index:
					print("Bad input!\n\n")
					continue
				else:
					print("Selected index[%s] - " %(opt)+index_to_name[str(opt)])
					download(URL+index_to_dload[str(opt)])
			except ValueError:
				print("\nBad Input\n")
	except KeyboardInterrupt:
		print("\n\nAborted!")
	except Exception as e:
		print(e)
	
	
def download(dload_url):
	try:
		raw = requests.get(dload_url)
		raw = raw.content
		soup = BeautifulSoup(raw, 'lxml')
		link = soup.find_all('td', {'align':'center', 'class':'blocklist'})[-1].a['href']
		dload_response = requests.get(URL+link)
		torrent_name = link.split('&')[1].split('=')[1]
		
		download_location = os.path.expanduser('~/Downloads/torrench/')
		if not os.path.exists(download_location):
			os.makedirs(download_location)
		
		with open(download_location+torrent_name, "wb") as file:
			print("Downloading...")
			response = requests.get(URL+link)
			file.write(response.content)
			print("Download complete!")
			print("\nSaved in "+download_location+"\n")
	except KeyboardInterrupt:
		print("Aborted!")

if __name__ == "__main__":
	print("Its a module")
