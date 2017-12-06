"""xbit.pw module."""

import logging
import sys
import time

import requests
from torrench.utilities.Config import Config


class XBit(Config):
    """
    XBit class.

    This class fetches torrents from xbit.pw,
    and diplays results in tabular form.
    Further, torrent's magnetic link
    can be printed to console.
    Torrent can be added to client directly

    This class inherits Config class. Config class inherits
    Common class. The Config class provides proxies list fetched
    from config file. The Common class consists of commonly used
    methods.

    All activities are logged and stored in a log file.
    In case of errors/unexpected output, refer logs.
    """

    def __init__(self, title):
        """Initialisations."""
        Config.__init__(self)
        self.proxies = self.get_proxies('xbit')
        self.proxy = self.proxies[0]
        self.title = title
        self.logger = logging.getLogger('log1')
        self.index = 0
        self.total_fetch_time = 0
        self.mylist = []
        self.mapper = []
        self.mylist_crossite = []
        self.masterlist_crossite = []
        self.data = {}
        self.output_headers = [
                'ID', 'NAME', 'INDEX', 'SIZE', 'DISCOVERED']

    def search_torrent(self):
        """
        Obtain and parse JSON.

        Torrent id, name, magnet, size and date are fetched.
        """
        try:
            search = "api?search=%s&limit=100" % (self.title)
            print("Fetching results...")
            start_time = time.time()
            raw = requests.get(self.proxy+search).json()
            self.total_fetch_time = time.time() - start_time
            print("[in {:.2f} sec]".format(self.total_fetch_time))
            self.data = raw
            masterlist = []
            results = self.data['dht_results']
            if results == [{}]:
                return
            for result in results[:-1]:
                torrent_id = result['ID']
                name = result['NAME']
                magnet = result['MAGNET']
                size = result['SIZE']
                date = result['DISCOVERED']
                self.index += 1
                self.mapper.insert(self.index, (name, magnet, 'None'))
                self.mylist = [torrent_id, name, "--"+str(self.index)+"--", size, date]
                masterlist.append(self.mylist)
                seeds = None
                self.mylist_crossite = [name, self.index, size, seeds, date]
                self.masterlist_crossite.append(self.mylist_crossite)
            return masterlist
        except Exception as e:
            self.logger.exception(e)
            print("Error message: %s" % (e))
            print("Something went wrong! See logs for details. Exiting!")
            sys.exit(2)

    def post_fetch(self, masterlist):
        """
        After output is displayed, Following text is displayed on console.

        Text includes instructions, total torrents fetched, total pages,
        and total time taken to fetch results.
        """
        self.logger.debug("Displaying output result table.")
        self.show_output(masterlist, self.output_headers)
        oplist = [self.index, self.total_fetch_time]
        self.logger.debug("Displaying after_output text: total torrents and fetch_time")
        self.after_output('xbit', oplist)
        self.logger.debug("Selecting torrent")
        while True:
            index = self.select_index(len(self.mapper))
            if index == 0:
                continue
            self.select_option(self.mapper, index, 'xbit')


def main(title):
    """Execution begins here."""
    try:
        print("\n[XBit.pw]\n")
        xb = XBit(title)
        print("Using %s" %(xb.colorify("yellow", xb.proxy)))
        print("Fetching results...")
        masterlist = xb.search_torrent()
        if masterlist is None:
            print("\nNo results found for given input!")
            xb.logger.debug("No results fetched!")
            sys.exit(2)
        xb.post_fetch(masterlist)
    except KeyboardInterrupt:
        xb.logger.debug("Keyboard interupt! Exiting!")
        print("\n\nAborted!")


def cross_site(title, page_limit):
    xb = XBit(title)
    return xb


if __name__ == "__main__":
    print("It's a module!")
