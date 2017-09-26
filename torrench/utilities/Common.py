"""Common Module - Used by all torrent-fetching modules."""
import time
import os
import sys
import platform
import requests
from bs4 import BeautifulSoup
import colorama
from tabulate import tabulate
import logging
import subprocess
import webbrowser
import pyperclip
from configparser import SafeConfigParser


class Common:
    """
    Common class.

    This class consists common methods that are used by all the modules.

    methods:
    -- http_request_time():: Returns 'self.soup' as well as time taken to fetch URL.
    -- http_request():: Same as above. Only does not return time taken
    Also, time taken to fetch URL is returned.
    -- download():: To download .torrent file in $HOME/Downloads/torrench dir.
    -- colorify():: To return colored self.output
    -- show_output():: To display search results self.output (self.output table)
    -- copy_magnet():: To copy magnetic link to clipboard.
    --load_torrent():: To load torrent magnetic link to client.
    """

    def __init__(self):
        """Initialisations."""
        self.config = SafeConfigParser()
        self.config_dir = os.getenv('XDG_CONFIG_HOME', os.path.expanduser(os.path.join('~', '.config')))
        self.full_config_dir = os.path.join(self.config_dir, 'torrench')
        self.config_file_name = "torrench.ini"
        self.torrench_config_file = os.path.join(self.full_config_dir, self.config_file_name)
        self.raw = None
        self.soup = None
        self.output = None
        self.start_time = 0
        self.page_fetch_time = 0
        self.colors = {}
        self.logger = logging.getLogger('log1')
        self.OS_WIN = False
        if platform.system() == "Windows":
            self.OS_WIN = True

    def http_request_time(self, url):
        """
        http_request_time method.

        Used to fetch 'url' page and prepare soup.
        It also gives the time taken to fetch url.
        """
        try:
            try:
                self.start_time = time.time()
                self.raw = requests.get(url, timeout=15)
                self.page_fetch_time = time.time() - self.start_time
                self.logger.debug("returned status code: %d for url %s" % (self.raw.status_code, url))
            except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
                self.logger.error(e)
                self.logger.exception("Stacktrace...")
                return -1
            except KeyboardInterrupt as e:
                self.logger.exception(e)
                print("\nAborted!\n")
            self.raw = self.raw.content
            self.soup = BeautifulSoup(self.raw, 'lxml')
            return self.soup, self.page_fetch_time
        except KeyboardInterrupt as e:
            print("Aborted!")
            self.logger.exception(e)
            sys.exit(2)

    def http_request(self, url):
        """
        http_request method.

        This method does not calculate time.
        Only fetches URL and prepares self.soup
        """
        try:
            try:
                self.raw = requests.get(url, timeout=15)
                self.logger.debug("returned status code: %d for url %s" % (self.raw.status_code, url))
            except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
                self.logger.error(e)
                self.logger.exception("Stacktrace...")
                return -1
            self.raw = self.raw.content
            self.soup = BeautifulSoup(self.raw, 'lxml')
            return self.soup
        except KeyboardInterrupt as e:
            print("Aborted!")
            self.logger.exception(e)
            sys.exit(2)

    def download(self, dload_url, torrent_name):
        """
        Torrent download method.

        Used to download .torrent file.
        Torrent is downloaded in ~/Downloads/torrench/
        """
        try:
            self.logger.debug("Download begins...")
            home = os.path.expanduser(os.path.join('~', 'Downloads'))
            downloads_dir = os.path.join(home, 'torrench')
            self.logger.debug("Default download directory: %s", (downloads_dir))
            if not os.path.exists(downloads_dir):
                self.logger.debug("download directory does not exist.")
                os.makedirs(downloads_dir)
                self.logger.debug("created directory: %s", (downloads_dir))

            with open(os.path.join(downloads_dir, torrent_name), "wb") as file:
                print("Downloading torrent...")
                response = requests.get(dload_url)
                file.write(response.content)
                self.logger.debug("Download complete!")
                print("Download complete!")
                print("\nSaved in %s\n" %(downloads_dir))
                self.logger.debug("Saved in %s", (downloads_dir))
        except KeyboardInterrupt as e:
            self.logger.exception(e)
            print("\nAborted!\n")

    def colorify(self, color, text):
        """To return colored text."""
        colorama.init()
        self.colors = {
            "yellow": colorama.Fore.YELLOW + colorama.Style.BRIGHT,
            "green": colorama.Fore.GREEN + colorama.Style.BRIGHT,
            "magenta": colorama.Fore.MAGENTA + colorama.Style.BRIGHT,
            "red": colorama.Fore.RED + colorama.Style.BRIGHT,
            "reset": colorama.Style.RESET_ALL
        }
        text = self.colors[color] + text + self.colors["reset"]
        return text

    def show_output(self, masterlist, headers):
        """To display tabular output of torrent search."""
        try:
            self.output = tabulate(masterlist, headers=headers, tablefmt="grid")
            print("\n%s" %(self.output))
        except KeyboardInterrupt as e:
            self.logger.exception(e)
            print("\nAborted!\n")

    def copy_magnet(self, link):
        """Copy magnetic link to clipboard."""
        try:
            pyperclip.copy(link)
            print("(Magnetic link copied to clipboard)")
        except pyperclip.exceptions.PyperclipException as e:
            print("(Unable to copy magnetic link to clipboard. Is [xclip] installed?)")
            print("(See logs for details)")
            self.logger.error(e)

    def load_torrent(self, link):
        """Load torrent (magnet) to client."""
        try:
            if not self.OS_WIN:
                """[LINUX / MacOS]"""
                if os.path.isfile(self.torrench_config_file):
                    self.logger.debug("torrench.ini file exists")
                    self.config.read(self.torrench_config_file)
                    client = self.config.get('Torrench-Config', 'client')
                    self.logger.debug("using client: %s" %(client))
                else:
                    print("No config (torrench.ini) file found!")
                    self.logger.debug("torrench.ini file not found!")
                    return
                """
                [client = Transmission (transmission-remote)]
                    > Load torrent to transmission client
                    > Torrent is added to daemon using `transmission-remote`.
                    > Requires running `transmission-daemon`.

                    1. For authentication:
                        $TR_AUTH environment variable is used.
                        [TR_AUTH="username:password"]
                    2. For SERVER and PORT:
                        $TR_SERVER environment variable is used.
                        [TR_SERVER="IP_ADDR:PORT"]

                    DEFAULTS
                    Username - [None]
                    password - [None]
                    IP_ADDR - localhost (127.0.0.1)
                    PORT - 9091
                """
                if client == 'transmission-remote':
                    server = os.getenv('TR_SERVER', "localhost:9091")
                    p = subprocess.Popen([client, server, '-ne', '--add', link], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                    e = p.communicate()  # `e` is a tuple.
                    error = e[1].decode('utf-8')
                    p.wait()
                    if error != '':
                        print(self.colorify("red", "[ERROR] %s" % (error)))
                        self.logger.error(error)
                    else:
                        print(self.colorify("green", "Success (PID: %d)") %(p.pid))
                        self.logger.debug("Torrent added successfully!")
                else:
                    """
                    Any other torrent client.
                    > Tested: transmission-gtk, transmission-qt
                    > Not tested, but should work: rtorrent, qbittorrent (please update me)
                    """
                    p = subprocess.Popen([client, link], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print(self.colorify("green", "Success (PID: %d)") %(p.pid))
                    self.logger.debug("torrent added!")
            else:
                """
                [WINDOWS]

                The magnetic link is added to web-browser.
                Web browser should be able to load torrent to client automatically
                """
                webbrowser.open_new_tab(link)
        except Exception as e:
            self.logger.exception(e)
            print(self.colorify("red",  "[ERROR]: %s") % (e))
