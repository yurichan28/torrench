"""Idope Module."""

import sys
from torrench.utilities.Config import Config
import logging


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
        To select required torrent.

        Torrent is selected through index value.
        Two options are present:
        1. To print magnetic link and upstream link to console.
        Further, torrent can be added directly to client (Note: May not work everytime.)
        2. To load torrent to client.
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


def main(title, page_limit):
    """Execution begins here."""
    print("\n[Idope]")
    idp = Idope(title, page_limit)
    idp.get_html()
    idp.parse_html()
    idp.after_output_text()
    idp.select_torrent()


if __name__ == "__main__":
    main()
