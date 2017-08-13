'''
Copyright (C) 2017 Rijul Gulati <kryptxy@protonmail.com>
Licence: GPL(3)
'''

#! /usr/bin/python3

import platform
import os
import sys
import argparse
import torrench.check_config as check_config
import torrench.Torrench as Torrench

# temp directory to store TPB custom HTML files
home = os.path.expanduser('~/.torrench')
temp_dir = os.path.join(home, "temp")	
if platform.system() == 'Windows':
	from multiprocessing import Queue
	home = os.path.expanduser('~\.torrench')

def main():
	parser = argparse.ArgumentParser(description="Command-line torrent search tool.")
	parser.add_argument("-t", "--thepiratebay", action="store_true", help="Search thepiratebay")
	parser.add_argument("-k", "--kickasstorrent", action="store_true", help="Search KickassTorrent (KAT)")
	parser.add_argument("search", help="Enter search string", nargs="?", default=None)
	parser.add_argument("-p", "--page-limit", type=int, help="Number of pages to fetch results from (1 page = 30 results).\n [default: 1]", default=1, dest="limit")
	parser.add_argument("-c", "--clear-html", action="store_true", default=False, help="Clear all [TPB] torrent description HTML files and exit.")
	parser.add_argument("-v", "--version", action='version', version='%(prog)s 1.0.3', help="Display version and exit.")
	args = parser.parse_args()
	resolve_args(args)
	
def resolve_args(args):   
	input_title = args.search
	page_limit = args.limit

	if args.clear_html:    
		if args.thepiratebay:
			try:
				files = os.listdir(temp_dir)
			except FileNotFoundError:
				print("Directory not initialised. Exiting.")
				sys.exit(0)
			if not files:
				print("\nNothing to remove\n")
			else:
				for count, file_name in enumerate(files, 1):
					os.remove(os.path.join(temp_dir, file_name))
				print("\nRemoved {} file(s).\n".format(count))
			sys.exit(0)
		else:
			print("error: use -c with -t ")
			sys.exit(0)

	if input_title == None:
		print("\nInput string expected.\nUse --help for more\n")
		sys.exit(0)
	
	elif page_limit <= 0 or page_limit > 50:
		print("Enter valid page input [0<p<=50]")
		sys.exit(0)

	else:
		if args.thepiratebay or args.kickasstorrent:
			check_config.main()
			if args.thepiratebay: 
				Torrench.main(input_title, page_limit, 1) ## 1 means TPB
			elif args.kickasstorrent:
				Torrench.main(input_title, page_limit, 2) ## 2 means KAT
		else:
			Torrench.main(input_title, None, None)

if __name__ == "__main__":
	main()
