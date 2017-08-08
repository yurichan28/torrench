# Torrench - Command-line torrent search tool
![Build Status](https://travis-ci.org/kryptxy/torrench.svg?branch=master)

![both-search](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/mix.gif)
_(click to expand)_

**Note:** Using thepiratebay (TPB) requires some configuration to be done. Please do not skip the TPB readme section.

---

## Index
* [ABOUT](https://github.com/kryptxy/torrench#about)
* [INSTALLATION/BUILDING](https://github.com/kryptxy/torrench#installationbuilding-from-source)
* [OPTIONS](https://github.com/kryptxy/torrench#options)
* [FEATURES](https://github.com/kryptxy/torrench#features)
* [EXAMPLES](https://github.com/kryptxy/torrench#examples)
* [DISCLAIMER](https://github.com/kryptxy/torrench#disclaimer)
* [BUGS/FEEDBACK](https://github.com/kryptxy/torrench#bug-report-andor-feedback)
* [CONTACT](https://github.com/kryptxy/torrench#contact)
* [LICENCE](https://github.com/kryptxy/torrench#licence)

## ABOUT
Torrench is a command-line program to search and download torrents from various torrent-hosting websites. It's compatible under **Linux and Windows** operating systems. 
Torrents can be downloaded from following websites:
1. linuxtracker.org - Download linux distros ISO torrents **[default]**	
2. The Pirate Bay (TPB)**\***: (Read below)
3. More to come...

#### \* The Pirate Bay(TPB)
By default, searching thepiratebay (TPB) from torrench is disabled. The user should configure and enable it to use. I have provided configuration steps, but before moving to configuration, please note the following:

* Using TPB in many countries is illegal. Using TPB can get you into un-intended troubles (e.g notices/block from ISP). Read [Legal issues](https://en.wikipedia.org/wiki/The_Pirate_Bay#Legal_issues)
* Neither I, nor the tool shall be held responsible for any action taken against you for using TPB from torrench.
* Illegal searches [example](https://github.com/kryptxy/torrench#illegal-searches-should-not-be-practiced)
* This should be enough. Please see [Configuration steps](https://github.com/kryptxy/torrench#thepiratebay-configuration) to enable TPB.

---

## Installation/Building from Source
### Linux

* Requires [Python3](https://www.python.org/downloads/)
* Arch Users - Can install from [AUR](https://aur.archlinux.org/packages/torrench/)
* Other distro users [Ubuntu,Fedora,Suse,etc...] can use pip (python3-pip)
```
sudo -H python3 -m pip install torrench
```
* Alternatively, build from source (python-setuptools)
```bash
$ sudo python3 setup.py install
```
	
### Windows
Windows does not require any additional packages. Everything required to run this software is provided in executable (Does not even require python pre-installed).

* Download [torrench executable](https://github.com/kryptxy/torrench/releases/download/v1.0.1.20170807/torrench-1.0.1.20170807.exe)
* That's it. Run using cmd/powershell [```> torrench.exe <search>```]

	* NOTE: 
		* Windows powershell is unable to display magenta color. When I tried, the _name_ field was appearing empty. So to distinguish trusted uploaders, I have added a cyan-colored (\**) in front and at the back of TORRENT NAME and UPLOADER NAME. 
		* In windows, the default location for storing html files is ```C:\Users\<user>\.torrench\temp```

### ThePirateBay Configuration:
1. Download [config.ini](https://ln.sync.com/dl/26cd652e0/nqzvd8b3-9gqs3pdu-32btqm2c-9r6mbymm) file (Hosted on sync)
	* **Windows -** Copy the config file in ```C:\Users\<user>\.config\tpb\``` (create any missing directories)
	* **Linux -** Copy the config file to ```$HOME/.config/tpb/``` (Create any missing directories)
2. Enable it
	* Open config.ini file
	* Set ```enable=1```
	* Save and exit
3. That's it. Use with ``` (-t) flag```

---

## Options
```bash
usage: torrench [-h] [-t] [-p LIMIT] [-c] [-v] [search]

Command-line torrent search tool.

positional arguments:
  search                Enter search string

optional arguments:
  -h, --help            show this help message and exit
  -t, --thepiratebay    Search thepiratebay
  -p LIMIT, --page-limit LIMIT
                        Number of pages to fetch results from (1 page = 30
                        results). [default: 1]
  -c, --clear-html      Clear all [TPB] torrent description HTML files and
                        exit.
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
$ torrench -h	## Display help
$ torrench "ubuntu 17.10"	## Search for ubuntu 17.10 distro ISO
$ torrench "fedora 25 workstation"	## Search for F25 distro ISO
```
![fedora](https://raw.githubusercontent.com/kryptxy/torrench/master/images/screenshots/linux.gif)
---
### Illegal searches (Should not be practiced)

```bash
$ torrench -t "windows 10"
$ torrench -t "game of thrones s05" -p 3
```
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
