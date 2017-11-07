"""RarBg Module."""

import requests
from torrench.utilities.Config import Config
import logging
import sys
import time

class RarBg(Config):
    """
    RarBg Class.

    Torrench uses RarBG API instead of scrapping the web.
    For this to work, a token is generated.
    Tokens automaticly expire in 15 minutes.
    The api has a 1req/2s limit.
    """
    def __init__(self, title):
        """Initialisations."""
        Config.__init__(self)
        self.proxies = self.get_proxies('rarbg')
        self.proxy = self.proxies[0]
        self.logger = logging.getLogger('log1')
        self.title = title
        self.index = 0
        self.token = None
        self.mapper = []
        self.total_fetch_time = 0
        self.output_headers = [
                'CATEG', 'NAME', 'INDEX', 'SIZE', 'S/L', 'DATE'
                ]

    def get_token(self):
        """To generate token."""
        self.logger.debug("Getting token")
        get_token = "get_token=get_token"
        raw = requests.get(self.proxy+get_token).json()
        self.token = raw['token']
        self.logger.debug("Token generated - {}".format(self.token))

    def search_torrent(self):
        """To search torrent for given input.

        The API gives out results in JSON format.
        """
        try:
            masterlist = []
            params = "mode=search&app_id=torrench&sort=seeders&limit=100&format=json_extended&search_string={}&token={}".format(self.title, self.token)
            start_time = time.time()
            self.logger.debug("Fetching results")
            raw = requests.get(self.proxy+params).json()
            if 'error' in raw:
                print(raw['error'])
                self.logger.debug(raw['error'])
                self.logger.debug("Exiting!")
                sys.exit(2)
            self.total_fetch_time = time.time() - start_time
            results = raw['torrent_results']
            for result in results:
                name = result['title']
                category = result['category']
                magnet = result['download']
                seeds = str(result['seeders'])
                leeches = str(result['leechers'])
                seeds = self.colorify("green", seeds)
                leeches = self.colorify("red", leeches)
                size = result['size']
                date = result['pubdate']
                date = " ".join(date.split(" ")[0:2])
                link = result['info_page']
                size = size/1024/1024/1024
                size_end = "GB"
                if size < 1:
                    size *= 1024
                    size_end = "MB"
                size = "{0:.2f} {1}".format(size, size_end)
                self.mapper.insert(self.index, (name, magnet, link))
                self.index += 1
                self.mylist = [category, name, "--" +
                    str(self.index) + "--", size, seeds + '/' + leeches, date]
                masterlist.append(self.mylist)
            self.logger.debug("Results fetched successfully!")
            self.show_output(masterlist, self.output_headers)
        except Exception as e:
            self.logger.exception(e)
            print("Error message: %s" % (e))
            print("Something went wrong! See logs for details. Exiting!")
            sys.exit(2)

    def after_output_text(self):
        """
        After output is displayed, Following text is displayed on console.

        Text includes instructions, total torrents fetched, total pages,
        and total time taken to fetch results.
        """
        oplist = [self.index, self.total_fetch_time]
        self.after_output('rarbg', oplist)

    def select_torrent(self):
        """
        To select required torrent.

        Torrent is selected through index value.
        Two options are present:
        1. To print magnetic link and upstream link to console.
        2. Torrent can be added directly to client.
        """
        self.logger.debug("Selecting torrent...")
        temp = 9999
        while(temp != 0):
            try:
                temp = int(input("\n(0=exit)\nindex > "))
                self.logger.debug("selected index %d" % (temp))
                if temp == 0:
                    print("\nBye!")
                    self.logger.debug("Torrench quit!")
                    break
                elif temp < 0:
                    print("\nBad Input!")
                    continue
                else:
                    selected_torrent, req_magnetic_link, torrent_link = self.mapper[temp-1]
                    print("Selected index [%d] - %s\n" % (temp, self.colorify("yellow", selected_torrent)))
                    self.logger.debug("selected torrent: %s ; index: %d" % (selected_torrent, temp))
                    temp2 = input("1. Print links [p]\n2. Load magnetic link to client [l]\n\nOption [p/l]: ")
                    temp2 = temp2.lower()
                    self.logger.debug("selected option: [%c]" % (temp2))
                    if temp2 == 'p':
                        self.logger.debug("printing magnetic link and upstream link")
                        print("\nMagnetic link - %s" % (self.colorify("red",  req_magnetic_link)))
                        self.copy_magnet(req_magnetic_link)
                        print("\n\nUpstream link - %s\n" % (self.colorify("yellow", torrent_link)))
                    elif temp2 == 'l':
                        try:
                            self.logger.debug("Loading magnetic link to client")
                            self.load_torrent(req_magnetic_link)
                        except Exception as e:
                            self.logger.exception(e)
                            continue
                    else:
                        self.logger.debug("Inappropriate input! Should be [p/l/g] only!")
                        print("Bad input!")
                        continue
            except (ValueError, IndexError, TypeError) as e:
                print("\nBad Input!")
                self.logger.exception(e)
                continue


def main(title):
    """Execution begins here."""
    print("\n[RarBg]\n")
    rbg = RarBg(title)
    rbg.get_token()
    rbg.search_torrent()
    rbg.after_output_text()
    rbg.select_torrent()


if __name__ == "__main__":
    print("It's a module!")
