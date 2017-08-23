'''
To check if configuration file is present and enabled to use TPB/KAT
Also defines config files's directory structure.

For Linux, default config file location is: $HOME/.config/torrench/
For Windows: ~\.config\torrench\
'''

import os
from configparser import SafeConfigParser

config = SafeConfigParser()
config_dir = os.path.expanduser(os.path.join('~', '.config'))
full_config_dir = os.path.join(config_dir, 'torrench')
config_file_name = "config.ini"
config_file = os.path.join(full_config_dir, config_file_name)

'''
Function to check if config file exists
Return true if it does
'''
def file_exists():
	if os.path.isfile(config_file):
		config.read(config_file)
		enable = config.get('Torrench-Config', 'enable')
		if enable == '1':
			return True
'''
Get TPB URL
'''
def get_tpb_url():
	config.read(config_file)
	url = config.get('Torrench-Config', 'TPB_URL')
	return url

'''
Get KAT URL
'''
def get_kat_url():
	config.read(config_file)
	url = config.get('Torrench-Config', 'KAT_URL')
	return url
