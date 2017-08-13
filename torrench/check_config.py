'''
Copyright (C) 2017 Rijul Gulati <kryptxy@protonmail.com>
Licence: GPL(3)
'''

## To check if configuration file is present and enabled to use TPB/KAT
## Also defines config files's directory structure.

## For Linux, default config file location is: $HOME/.config/torrench/
## For Windows: ~\.config\torrench\

import os
import sys
import platform
from configparser import SafeConfigParser
config = SafeConfigParser()

def main():

	config_dir = os.path.expanduser('~/.config')
	sub_config_dir = "torrench/"
	config_file_name = "config.ini"
	if platform.system() == 'Windows':	
		# Windows conf file resides in ~\.config\tpb\
		config_dir = os.path.expanduser('~\.config')
		sub_config_dir = "torrench\\"
		
	full_config_dir = os.path.join(config_dir, sub_config_dir) # Joining config_dir and sub_config_dir
	
	if not os.path.exists(full_config_dir):
		os.makedirs(full_config_dir) # Create ~/.config/torrench directory if it doesn't exist
		
	config_error = "\nConfig file found, but disabled. Please enable to continue. Read documentation for instructions.\n"
	config_error2 = "\nNo config file found in %s.\nPlease read documentation for config file setup instructions.\n" %(full_config_dir)
	
	config_file = os.path.join(full_config_dir, config_file_name) # Config file location
	
	# If file exists, pass. Else show error
	if os.path.isfile(config_file):
		config.read(config_file)
		enable = config.get('Torrench-Config', 'enable')
		if enable != '1':
			print(config_error)
			sys.exit(0)
		else:
			pass
	else:
		print(config_error2) 
		sys.exit(0)

def get_tpb_url():
	url = config.get('Torrench-Config', 'TPB_URL')
	return url

def get_kat_url():
	url = config.get('Torrench-Config', 'KAT_URL')
	return url
	
	
	
	
	
	
	
