'''
Copyright (C) 2017 Rijul Gulati <kryptxy@protonmail.com>

This file is part of Torrench.

Torrench is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Torrench is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>. 
'''

from bs4 import BeautifulSoup
import requests
import os;
import time

def get_details(url, index):
	
	home = os.path.expanduser('~')
	main_dir = home+"/.torrench/"
	temp_dir = main_dir+"temp/"
	
	raw = requests.get(url);
	raw = raw.content
	unique_id = url.split('/')[-1]
	file_name = unique_id+".html"
	soup = BeautifulSoup(raw, "lxml")
	
	content = soup.find('div', id="details")
	nfo = str(content.find_all('div', class_="nfo")[0])
	dt = content.find_all('dt')	# Torrent info table headers
	dd = content.find_all('dd')	# info table values
	title = "(Index: "+index+") - "+str(soup.find('div', id="title").string)
	name = str(soup.find('div', id="title"))
	magnet = soup.find('div', class_="download").a["href"]
	
	#FETCHING COMMENTS
	comments_list=[]
	commenter_list=[]
	
	# Fetching comments of base (default) page
	comments = soup.find_all('div', class_='comment')
	commenter = soup.find(id="comments").find_all('p')
	comments_list.append(comments)
	commenter_list.append(commenter)
	
	#Determine if any other comment pages are present. 
	total_comments_pages = soup.find('div', class_='browse-coms') #Total number of comment pages
	if total_comments_pages!=None:
		total_comments_pages = int(soup.find('div', class_='browse-coms').strong.string)
		print("\n%d comment pages (1 page = 25 comments (MAX))" %(total_comments_pages))			
		temp=True
		pg_count=0
		if(total_comments_pages>2): ## If more than 3 comment pages are present, ask user what to do.
			while(temp):
				opt = input("Fetch all pages? May take longer [y/n/display anyway[d]]: ")
				if opt=='y' or opt =='Y':
					pg_count = 0
					temp=False
				elif opt=='n' or opt=='N':
					pg_inp = input("Number of pages to fetch comments from? [0 < n < %d]: " %(total_comments_pages));
					if pg_inp=='':
						print("Bad Input")
					else:
						pg_inp = int(pg_inp)
						if pg_inp < total_comments_pages and pg_inp > 0:
							pg_count = total_comments_pages-pg_inp
							temp=False
						else:
							print("Bad Input")	
				elif opt=='d':
					pg_count=total_comments_pages
					temp=False
				else:
					print("Bad Input")
					
		print("\nLast page (%d) [Already fetched]" %(total_comments_pages))
		total_comments_pages-=1 # Since last page is already fetched. So start from (n-1)th page
		
		while(total_comments_pages>pg_count):
			start_time=time.time()
			raw = requests.get(url, params={'page': total_comments_pages})
			end_time = time.time() - start_time
			print("Page "+str(total_comments_pages)+" [%.2f sec]" %(end_time))
			raw = raw.content
			soup2 = BeautifulSoup(raw, "lxml")
			comments = soup2.find_all('div', class_='comment')
			commenter = soup2.find(id="comments").find_all('p')
			comments_list.append(comments)
			commenter_list.append(commenter)
			total_comments_pages-=1
			
	
	torrent_hash = soup.find('div', class_="download").a["href"].split('&')[0].split(':')[-1]
	torrent_hash = torrent_hash.upper()
	
	## Set torrent hash explicitly as it is not fetched directly as other dd elements
	dd[-1].string = torrent_hash
	
	# Check Uploader-Status
	style_tag = "<style> pre {white-space: pre-wrap; text-align: left} h2, .center {text-align: center;} .vip {color: #32CD32} .trusted {color: #FF00CC}  body {margin:0 auto; width:70%;} table, td, th {border: 1px solid black;} td, th {text-align: center; vertical-align: middle; font-size: 15px; padding: 6px} .boxed{border: 1px solid black; padding: 3px} </style> "
	begin_tags = "<!DOCTYPE html><html><head><meta http-equiv='Content-type' content='text/html;charset=utf-8'> <title>"+title+"</title>"+style_tag+"</head><body>"
	end_tags = "</body></html>"

	# File opens here
	if not os.path.exists(temp_dir):
		os.makedirs(temp_dir)	
	f = open(temp_dir+unique_id+".html", "w")
	f.write(begin_tags)
	f.write("<h2><u><a href="+url+" target='_blank'>"+name+"</a></u></h2><br />")
	f.write("<table align='center'>")

	# Torrent info table
	for i in dt:
		dt_str = str(i.get_text()).replace(":", "")
		f.write("<th>"+dt_str+"</th>")
	f.write("</tr>\n<tr>\n")
	status=""
	for j in dd:
		dd_str = str(j.get_text()).replace(":", "")
		if j.img != None:
			if j.img['title'] == 'VIP':
				dd_str = "<div class='vip'>"+dd_str+"</div>"
				status='vip'
			elif j.img['title'] == 'Trusted':
				dd_str = "<div class='trusted'>"+dd_str+"</div>"
				status='trusted'	
		f.write("<td>"+dd_str+"</td>")
		
	f.write("</tr></table>")
	
	if status=='vip':
		f.write("<div class='vip'> *VIP Uploader </div>")
	elif status=='trusted':
		f.write("<div class='trusted'> *Trusted Uploader </div>")
	
	f.write("<br />")
		
	# Magnetic link[1]
	f.write("<div class='center'><a href="+magnet+" target='_blank'>[Magnetic Link (Download)]</a></div><br />")

	# Printing Description
	f.write("<div class='boxed'>")
	f.write("<h2><u> DESCRIPTION </u></h2>")
	f.write("<pre>")
	f.write(nfo)
	f.write("</pre></div>")
	f.write("<div class='boxed'>")
	f.write("<h2><u> COMMENTS </u></h2>")
	#End Description
	
	count=1
	#Printing Comments
	if commenter_list != [] and commenter_list[0]!=[]:
		f.write("<table align='center'>")
		for k in range(len(commenter_list)):
			for i, j in zip(commenter_list[k], comments_list[k]):
				f.write("<tr><th>"+str(i.get_text())+"</th>")
				f.write("<td><pre>"+str(j.get_text())+"</pre></td></tr>")
				count+=1
		f.write("</table><br />");
		f.write("<div class=center> (Total %d comments) </div>" %(count))
	else:
		f.write("<pre class='center>No comments found!</pre></div>") 
		f.write("</div><br />");
	# End Comments
	# Magnetic link[2]
	f.write("<br /><div class='center'><a href="+magnet+" target='_blank'>[Magnetic Link (Download)]</a></div><br /><br />")
	f.write(end_tags);
	f.close();
	
	file_url = "file://"+temp_dir+file_name
	return file_url
	
if __name__ == "__main__":
	print("It's a module. Can only be imported!");
	
