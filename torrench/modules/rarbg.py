"""RarBg Module."""

import logging
import sys
import time

import requests
from torrench.utilities.Config import Config


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
        Select torrent

        Torrent is selected using index value.
        All of its functionality is defined in Common.py file.
        """
        self.logger.debug("Output displayed. Selecting torrent")
        while True:
            index = self.select_index(len(self.mapper))
            if index == 0:
                continue
            self.select_option(self.mapper, index, 'rarbg')


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
