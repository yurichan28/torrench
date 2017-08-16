'''
Modified for DistroWatch by Jesse Smith <jsmith@resonatingmedia.com>
'''

import os
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import colorama
colorama.init()
YELLOW = colorama.Fore.YELLOW + colorama.Style.BRIGHT
RESET = colorama.Style.RESET_ALL

print("""
#####################
#                   #
#    DistroWatch    #                       
#                   #
#####################
""")

URL = "https://distrowatch.com"

# Torrent's .torrent files are downloaded in $HOME/Downloads/torrench directory
home = os.path.expanduser(os.path.join('~', 'Downloads'))
downloads_dir = os.path.join(home, 'torrench')

mylist = []
masterlist = []
urllist = []
index_to_name = {}
index_to_dload = {}
categories_dict = {}
categories_dict2 = {}
categ_url_code = 9999

def main(title):
	try:
		print("Search input : "+title)
		title = title.lower()
		print("Fetching results...\n")
		raw = requests.get("https://distrowatch.com/dwres.php?resource=bittorrent")
		raw = raw.content
		soup = BeautifulSoup(raw, 'lxml')
		content = soup.find_all('td', 'torrent')
		torrent_date = soup.find_all('td', 'torrentdate')
		index = 0
		
		for i, j in zip(content, torrent_date):
			try:
				link = i.find('a')
				url = "https://distrowatch.com/" + link.get('href')
				name = link.string
				name = name.lower()
				if title in name:
					date = j.string
					index += 1
					index_to_name[str(index)] = name
					mylist = [name, "--"+str(index)+"--", date]
					masterlist.append(mylist)
					urllist.append(url)
					
			except AttributeError:
				pass
		
		if index == 0:
			print("\nNo results for give input!\n")
			return
		output = tabulate(masterlist, headers = ['NAME', 'INDEX', 'UPLOADED'], tablefmt="grid")
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
					print("\nSelected index [%s] - " %(opt)+YELLOW+index_to_name[str(opt)]+RESET)
					download(urllist[opt-1])
			except ValueError:
				print("\nBad Input\n")
	except KeyboardInterrupt:
		print("\n\nAborted!")
	except Exception as e:
		print(e)

def download(dload_url):
	try:
		print("Downloading ", dload_url)
		dload_response = requests.get(dload_url)
		torrent_name = dload_url.split('/')
		torrent_name = torrent_name[5]
		
		if not os.path.exists(downloads_dir):
			os.makedirs(downloads_dir)
		
		with open(os.path.join(downloads_dir, torrent_name), "wb") as file:
			response = requests.get(dload_url)
			file.write(response.content)
			print("Download complete!")
			print("\nSaved in %s \n" %(downloads_dir))
	except KeyboardInterrupt:
		print("Aborted!")

if __name__ == "__main__":
	print("Its a module")
