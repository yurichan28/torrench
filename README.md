# Torrench - Command-line torrent search tool
![Build Status](https://travis-ci.org/kryptxy/torrench.svg?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/38685c00c3604b608d908b5ae7a6da51)](https://www.codacy.com/app/kryptxy/torrench?utm_source=github.com&utm_medium=referral&utm_content=kryptxy/torrench&utm_campaign=badger)
[![GitHub release](https://img.shields.io/github/release/kryptxy/torrench.svg)]()
[![PyPI](https://img.shields.io/pypi/v/torrench.svg)](https://pypi.python.org/pypi/torrench/)
[![AUR](https://img.shields.io/aur/version/torrench.svg)](https://aur.archlinux.org/packages/torrench/)
[![PyPI](https://img.shields.io/pypi/pyversions/torrench.svg)]()
[![Dependency Status](https://gemnasium.com/badges/github.com/kryptxy/torrench.svg)](https://gemnasium.com/github.com/kryptxy/torrench)
[![Say Thanks](https://img.shields.io/badge/say-thanks-ff69b4.svg)](https://saythanks.io/to/kryptxy)

---
* [About](https://github.com/kryptxy/torrench#about)
* [Optional Sites (TPB/KAT/1337x..) Usage](https://github.com/kryptxy/torrench#-sites-hosting-illegal-content-must-read)
* [Installation/Building from source](https://github.com/kryptxy/torrench#installationbuilding-from-source)
* [Usage and Options](https://github.com/kryptxy/torrench#usage)
* [Features](https://github.com/kryptxy/torrench#features)
* [Samples](https://github.com/kryptxy/torrench#samples)
* [Disclaimer](https://github.com/kryptxy/torrench#disclaimer)
* [Known Issues](https://github.com/kryptxy/torrench#known-issues)
* [Contributing (Bugs/Suggestions/Feedback)](https://github.com/kryptxy/torrench#contributing-bug-reportssuggestionsfeedbacks)
* [Contact](https://github.com/kryptxy/torrench#contact)
* [Licence](https://github.com/kryptxy/torrench#licence)

![linuxtackerv](images/screenshots/linuxtracker.gif)

_(Click to expand) ([More samples](https://github.com/kryptxy/torrench#samples))_

---

## About
Torrench is a command-line program to search and download torrents from torrent-hosting sites. It's compatible under **Windows, Linux and MacOS**.
Torrench supports following websites:

**Supported Sites**

* Linuxtracker (default)
* Distrowatch
* The Pirate Bay (TPB) **[D]**
* KickassTorrents **[D]**
* RarBG **[D]**
* 1337x **[D]**
* LimeTorrents **[D]**
* SkyTorrents **[D]**
* Nyaa **[D]**
* Idope **[D]**
* LibGen (Ebooks) (search only using book's ISBN) **[D]**
* XBit **[D]**

Tested on following platforms:
* **Windows:** Win7 (32bit, 64bit), Win8, Win8.1, Win10.
* **Linux:** Debian/Ubuntu, Fedora, Arch

**[Reported by users]**
* **macOS:** Yosemite, Sierra, High Sierra (10.13). [I do not own a Mac hardware, so unable to test it myself. If you find it working on your system (it should), update me?]

**IMPORTANT -** Please keep a close eye on [CHANGELOGS](https://github.com/kryptxy/torrench/blob/master/CHANGELOG.md). All updates info, addition setup info (whenever required), and everyting else related will be updated there.

---

#### \* **[D]** Sites hosting illegal content (Disabled) (MUST READ)
By default, searching thepiratebay(TPB)/kickasstorrents(KAT)/SkyTorrents/Nyaa/XBit... from torrench is disabled. The user should configure and enable it to use. I have provided configuration steps, but before moving to configuration, please note the following:

* Using these sites is completely optional. They would never interfere/cause any problems when searching linuxtracker/distowatch.
* Using these sites in many countries is illegal. Using them can get you into un-intended troubles (e.g notices/block from ISP). Read [Legal issues](https://en.wikipedia.org/wiki/The_Pirate_Bay#Legal_issues)
* Neither I, nor the tool shall be held responsible for any action taken against you for using the above-mentioned sites from torrench.
* Illegal searches [examples](https://github.com/kryptxy/torrench#searches-considered-illegal)
* [Configuration instructions](https://github.com/kryptxy/torrench#configuration-instructions) if you decide to use them.

_Torrench initially began as a python learning project for me. I am sure there are ways to implement code I wrote in a much better/efficient way. Do [let me know](https://github.com/kryptxy/torrench#contact). Alternatively, you can also send a pull request. See [Contributing](https://github.com/kryptxy/torrench/blob/master/CONTRIBUTING.md)._

---

## Installation/Building from Source
### Linux

* Requires [Python3](https://www.python.org/downloads/) (3.4+)
* Arch Users - Can install from [AUR](https://aur.archlinux.org/packages/torrench/)
* Other distro users [Ubuntu,Fedora,Suse,etc...] can use **pip3** (install/upgrade)
```
$ sudo pip3 install --upgrade torrench
```
* Alternatively, build from source (python-setuptools)
```bash
$ sudo python3 setup.py install
```

### Windows
Windows does not require any additional packages. Everything required to run this software is provided in executable (Does not even require python pre-installed).

* Download latest [torrench executable](https://github.com/kryptxy/torrench/releases/download/v1.0.61/torrench-1.0.61.exe)
* That's it. Run using cmd/powershell [```> torrench.exe <search>```]

	* NOTE:
		* In windows, the default location for storing [TPB] html files is ```C:\Users\<user>\.torrench\temp```
        * ~~For now, `linuxtacker`, `distrowatch` and `libgen` does not allow adding torrent to client from torrench. A `.torrent` file is downloaded to hard-drive. I was unable to find a way to load `.torrent` to client from torrench. I'll try to figure this out when I'll get time. Till then, torrent should be loaded manually after it is downloaded. Also, if someone has a work-around for the same, let me know?~~ 
        **FIXED in v1.0.61**

### Osx

Please note OSX requires to install package `pyopenssl`:
```
$ pip3 install pyopenssl
```

### Configuration instructions:
1. Download the [**config.ini**](https://pastebin.com/reymRHSL) file.
	* **Windows -** Copy the config file in ```C:\Users\<user>\.config\torrench\``` (create any missing directories)
	* **Linux -** Default location is ```$XDG_CONFIG_HOME/torrench/```. If ```$XDG_CONFIG_HOME``` is not defined, it fallbacks to ```$HOME/.config/torrench/``` (Create any missing directories).
	* **MacOS -** See minimal setup guide below.
2. Enable it
	* Open config.ini file
	* Set ```enable=1```
	* Save and exit
3. That's it.

* Once setup, config file can be updated using [`$ torrench -U`]. Setting this up manually for the first time is mandatory though.

_Config file [minimal setup guide](https://gist.github.com/kryptxy/788a052ab8ae9cb5dacdd72d88d3f0ea) (Windows/Linux/MacOS)_

---

## Usage
```bash
$ torrench SEARCH_STRING  ## Search linuxtracker
$ torrench -d SEARCH_STRING ## Search distrowatch
$ torrench [Options] <SEARCH_STRING>
```

## Options
```bash
optional arguments:
    -h, --help            show this help message and exit
    -v, --version         Display version and exit.
    -C, --cross_site      Enable cross-site search
    -U, --update-config   Update config.ini file.
    --interactive         Enable interactive mode for searches
    --no-merge            (Cross-site) Do not merge results in one table
    --sorted              (Cross-site) sort results on basis of Seeds.

Main Sites:
    search                Search LinuxTracker (default)
    -d, --distrowatch     Search Distrowatch

Optional Sites:
  Requires configuration (disabled by default)

    -t, --thepiratebay    Search thepiratebay (TPB)
    -k, --kickasstorrent  Search KickassTorrent (KAT)
    -s, --skytorrents     Search SkyTorrents
    -x, --x1337           Search 1337x
    -r, --rarbg           Search RarBg
    -n, --nyaa            Search Nyaa
    -l, --limetorrents    Search LimeTorrents
    -i, --idope           Search Idope
    -b, --xbit            Search XBit.pw
    -g, --libgen          Search LibGen (Ebooks)

Additional options:
    -c, --clear-html      Clear all [TPB] torrent description HTML files and exit.
    -p LIMIT, --page-limit LIMIT
                            Number of pages to fetch results from. [default: 1]
    --copy                Copy magnetic link to clipboard
    --top                 Get TOP torrents [TPB/SkyTorrents]
 ```

## Features
* Displays results in organized, tabular form.
* Load torrent to client from torrench.
* [Cross-site search](https://github.com/kryptxy/torrench/blob/master/README.md#cross-site-search): Search multiple sites with a single command.
* Interactive mode for searching across modules (```--interactive```)
* Copy magnetic link to clipboard (```$ torrench -x 'ubuntu' --copy```) [Linux systems require ```xclip``` package additionally]
* Get TOP torrents [TPB/SkyTorrents] (```--top```)
* *Much more...*

---

### Loading torrent to client

#### [LINUX/MacOS]
* Requires **[torrench.ini](https://github.com/kryptxy/torrench/blob/master/torrench.ini)** config file.
    * Default directory: **$XDG_CONFIG_HOME/torrench**
    * Fallback: **$HOME/.config/torrench/**
* Set the default torrent client name in config file.
    * ```CLIENT = <name>```
* Clients tested:
    * Transmission (```transmission-remote```, ```transmission-gtk```, ```transmission-qt```)
    * Deluge (```deluge```, ```deluge-console```)
    * qBittorrent
* If someone tried ```rtorrent```, please report.

* **Setting up ```transmission-remote```**
    * Requires running **transmission-daemon** service
    * Torrent is added to transmission client using **transmission-remote** utitlity.
    * **(IMP)** For AUTHENTICATION - ```$TR_AUTH``` environment variable is used.
        * [TR_AUTH="username:password"]
    * **(IMP)** For PORT/SERVER - Set the PORT and SERVER variable in **[torrench.ini](https://github.com/kryptxy/torrench/blob/master/torrench.ini)** file accordingly.
        * If ```$TR_AUTH``` or PORT/SERVER are not set, the following (default) values are used:
        * DEFAULTS
            * Username - [None]
            * password - [None]
            * SERVER - localhost (127.0.0.1)
            * PORT - 9091

#### [Windows]
* ~~In windows, by default the magnetic link is opened in browser. If a torrent client is installed, the browser should automatically open the (default) client and load torrent to the client.~~
* Instead of opening torrent in browser, torrent is loaded directly to **default torrent client**. Works for both magnetic links and .torrent files.

---

### Cross-Site search
It is possible to search multiple sites with a single command (Cross-site search)

#### Sample
`$ torrench -Ctisx 'ubuntu'`

![cross-site](images/screenshots/cross.gif)

**USAGE**
-  Use `-C` argument to search multiple sites. Example: `$ torrench -Ctlxsb 'fedora'`
- By default, the results are merged into a **single table**. To view results separately, use `--no-merge` argument. This would give an option to select site, followed by torrent selection.
- By default the results are merged on the basis of order of fetch.
        Eg: If TPB is fetched first followed by KAT, final table will have all results of TPB followed by KAT.
        To sort results, use `--sort` argument. Results are sorted on basis of **seeds**.
- As of now, **linuxtracker, distrowatch and libgen are not supported.** Rest all can be used for cross-site.

---

### Note
* A torrent might take long to fetch results. I have generally faced this issue when running torrench for the first time. When this happens:
	* Abort the ongoing search [Ctrl+C]
	* Search again. The second time generally works fine.
* KAT Proxy is quite shaky, and might not work at all times. I have been unable to find any reliable KAT proxy. Consider alternatives if they do not work.
* Searching **LibGen** - LibGen allows searching for Ebooks using book's **ISBN-10 number only**. Searching using book title is not supported. (LibGen API does not allow searching using title). A book's ISBN-10 number can be found with a simple google search, or on websites like Amazon.

---

## Samples

```bash
$ torrench "ubuntu desktop 16.04"	## Search Linuxtracker for Ubuntu Desktop 16.04 distro ISO
$ torrench "fedora workstation"	## Search for Fedora Workstation distro ISO
$ torrench -d "opensuse" ## Search distrowatch for opensuse ISO
$ torrench -d "solus" ## Search distrowatch for solus ISO
$ torrench -x "fedora" ## Search XBit for fedora distros ISO
$ torrench -l 'arch linux'  ## Search limetorrents for Arch linux disro ISO
```
#### Linuxtracker
```bash
$ torrench "fedora workstation"
```
![linuxtracker](images/screenshots/linuxtracker.gif)
![linuxtracker](images/screenshots/linuxtracker.png)

#### DistroWatch
```bash
$ torrench -d "ubuntu"
```
![distrowatch](images/screenshots/distrowatch.gif)

#### 1337x
```bash
$ torrench -x "ubuntu"
```
![1337x](images/screenshots/1337x.png)

#### Idope
```bash
$ torrench -i "opensuse"
```
![illegal](images/screenshots/idope.png)

#### LimeTorrents
```bash
$ torrench -l "arch linux"
```
![illegal](images/screenshots/idope.png)


#### XBit
```bash
$ torrench -x "fedora"
```
![xbit](images/screenshots/xbit.png)

---
### Searches considered illegal
#### TPB Examples

```bash
$ torrench -t "game of thrones s07e02" -p 2	## Search and fetch 2 pages TPB for GOT s07e02
$ torrench -t "windows 7"
```
![illegal](images/screenshots/tpb.png)

![illegal](images/screenshots/html.png)
_(Dynamically-generated Torrent description HTML page)_

![illegal](images/screenshots/tpb.gif)
_(Click to expand)_

#### LibGen (Ebooks) (Search using ISBN-10)
```bash
$ torrench -g 1593272901
```
![illegal](images/screenshots/libgen.png)

#### KAT
```bash
$ torrench -k "doctor strange"
$ torrench -k "guardians of the galaxy"
```

#### RarBg
```bash
$ torrench -r "mr robot"
```


#### SkyTorrents
```bash
$ torrench -s "hannibal"
$ torrench -s "narcos"
```


#### Nyaa
```bash
$ torrench -n "naruto"
```

---

## Disclaimer
This tool fetches torrent and details from already existing torrent website(s). I do not take any responsibility for availability of any kind of torrent data, or/and hosting of any torrent website(s). Also, I am  not responsible for closing of any of the torrent website(s). As long as the website(s) (proxies) are available, data will be fetched.

## Known issues
* **Distorted results**: Some websites displaying non-english characters can distort the resulting table. To properly align tables which contain wide characters (typically fullwidth glyphs from Chinese, Japanese or Korean languages), the user should install `wcwidth` library.

`$ sudo pip3 install wcwidth`

## Contributing (Bug reports/suggestions/feedbacks)
Please see [CONTRIBUTING](https://github.com/kryptxy/torrench/blob/master/CONTRIBUTING.md)

## Contact
* E-mail : kryptxy@protonmail.com
* [Twitter (DM)](https://twitter.com/kryptxy)
* [Telegram](http://t.me/kryptxy)

## Thank you
* Contributors for giving your time to this project and improving it.
* Users for your valuable feedback and suggestions.

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
