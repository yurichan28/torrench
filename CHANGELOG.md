### [08/09/2017] v1.0.5
#### MAJOR UPDATE
**New copy of config.ini file is required for TPB/KAT/Skytorrents updated support**
* Added classes. Re-written modules in form of classes.
* **Added logging.** All torrench activities are now logged in a log file. A new log file is created everyday (at midnight). The current log file is named **torrench.log**, while previous log files are named **torrench.log.YYYY-MM-DD**.
Log files are present as follows:
    * **Windows:** ```~\AppData\Local\torrench```
    * **\*nix systems (Linux/MacOS):** Default location is $XDG_DATA_HOME. Fallback to ```$HOME/.local/share/torrench```
* \*nix users (Linux/MacOS): Default location for CONFIG file (config.ini) has been changed to ```$XDG_CONFIG_HOME```. If it is not set, fallbacks to ```$HOME/.config/torrench```
* Added **SkyTorrents** support (-s).
* Added **Top torrents** option for TPB and SkyTorrents (--top).
* Added two more KAT proxies.
* Improved TPB/KAT proxy cycling. If one proxy is not available, next proxy is selected.
* Updated config.ini file.
* Project structure improvements.
* Many other minor improvements.

### [24/08/2017] v1.0.42
* Fix KAT proxy site error.
Note: UPDATE the config.ini file for KAT to work!
New config.ini file links have been updated in description.

### [22/08/2017] v1.0.41
* Re-structured entire project
* Added DistroWatch support
* Fix TPB/KAT not showing some torrents
* Fix sys.exit() codes
* Speed optimisations
* Instead of directly loading magnetic link to client, it is first printed.
* Other minor fixes

### [13/08/2017] v1.0.3
* Added kickasstorrents (KAT) support. Use with (-k) argument.
* Changed config directory to ~/.config/torrench from ~/.config/tpb [tpb/ -> torrench/]
* Changed file structure for better code management
* Other little bug fixes.


### [09/08/2017] v1.0.2
* Replaced termcolor dependency with colorama (cross-platform)
* Fixed trusted uploader's output color (magenta) for windows. Color displays perfect now [TPB]

### [06/08/2017] Torrench v1.0.1.20170807
* setup.py - replaced bs4 to beautifulsoup4

### [06/08/2017] Torrench v1.0.0.20170806
* Added setup.py script [uploaded torrench on pypi]
* Re-structured entire software for better management
* [TPB] Changed config file directory to ~/.config/tpb/ (Linux) and ~\.config\tpb\ (Windows)
* Minor code-fixes

### [01/08/2017]
* Added linuxtracker.org to search linux distro torrent [default]
* Indexing torrents from TPB requires special configuration. It won't work without it.
   See documentation for more. (Read carefully!)
