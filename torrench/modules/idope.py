"""Idope Module."""

import logging
import sys

from torrench.utilities.Config import Config


class Idope(Config):
    """
    Idope class.

    This class fetches torrents from Idope website,
    and diplays results in tabular form.
    Further, torrent's magnetic link,
    upstream link and files to be downloaded with torrent can be
    printed on console.
    Torrent can be added to client directly

    This class inherits Config class. Config class inherits
    Common class. The Config class provides proxies list fetched
    from config file. The Common class consists of commonly used
    methods.

    All activities are logged and stored in a log file.
    In case of errors/unexpected output, refer logs.
    """

    def __init__(self, title, page_limit):
        """Initialisations."""
        Config.__init__(self)
        self.proxies = self.get_proxies('idope')
        self.proxy = self.proxies[0]
        self.logger = logging.getLogger('log1')
        self.title = title
        self.pages = page_limit
        self.soup = None
        self.soup_dict = {}
        self.page = 0
        self.total_fetch_time = 0
        self.index = 0
        self.mylist = []
        self.mapper = []
        self.output_headers = [
                'NAME', 'INDEX', 'SIZE', 'SEEDS', 'AGE']

    def get_html(self):
        """
        To get HTML page.

        Once proxy is found, the HTML page for
        corresponding search string is fetched.
        Also, the time taken to fetch that page is returned.
        Uses http_request_time() from Common.py module.
        """
        try:
            for self.page in range(self.pages):
                print("\nFetching from page: %d" % (self.page+1))
                search = "/torrent-list/{}/?p={}".format(self.title, self.page+1)
                self.soup, time = self.http_request_time(self.proxy + search)
                self.logger.debug("fetching page %d/%d" % (self.page+1, self.pages))
                print("[in %.2f sec]" % (time))
                self.logger.debug("page fetched in %.2f sec!" % (time))
                self.total_fetch_time += time
                self.soup_dict[self.page] = self.soup
        except Exception as e:
            self.logger.exception(e)
            print("Error message: %s" %(e))
            print("Something went wrong! See logs for details. Exiting!")
            sys.exit(2)

    def parse_html(self):
        """
        Parse HTML to get required results.

        Results are fetched in masterlist list.
        Also, a mapper[] is used to map 'index'
        with torrent name, link and magnetic link
        """
        try:
            masterlist = []
            for page in self.soup_dict:
                self.soup = self.soup_dict[page]
                results = self.soup.findAll('div', class_='resultdiv')
                trackers = self.soup.find('input', id='hidetrack')['value']
                if results == []:
                    print("\nNo results found for given input!")
                    self.logger.debug("No results found for given input! Exiting!")
                    sys.exit(2)
                for result in results:
                    name = " ".join(result.a.div.string.split())
                    link = result.a['href']
                    link = self.proxy + link
                    r = result.find('div', class_='resultdivbotton').text.split()
                    age = "{} {}".format(r[2], r[3])
                    size = "{} {}".format(r[5], r[6])
                    seeds = r[8]
                    seeds = self.colorify("green", seeds)
                    #files = r[10]
                    info_hash = r[11]
                    magnet = "magnet:?xt=urn:btih:{}&dn={}{}".format(info_hash, name, trackers)
                    self.index += 1
                    self.mapper.insert(self.index, (name, magnet, link))
                    self.mylist = [name, "--" +
                        str(self.index) + "--", size, seeds, age]
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
        self.after_output('idope', oplist)

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
            self.select_option(self.mapper, index, 'idope')

def main(title, page_limit):
    """Execution begins here."""
    print("\n[Idope]")
    idp = Idope(title, page_limit)
    idp.get_html()
    idp.parse_html()
    idp.after_output_text()
    idp.select_torrent()


if __name__ == "__main__":
    print("It's a module!")
