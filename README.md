# Torrench - Command-line torrent search tool
Torrench is a command-line torrent search tool that fetches torrents and displays results **within console window**. It does this by scrapping torrent-hosting websites (list below). Once torrent results are fetched, torrench can further fetch torrent details as well. Details include torrent Description, comments, as well as download link/file.

_Current version - v1.0.0.20170806_

_Torrench initially began as a python learning project for me. I am sure there are ways to implement code I wrote in a better/efficient way. If you find any, please [let me know](https://github.com/kryptxy/torrench#contact)._

_I'll continue updating it, add new features and try making it better and more efficient._

## Compatibility
It's compatible under **Linux and Windows** operating systems. 
As for MacOS, I don't own any mac hardware. If anyone wants to help porting it onto apple, feel free to do so.

## Websites Supported
1. linuxtracker.org - Download linux distros ISO torrents **[default]**
2. The Pirate Bay (TPB) - [REQUIRES CONFIGURATION. READ CAREFULLY BEFORE USING](https://github.com/kryptxy/torrench#should-i-use-thepiratebay)

## Installation
### Linux
1. Requires [Python3](https://www.python.org/downloads/) and python3-pip,
2. Installing

	2.1 From source
	```bash
	$ sudo python3 setup.py install
	```
	
	2.2 Using pip ([PyPI](https://pypi.python.org/pypi/torrench/))
	```
	sudo -H python3 -m pip install torrench
	```
	
### Windows
Windows does not require any additional packages. Everything required to run this software is provided in executable (Does not even require python pre-installed).

* Download [torrench.exe](https://ln.sync.com/dl/bea8abc90/bbtdxg2w-3inaqjb4-z4btacg5-9e8i9a3b) executable
* That's it. Run using cmd/powershell [```> torrench.exe <search>```]

	* NOTE: 
		* Windows powershell is unable to display magenta color. When I tried, the _name_ field was appearing empty. So to distinguish trusted uploaders, I have added a cyan-colored (\**) in front and at the back of TORRENT NAME and UPLOADER NAME. 
		* In windows, the default location for storing html files is ```C:\Users\<user>\.torrench\temp```


## Should I use ThePirateBay?
By default, searching thepiratebay (TPB) from torrench is disabled. Some configuration is required to be done by user to enable TPB.
But, before moving to configuration, note the following:

* Using TPB in many countries is illegal. Using TPB can get you into un-intended troubles (e.g notices/block from ISP). Read [Legal issues](https://en.wikipedia.org/wiki/The_Pirate_Bay#Legal_issues)
* Neither I, nor the tool will be held responsible for any action taken against user for using TPB from torrench.
* Examples of [illegal contents](https://github.com/kryptxy/torrench#illegal-searches-should-not-be-practiced) on TPB. 

#### Configuration instructions (If you decided to use it anyways):
1. Download [config.ini](https://ln.sync.com/dl/26cd652e0/nqzvd8b3-9gqs3pdu-32btqm2c-9r6mbymm) file (Hosted on sync)
	* **Windows -** Copy the config file in ```C:\Users\<user>\.config\tpb\``` (create any missing directories)
	* **Linux -** Copy the config file to ```$HOME/.config/tpb/``` (Create any missing directories)
2. Config file needs to be enabled
	* Open config.ini file
	* Set ```enable=1```
	* Save and exit
3. That's it. Use with ``` (-t) flag```

# Features 
* Supports all \*nix distros
* Simple to use.
* Display search results in organized, tabular form.
* Supports filtering search using categories
* **[TPB_Specific]** Surf torrents Ad-free
* **[TPB-Specific]** Get complete torrent details (Description, comments, torrent download). Torrent details are available in dynamically-generated HTML pages.
* **[TPB-Specific]** Display colored results on basis of uploader's status (Very useful when choosing torrent). (If you are familiar with thepiratebay, you must be knowing that it divides uploaders into 3 categories)
	* VIP Uploader [_green-skull_]
	* Trusted Uploader [_magenta-skull_]
	* General Uploader
* **[TPB-Specific]** Fetch Torrents on basis of pages [1 page yields 30 results (max)].
* **[TPB-Specific]** Fetch Comments on basis of pages [Useful when torrent has large number of comments, and not all comments are intended to be fetched].

## Usage (with example)
```bash
## Input should to precise to get better/expected results

usage: torrench [-h] [-t] [-p LIMIT] [-c] [-v] [search]

Command-line torrent search tool.

positional arguments:
  search                Enter search string

optional arguments:
  -h, --help            show this help message and exit
  -t, --thepiratebay    Search ThePirateBay (TPB)
  -p LIMIT, --page-limit LIMIT
                        Number of pages to fetch results from (1 page = 30
                        results). [default: 1]
  -c, --clear-html      Clear all [TPB] torrent description HTML files and
                        exit.
  -v, --version         Display version and exit.
  
EXAMPLE: 
$ torrench "ubuntu 16.10" - Fetches torrents for ubuntu 16.10
$ torrench "arch linux" - Fetches torrents for Arch Linux
```

# Samples
## Linux

```bash
$ torrench "opensuse"
```
![linux-1](/images/screenshots/legal-1-linux.png)
![linux-2](/images/screenshots/legal-2-linux.png)

## Windows
``` 
> torrench.exe "ubuntu"
```
![windows-1](/images/screenshots/legal-1.PNG)

```
> torrench.exe "fedora workstation 26"
```
![windows-1](/images/screenshots/powershell-1.PNG)
![windows-2](/images/screenshots/powershell-2.PNG)

## Illegal searches (Should not be practiced)
```
> torrench.exe -t "fast 8"
```
![windows-1-illegal](/images/screenshots/win-1-illegal.PNG)

```
> torrench.exe -t "suits s05e08"
```
![windows-2-illegal](/images/screenshots/win-2-illegal.PNG)

```bash
$ torrench -t "windows"
```
![linux-illegal](/images/screenshots/illegal.png)

## Known Issues (and Workarounds)
1. A torrent might take very long to fetch results. I have generally faced this issue when running torrench for the first time. I still got to figure this out. Till then, here is what I do:
	* Abort the ongoing search [Ctrl+C]
	* Search again. The second time generally works fine.

### Note
* Each and every detail you will see on the terminal/HTML page is fetched from the website. If some info is  missing/unintended, it's probably how its available on website.
* **[TPB-specific]** All torrent comments can be fetched.
	* Comments are divided into pages. 1 page can have MAX 25 comments. 
	If (suppose) a torrent has <=50 comments (2 pages), no prompt occurs.
	If a torrent has more than 50 comments, you will get a prompt asking number of pages to fetch.
	Options:
		* (fetch all): Fetch all pages
		* (enter n): Enter number of pages to fetch
		* (d): "display anyway" - Do not fetch any extra pages. By default the latest comments (comments on last page are fetched).

	Fetching comments pages can be time-costly. For every comment page, entire new HTML page is fetched.

## Disclaimer
This tool only fetches torrent and details from already existing torrent website(s). I do not take any responsibility for availability of any kind of torrent data, or/and hosting of any torrent website(s). Also, I am  not responsible for closing of any of the torrent website(s). As long as the website(s) (proxies) are available, data will be fetched.

## Bug Report
Found a bug? Please report and help improving this tool. You can [Open Issue](https://github.com/kryptxy/torrench/issues/new) or contact me directly.

## Feedback/Suggestions/Feature Requests 
Feedbacks/Suggestions are much appreciated. They help in improving the tool, and keep me motivated. 

## Contact
E-mail : kryptxy@protonmail.com

## Licence

```
Copyright (C) 2017 Rijul Gulati <kryptxy@protonmail.com>

Torrench is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Torrench is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Torrench.  If not, see <http://www.gnu.org/licenses/>.
```
