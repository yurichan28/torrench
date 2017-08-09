# Torrench - Command-line torrent search tool
![Build Status](https://travis-ci.org/kryptxy/torrench.svg?branch=master)
[![GitHub release](https://img.shields.io/github/release/kryptxy/torrench.svg)]()
[![PyPI](https://img.shields.io/pypi/v/torrench.svg)](https://pypi.python.org/pypi/torrench/)
[![AUR](https://img.shields.io/aur/version/torrench.svg)](https://aur.archlinux.org/packages/torrench/)
[![PyPI](https://img.shields.io/pypi/pyversions/torrench.svg)]()
[![Dependency Status](https://gemnasium.com/badges/github.com/kryptxy/torrench.svg)](https://gemnasium.com/github.com/kryptxy/torrench)

Torrench is a command-line program to search and download torrents from torrent-hosting sites. It's compatible under **Linux and Windows** operating systems. 
Torrents can be downloaded from following websites:
1. linuxtracker.org - Download linux distros ISO torrents.
2. The Pirate Bay (TPB)**\*** (Due to illegality of TPB, some configuration is to be done by user. Please Read below).
3. More to come...

![both](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/mix.gif)
_(Click to expand) (Sample shows why TPB is disabled by default.)_

#### \* Using The Pirate Bay (TPB)
By default, searching thepiratebay (TPB) from torrench is disabled. The user should configure and enable it to use. I have provided configuration steps, but before moving to configuration, please note the following:

* Using TPB in many countries is illegal. Using TPB can get you into un-intended troubles (e.g notices/block from ISP). Read [Legal issues](https://en.wikipedia.org/wiki/The_Pirate_Bay#Legal_issues)
* Neither I, nor the tool shall be held responsible for any action taken against you for using TPB from torrench.
* Illegal searches [example](https://github.com/kryptxy/torrench#illegal-searches-should-not-be-practiced)
* This should be enough. Please see [Configuration steps](https://github.com/kryptxy/torrench#thepiratebay-configuration) to enable TPB.

_Torrench initially began as a python learning project for me. I am sure there are ways to implement code I wrote in a much better/efficient way. Do [let me know](https://github.com/kryptxy/torrench#contact) or [Open issue](https://github.com/kryptxy/torrench/issues/new) if you come across any. Alternatively, you can also send a pull request. 
I believe this project can go a long way. I'll need your help expanding it, and keeping it active. Suggestions/Feedbacks are highly appreciated. (I'll soon upload the contributions how-to)_

---

## Installation/Building from Source
### Linux

* Requires [Python3](https://www.python.org/downloads/)
* Arch Users - Can install from [AUR](https://aur.archlinux.org/packages/torrench/)
* Other distro users [Ubuntu,Fedora,Suse,etc...] can use pip (python3-pip)
```
sudo python3 -m pip install torrench
```
* Alternatively, build from source (python-setuptools)
```bash
$ sudo python3 setup.py install
```
	
### Windows
Windows does not require any additional packages. Everything required to run this software is provided in executable (Does not even require python pre-installed).

* Download [torrench executable](https://github.com/kryptxy/torrench/releases/download/v1.0.2/torrench-1.0.2.exe)
* That's it. Run using cmd/powershell [```> torrench.exe <search>```]

	* NOTE: 
		* In windows, the default location for storing html files is ```C:\Users\<user>\.torrench\temp```

### ThePirateBay Configuration:
1. Download [config.ini](https://ln.sy2nc.com/dl/26cd652e0/nqzvd8b3-9gqs3pdu-32btqm2c-9r6mbymm) file (Hosted on sync)
	* **Windows -** Copy the config file in ```C:\Users\<user>\.config\tpb\``` (create any missing directories)
	* **Linux -** Copy the config file to ```$HOME/.config/tpb/``` (Create any missing directories)
2. Enable it
	* Open config.ini file
	* Set ```enable=1```
	* Save and exit
3. That's it. Use with ``` (-t) flag```

---

## Usage
```bash
$ torrench SEARCH_STRING  ## Search linuxtracker
$ torrench -t SEARCH_STRING ## Search thepiratebay
$ torrench [Options] <SEARCH_STRING>
```

## Options
```bash
  -h, --help            show this help message and exit
  
  -t, --thepiratebay    Search thepiratebay
  
  -p LIMIT, --page-limit LIMIT
                        Number of pages to fetch results from (1 page = 30 results). [default: 1] [TPB]
						
  -c, --clear-html      Clear all [TPB] torrent description HTML files and exit.
						
  -v, --version         Display version and exit.
 ```

---

## Features
* Supports all \*nix distros
* Displays results in organized, tabular form.
* [linuxtracker] Supports filtering search using categories
* **[TPB_Specific]** 
	* Surf torrents Ad-free
	* Get complete torrent details (Description, comments, torrent download). Torrent details are available in dynamically-generated HTML pages.
	* Display colored results on basis of uploader's status (Very useful when choosing torrent). (If you are familiar with thepiratebay, you must be knowing that it divides uploaders into 3 categories)
		* VIP Uploader [_green-skull_]
		* Trusted Uploader [_magenta-skull_]
		* General Uploader	
	* Fetch Torrents on basis of pages [1 page yields 30 results (max)].
	* Fetch Comments on basis of pages [Useful when torrent has large number of comments, and not all comments are intended to be fetched].

### Note
* A torrent might take long to fetch results. I have generally faced this issue when running torrench for the first time. When this happens:
	* Abort the ongoing search [Ctrl+C]
	* Search again. The second time generally works fine.

---

## Examples

```bash
$ torrench "ubuntu desktop 16.04"	## Search for Ubuntu Desktop 16.04 distro ISO
$ torrench "fedora workstation"	## Search for Fedora Workstation distro ISO
```
![ubuntu](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/ubuntu.png)
![fedora](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/linux.gif)
---
### Searches considered illegal

```bash
$ torrench -t "windows 7"	## Search win7 TPB
$ torrench -t "game of thrones s07e02" -p 2	## Search and fetch 2 pages TPB for GOT s07e02
```
![illegal](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/windows.png)

![illegal](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/html.png)
_(Dynamically-generated Torrent description HTML page)_ 

![illegal](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/got.gif)
_(Click to expand)_

---

## Disclaimer
This tool only fetches torrent and details from already existing torrent website(s). I do not take any responsibility for availability of any kind of torrent data, or/and hosting of any torrent website(s). Also, I am  not responsible for closing of any of the torrent website(s). As long as the website(s) (proxies) are available, data will be fetched.

## Bug Report and/or Feedback
Found a bug? Please report and help improving this tool. You can [Open Issue](https://github.com/kryptxy/torrench/issues/new) or contact me directly.
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
