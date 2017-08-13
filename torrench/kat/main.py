'''
Copyright (C) 2017 Rijul Gulati <kryptxy@protonmail.com>
Licence: GPL(3)
'''

## KickassTorrents main module

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import colorama
import time
import webbrowser
import platform
import torrench.kat.find_url as find_url

print("""
#########################
#                       #
#    KickAssTorrents    #                       
#                       #
#########################
""")

OS_WIN = False
if platform.system() == 'Windows':
	OS_WIN = True

colorama.init()
YELLOW = colorama.Fore.YELLOW + colorama.Style.BRIGHT
GREEN = colorama.Fore.GREEN + colorama.Style.BRIGHT
RED = colorama.Fore.RED + colorama.Style.BRIGHT
RESET = colorama.Style.RESET_ALL

def main(title, page_limit):
	try:
		# Get proxy list
		print("\nObtaining proxies...")
		url_list = []
		url_list = find_url.find_url_list()
		print(">>> %s\n>>> %s\n>>> %s" %(url_list[0], url_list[1], url_list[2]))
		print("\n>>> Using " + YELLOW + url_list[0] + RESET)
		
		page_result_count=9999
		master_list = []
		map_name_index = {}
		map_magnet_index = {}
		map_torrlink_index = {}
		index = 0 ## Torrent index value variable
		total_page_fetch_time = 0 ## Time take to fetch all pages
		
		for p in range(page_limit):
		
			if page_result_count < 30:
					break
			
			if page_limit > 1:
				fetch_status_str = "\nFetching from page: "+str(p+1)
				print(fetch_status_str)
			else:
				print("Fetching results...")
			
			page_result_count = 0
			url_list_count = 0
			url = url_list[url_list_count]
			search = "/usearch/%s/%d/" %(title, p+1)
		
			while(url_list_count < len(url_list)):
				try:
					start_time = time.time()
					raw = requests.get(url+search)
					page_fetch_time = time.time() - start_time  ## page_fetch_time = time take to fetch ONE page
					time.sleep(0.5)
					raw = raw.content
					break
				except requests.exceptions.ConnectionError:
					print("Connection error... ")
					url_list_count += 1
					url = url_list[url_list_count]
					print("Trying "+url)
			
			soup = BeautifulSoup(raw, "lxml")		
			
			content = soup.find_all('table', class_='data')[0]
			
			data = content.find_all('tr', class_='odd')
			
			# Results for given input found or not?
			if data == []:
				print("\nNo results found for given input!\n")
				return
				
			mylist = []
			## Torrent fetch begins here
			for i in data:
				name = i.find('a', class_='cellMainLink')
				if OS_WIN:
					try:
						name = name.string.encode('ascii', 'replace').decode() # Handling Unicode characters in windows.
					except AttributeError: 
						name = name.string
				else:
					name = name.string
				torrent_link = i.find('a', class_='cellMainLink')['href']
				uploader_name = i.find('span', class_='lightgrey').get_text().split(" ")[-4]
				category = i.find('span', class_='lightgrey').get_text().split(" ")[-2]
				verified_uploader = i.find('a', {'title': 'Verified Torrent'})
				if verified_uploader != None:
					uploader_name = YELLOW + uploader_name + RESET
					verified = True
				comment_count = i.find('a', class_='icommentjs').get_text()
				if comment_count == " ":
					comment_count = 0
				misc_details = i.find_all('td', class_='center')
				size = misc_details[0].string
				date_added =  misc_details[1].string
				seeds = misc_details[2].string
				seeds = GREEN + seeds + RESET
				leeches = misc_details[3].string
				leeches = RED + leeches + RESET
				magnet = i.find('a', {'title': 'Torrent magnet link'})['href']
				index += 1
				page_result_count += 1
				
				mylist = [category, name, '--'+str(index)+'--', uploader_name, size, date_added, seeds, leeches, comment_count]
				master_list.append(mylist)
				
				map_name_index[str(index)] = name
				map_magnet_index[str(index)] = magnet
				map_torrlink_index[str(index)] = torrent_link
		
			if(page_limit == 1):
				total_page_fetch_time = page_fetch_time
			else:
				print(">> "+str(page_result_count)+" torrents")
				print ("[%.2f sec]" %(page_fetch_time))
				total_page_fetch_time += page_fetch_time
			
				
		## Display fetched results
		total_result_count = index	
		
		if total_result_count > 0:
			result = tabulate(master_list, headers=['CATEG', 'NAME', 'INDEX', 'Uploader', 'SIZE', 'DATE', 'S', 'L', 'C'], tablefmt='grid') 
			print("\n\nS=SEEDS; L=LEECHES; C=COMMENTS; "+ YELLOW+"YELLOW UPLOADERS "+RESET+"are Verified Uploaders")
			print(result)
			print("\nTotal: "+str(total_result_count)+" torrents"+" [in %.2f sec]" %(total_page_fetch_time))
			
			exact_no_of_pages = total_result_count//30
			has_extra_page = total_result_count%30
			if has_extra_page > 0:
				exact_no_of_pages +=1
			print("Total pages: "+str(exact_no_of_pages))
				
			print("\nFurther, torrent can be downloaded using magnetic link\n__OR__ Torrent's upstream link can be obtained to be opened in web browser.")
			print("\nEnter torrent's index value (Maximum one index)")

			index=999
			while(index!=0):
				try:
					index = int(input("\n\n(0=exit)\nindex > "))
				except ValueError:
					print("\nBad Input! Try again.\n")
				if index < 0 or index > total_result_count:
					print("Invalid input!")
					continue
				elif index == 0:
					print("\nBye!\n")
					break
				selected_torrent = map_name_index[str(index)]
				req_magnetic_link = map_magnet_index[str(index)]
				req_torr_link = map_torrlink_index[str(index)]
				
				if verified:
					selected_torrent = YELLOW + selected_torrent + RESET
				print("Selected index [%d] - %s\n" %(index, selected_torrent))
				
				option = input("[d] Download this torrent using magnet [d]\n[g] Get upstream link [g]\n\nOption [d/g]: ")
				if option == 'd' or option == 'g':
					if option == 'd':
						print("\nMagnetic link - "+req_magnetic_link+"\n")
						try:
							webbrowser.open_new_tab(req_magnetic_link)
						except Exception as e:
							print(e)
							continue
					elif option == 'g' or option == 'G':
						print("\nTorrent link: %s\n" %(YELLOW + url+req_torr_link + RESET))
						uinput = input("Open in browser? [y/n]: ")
						if uinput == 'y' or uinput == 'Y':
							webbrowser.open_new_tab(url+req_torr_link)
							continue
						elif uinput == 'n' or uinput == 'N':
							pass
				else:
					print("Bad Input")
					continue
	except KeyboardInterrupt as e:
		print("\nAborted!\n")
