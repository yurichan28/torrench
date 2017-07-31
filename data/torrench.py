#! /usr/bin/python3

'''
Copyright (C) 2017 Rijul Gulati <kryptxy@protonmail.com>
'''

import os
import sys
import argparse
import platform
from configparser import SafeConfigParser

config = SafeConfigParser()

home = os.path.expanduser('~/.torrench')
temp_dir = os.path.join(home, "temp")
WIN_TPB_CONF = "tpb\conf"
LINUX_TPB_CONF = "data/tpb/conf"
config_file_name = "config.ini"
OS_WIN = False

if platform.system() == 'Windows':
	from multiprocessing import Queue
	home = os.path.expanduser('~\.torrench')
	OS_WIN = True

# Verify if TPB-config file is present
def verify_tpb():
	
	if OS_WIN:
		tpb_config_dir = os.path.join(home, WIN_TPB_CONF)
	else:
		tpb_config_dir = os.path.join(home, LINUX_TPB_CONF)
		
	tpb_config_error = "\nPlease configure config.ini file to continue. Read documentation for instructions."
	tpb_config_error2 = "\nNo config file found in %s.\nPlease read documentation for config file setup instructions." %(tpb_config_dir)
	
	if not os.path.exists(tpb_config_dir):

		os.makedirs(tpb_config_dir)
		
	config_file = os.path.join(tpb_config_dir, config_file_name)
	if os.path.isfile(config_file):
		config.read(config_file)
		enable = config.get('TPB-Config', 'enable')
		if enable != '1':
			print(tpb_config_error)
			sys.exit(0)
		else:
			url = config.get('TPB-Config', 'URL')
			return url
	else:
		print(tpb_config_error2) 
		sys.exit(0)

# Command-line arguments	
def args():
	parser = argparse.ArgumentParser(description="Command-line torrent search tool.")
	parser.add_argument("-t", "--thepiratebay", action="store_true", help="Search thepiratebay")
	parser.add_argument("search", help="Enter search string", nargs="?", default=None)
	parser.add_argument("-p", "--page-limit", type=int, help="Number of pages to fetch results from (1 page = 30 results).\n [default: 1]", default=1, dest="limit")
	parser.add_argument("-c", "--clear-html", action="store_true", default=False, help="Clear all [TPB] torrent description HTML files and exit.")
	parser.add_argument("-v", "--version", action='version', version='%(prog)s v1.0', help="Display version and exit.")
	args = parser.parse_args()
	resolve_args(args)

# Resolving arguments
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
		if args.thepiratebay:
			verify_tpb()
			import tpb.main as tpb
			print("Indexing TPB...")
			tpb.main(input_title, page_limit)
		else:
			print("\nlinuxtracker.org\n")
			print("*Input should be precise for better results*")
			import linuxtracker.main as linuxtracker
			linuxtracker.main(input_title)

if __name__ == "__main__":
	args()
