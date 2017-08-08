'''
Copyright (C) 2017 Rijul Gulati <kryptxy@protonmail.com>
'''

import os
import sys
import time
import platform
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import colorama

colorama.init()
YELLOW = colorama.Fore.YELLOW + colorama.Style.BRIGHT
GREEN = colorama.Fore.GREEN + colorama.Style.BRIGHT
MAGENTA = colorama.Fore.MAGENTA + colorama.Style.BRIGHT
CYAN = colorama.Fore.CYAN + colorama.Style.BRIGHT
RESET = colorama.Style.RESET_ALL

OS_WIN = False

if platform.system() == 'Windows': # Determine platform
	import ctypes
	ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 3)
	os.system("mode CON: COLS=180 LINES=350") # Expand windows console window so output does not overlap (font==default). Change accordingly if necessary
	OS_WIN = True

def main(input_title, page_limit):
    
    ## MAIN CODE EXECUTION BEGINS HERE
    try:
        # Get proxy list
        print("Obtaining proxies...")
        import torrench.tpb.find_url as find_url
        url_list = []
        url_list = find_url.find_url_list()
        print (">>> "+url_list[0]+"\n>>> "+url_list[1])
        print("\n>>> Using " + YELLOW + url_list[0] + RESET)
        
        total_result_count = 0
        page_result_count = 9999
        details_link = {}
        details_name = {}
        magnetic_link_dict = {}
        masterlist = []
        page_fetch_time=0
        total_page_fetch_time=0

        title = input_title.replace(" ", "%20")

        # Traverse on basis of page_limit input
        for p in range(page_limit):

            #initially page_result_count=9999
            # If results in a page are <30, break loop (no more remaining pages are fetched)
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
            url_for_comments = url.split('//')[-1] #required for fetching comments
            search = "/search/%s/%d/99/0" %(title, p)

            while(url_list_count < len(url_list)):
                try:
                    start_time = time.time()
                    raw = requests.get(url+search)
                    page_fetch_time = time.time() - start_time
                    time.sleep(1)
                    raw = raw.content
                    break
                except requests.exceptions.ConnectionError as e:
                    print("Connection error... ")
                    url_list_count += 1
                    url = url_list[url_list_count]
                    print("Trying "+url)
            # End determining proxy site
            soup = BeautifulSoup(raw, "lxml")
            
            # Result for given input found or not?
            try:
                content = soup.find_all('table', id="searchResult")[0]
            except IndexError:
                if p == 0:
                    print("\nNo results found for given input!")
                    break

            data = content.find_all('tr')
            mylist = []
            temp_url = url.split('//')[-1]

            ### Extraction begins here ###
            for i in data[1:]:
                name = i.find('a', class_='detLink')
                uploader = i.find('a', class_="detDesc")
                if name != None and uploader != None:
                    if OS_WIN:
                        try:
                            name = name.string.encode('ascii', 'replace').decode() #Handling Unicode characters in windows.
                        except AttributeError: 
                            name = name.string
                    else:
                        name = name.string
                    uploader = uploader.string
                else:
                    continue
                comments = i.find('img', {'src': '//%s/static/img/icon_comment.gif' %(url_for_comments)})
                if comments != None:
                    comment = comments['alt'].split(" ")[-2] #Total number of comments
                else:
                    comment = "0"
                total_result_count+=1
                page_result_count+=1
                is_vip = i.find('img', {'title': "VIP"})
                is_trusted = i.find('img', {'title': 'Trusted'})
                if(is_vip != None):
                    name = GREEN + name + RESET
                    uploader = GREEN + uploader + RESET
                elif(is_trusted != None):
                    name = MAGENTA + name + RESET
                    uploader = MAGENTA + uploader + RESET	
                categ = i.find('td', class_="vertTh").find_all('a')[0].string
                sub_categ = i.find('td', class_="vertTh").find_all('a')[1].string
                seeds = i.find_all('td', align="right")[0].string
                leeches = i.find_all('td', align="right")[1].string
                date = i.find('font', class_="detDesc").get_text().split(' ')[1].replace(',', "")
                size = i.find('font', class_="detDesc").get_text().split(' ')[3].replace(',', "")
                torr_id = i.find('a', {'class': 'detLink'})["href"].split('/')[2]
                link = url+"/torrent/"+torr_id
                magnet = i.find_all('a', {'title': 'Download this torrent using magnet'})[0]['href']
                ### Extraction ends here ###

                # Storing each row result in mylist
                mylist = [categ+" > "+sub_categ, name, "--"+str(total_result_count)+"--", uploader, size, seeds, leeches, date, comment]
                # Further, appending mylist to a masterlist. This masterlist stores the required result
                masterlist.append(mylist)

                # Dictationary to map torrent name with corresponding link and magnet-link (Used later)
                details_link[str(total_result_count)] = link
                details_name[str(total_result_count)] = name
                magnetic_link_dict[str(total_result_count)] = magnet

            if(page_limit == 1):
                total_page_fetch_time = page_fetch_time
            else:
                print(">> "+str(page_result_count)+" torrents")
                print ("[%.2f sec]" %(page_fetch_time))
                total_page_fetch_time += page_fetch_time

    except KeyboardInterrupt:
        print("\nAborted!\n")
        sys.exit()

    # Print Results and fetch torrent details
    if(total_result_count > 0):
        print("\n\nS=Seeds; L=Leeches; C=Comments")
        final_output = tabulate(masterlist, headers=['TYPE', 'NAME', 'INDEX', 'UPLOADER', 'SIZE','S','L', 'UPLOADED', "C"], tablefmt="grid")
        print(final_output)
        print("\nTotal: "+str(total_result_count)+" torrents"+" [in %.2f sec]" %(total_page_fetch_time))
        exact_no_of_pages = total_result_count//30
        has_extra_page = total_result_count%30
        if has_extra_page > 0:
            exact_no_of_pages +=1
        print("Total pages: "+str(exact_no_of_pages))
        print("\nFurther, a torrent's details can be fetched (Description, comments, download(Magnetic) Link, etc.)");

        # Fetch torrent details
        import torrench.tpb.details as details
        print("Enter torrent's index value to fetch details (Maximum one index)\n")
        option = 9999
        option2 = 0
        while(option != 0):
            try:
                option = int(input("(0 = exit)\nindex > "))
                if option > total_result_count or option < 0 or option == "":
                    print("**Enter valid index**\n\n")
                    continue
                elif option == 0:
                    break
                else:
                    selected_link = details_link[str(option)]
                    selected_name = details_name[str(option)]
                    required_magnetic_link = magnetic_link_dict[str(option)]

                    print("\nSelected - "+selected_name+"\n")
                    option2 = input("1. Download this torrent using magnet [d]\n2. Get torrent details [g]\n\nOption [d/g]: ")
                    if option2 == 'd' or option2 == 'g':
                        if option2 == 'd':
                            print("\nMagnetic link - "+required_magnetic_link+"\n")
                            import webbrowser
                            try:
                                webbrowser.open_new_tab(required_magnetic_link)
                            except Exception as e:
                                print(e)
                            continue
                        elif option2 == 'g':
                            print("Fetching details for torrent index [%d] : %s" %(option, selected_name))
                            file_url = details.get_details(selected_link, str(option))
                            file_url = YELLOW + file_url + RESET
                            print("File URL: "+file_url+"\n\n")
                    else:
                        print("Bad Input!\n")
                        continue
            except KeyboardInterrupt:
                break
            except ValueError:
                print("Check input! (Enter one (integer) index at a time)\n\n")
        print("\nBye!\n")

if __name__ == "__main__":
    print("It's a module.")
