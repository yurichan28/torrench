### [23/09/2017] v1.0.54

1. **Add torrent to client directly from torrench**
    * **[Linux/MacOS]**
        * Requires **[torrench.ini](https://github.com/kryptxy/torrench/blob/master/torrench.ini)** config file.
            * Default directory: **$XDG_CONFIG_HOME/torrench**
            * Fallback: **$HOME/.config/torrench/**
        * Set the default torrent client name in config file.
            * ```CLIENT = <name>```
        * Clients tested by me:
            * Transmission (```transmission-remote```, ```transmission-gtk```, ```transmission-qt```)
        * I haven't tested any other, but they should work too (```rtorrent```, ```qbittorrent```...) (Test and report please)

        * **ABOUT ```transmission-remote```**
            * Requires running **transmission-daemon** service
            * Torrent is added to transmission client using **transmission-remote** utitlity.
            * For AUTHENTICATION - **$TR_AUTH** environment variable is used.
                * [TR_AUTH="username:password"]
            * For PORT/SERVER - Set the PORT and SERVER variable in **[torrench.ini](https://github.com/kryptxy/torrench/blob/master/torrench.ini)** file accordingly.
                * If $TR_AUTH or PORT/SERVER are not set, the following (default) values are used:
                * DEFAULTS
                    * Username - [None]
                    * password - [None]
                    * SERVER - localhost (127.0.0.1)
                    * PORT - 9091
        * **[Windows]**
            * In windows, by default the magnetic link is opened in browser. If a torrent client is installed, the browser should automatically open the (default) client and load torrent to the client.

2. Added ```--copy``` argument. Use this argument to **copy magnetic link** to clipboard. Magnetic link is **not copied** to clipboard without ```--copy```.
    * Magnetic link is copied on **printing the Magnetic link** (that is choosing [p] when given option to _load torrent_ or _print magnet_)
    * ```torrench -t "ubuntu" --copy```

3. Display option to _Print magnetic link_ or _Load magnet to client_ (KAT,SkyTorrents,Nyaa) instead of directly displaying the magnetic link.

---

### [23/09/2017] v1.0.53
* **Added Nyaa[.]si support (-n flag)**
* **Added XBit[.]pw support (-x flag)**
    * **Windows:** Since windows Command-prompt/Powershell is unable to print unicode characters (Well it can, but it may break other things and is not recommended), any such character is converted to **'?'** character.
* **Automatically copy magnetic link to clipboard [All platforms]**
    * **Linux:** Requires **xclip** package to be installed.
    * **MacOS:** (Not tested but should work without issues) - Test and report?
    * **Windows:** Nothing else required. Works as it is.
* **Add torrent directly to client [Linux/MacOS/Windows] (Updated - 27/09/17)**

    **PLEASE NOTE: THESE CHANGES WERE MADE AFTER v1.0.53 WAS RELEASED. PLEASE [BUILD FROM SOURCE](https://github.com/kryptxy/torrench#installationbuilding-from-source) TO GET THESE RIGHT NOW, OR YOU MAY WAIT FOR NEXT RELEASE**
    * **[Linux/MacOS]**
        * Requires **[torrench.ini](https://github.com/kryptxy/torrench/blob/master/torrench.ini)** config file.
            * Default directory: **$XDG_CONFIG_HOME/torrench**
            * Fallback: **$HOME/.config/torrench/**
        * Set the default torrent client name in config file.
            * ```CLIENT = <name>```
        * Clients tested by me:
            * Transmission (```transmission-remote```, ```transmission-gtk```, ```transmission-qt```)
        * I haven't tested any other, but they should work too (```rtorrent```, ```qbittorrent```...) (Test and report)

        * **ABOUT ```transmission-remote```**
            * Requires running **transmission-daemon** service
            * Torrent is added to transmission client using **transmission-remote** utitlity.
            * For AUTHENTICATION - **$TR_AUTH** environment variable is used.
                * [TR_AUTH="username:password"]
            * For PORT/SERVER - Set the PORT and SERVER variable in **[torrench.ini](https://github.com/kryptxy/torrench/blob/master/torrench.ini)** file accordingly.
                * If $TR_AUTH or PORT/SERVER are not set, the following (default) values are used:
                * DEFAULTS
                    * Username - [None]
                    * password - [None]
                    * SERVER - localhost (127.0.0.1)
                    * PORT - 9091
        * ~**Note:** As of now, this is the default (and the only) client supported by torrench.~

    * **Windows client support:** In windows, by default the magnetic link is opened in browser. If a torrent client is installed, the browser should automatically open the (default) client and load torrent to the client.
* **Fix wrong index display bug [TPB/KAT/linuxtracker]**
* **Few other minor fixes/updates.**
* **Updated/New copy of [config.ini](https://github.com/kryptxy/torrench#configuration-instructions) file is required for XBit/Nyaa support**

---

### [08/09/2017] v1.0.51 [1.0.5 is renamed to 1.0.51 for pip error fix]
#### MAJOR UPDATE
**New copy of config.ini file is required for TPB/KAT/Skytorrents updated support**
* Added classes. Re-written modules in form of classes.
* **Added logging.** All torrench activities are now logged in a log file. A new log file is created everyday (at midnight). The current log file is named **torrench.log**, while previous log files are named **torrench.log.YYYY-MM-DD**.
Log files are present as follows:
    * **Windows:** ```~\AppData\Local\torrench```
    * **\*nix systems (Linux/MacOS):** Default location is ```$XDG_DATA_HOME```. Fallback to ```$HOME/.local/share/torrench```
* \*nix users (Linux/MacOS): Default location for **CONFIG file (config.ini)** has been changed to ```$XDG_CONFIG_HOME```. If it is not set, fallbacks to ```$HOME/.config/torrench```
* Added **SkyTorrents** support (-s).
* Added **Top torrents** option for TPB and SkyTorrents (--top).
* Added two more KAT proxies.
* Improved TPB/KAT proxy cycling. If one proxy is not available, next proxy is selected.
* Updated config.ini file.
* Project structure improvements.
* Many other minor improvements.

---

### [24/08/2017] v1.0.42
* Fix KAT proxy site error.
Note: UPDATE the config.ini file for KAT to work!
New config.ini file links have been updated in description.

---

### [22/08/2017] v1.0.41
* Re-structured entire project
* Added DistroWatch support
* Fix TPB/KAT not showing some torrents
* Fix sys.exit() codes
* Speed optimisations
* Instead of directly loading magnetic link to client, it is first printed.
* Other minor fixes

---

### [13/08/2017] v1.0.3
* Added kickasstorrents (KAT) support. Use with (-k) argument.
* Changed config directory to ~/.config/torrench from ~/.config/tpb [tpb/ -> torrench/]
* Changed file structure for better code management
* Other little bug fixes.

---

### [09/08/2017] v1.0.2
* Replaced termcolor dependency with colorama (cross-platform)
* Fixed trusted uploader's output color (magenta) for windows. Color displays perfect now [TPB]

---

### [06/08/2017] Torrench v1.0.1.20170807
* setup.py - replaced bs4 to beautifulsoup4

---

### [06/08/2017] Torrench v1.0.0.20170806
* Added setup.py script [uploaded torrench on pypi]
* Re-structured entire software for better management
* [TPB] Changed config file directory to ~/.config/tpb/ (Linux) and ~\.config\tpb\ (Windows)
* Minor code-fixes

---

### [01/08/2017]
* Added linuxtracker.org to search linux distro torrent [default]
* Indexing torrents from TPB requires special configuration. It won't work without it.
   See documentation for more. (Read carefully!)
