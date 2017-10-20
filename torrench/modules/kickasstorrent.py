"""KickassTorrents Module."""

import sys
import logging
from torrench.utilities.Config import Config


class KickassTorrents(Config):
    """
    KickassTorrent class.

    This class fetches torrents from KAT proxy,
    and diplays results in tabular form.
    Further, torrent's magnetic link and
    upstream link can be printed on console.
    Torrent can be added to client directly
    (still needs tweaking. may not work as epected)

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
        self.proxies = self.get_proxies('kat')
        self.title = title
        self.pages = page_limit
        self.logger = logging.getLogger('log1')
        self.page = 0
        self.proxy = None
        self.soup = None
        self.soup_dict = {}
        self.index = 0
        self.total_fetch_time = 0
        self.mylist = []
        self.mapper = []
        self.output_headers = [
                'CATEG', 'NAME', 'INDEX', 'UPLOADER', 'SIZE', 'S', 'L', 'DATE', 'C']

    def check_proxy(self):
        """
        To check proxy availability.

        Proxy is checked in two steps:
        1. To see if proxy 'website' is available.

        In case of failiur, next proxy is tested with same procedure.
        This continues until working proxy is found.
        If no proxy is found, program exits.
        """
        count = 0
        for proxy in self.proxies:
            print("Trying %s" % (self.colorify("yellow", proxy)))
            self.logger.debug("Trying proxy: %s" % (proxy))
            self.soup = self.http_request(proxy)
            if self.soup.find('a')['href'] != proxy + "full/" or self.soup == -1:
                print("Bad proxy!")
                count += 1
                if count == len(self.proxies):
                    self.logger.debug("Proxy list finished! Exiting!")
                    print("No more proxies found! Exiting...")
                    sys.exit(2)
            else:
                self.logger.debug("Connected to proxy...")
                print("Available!\n")
                self.proxy = proxy
                break

    def get_html(self):
        """
        To get HTML page.

        Once proxy is found, the HTML page for
        corresponding search string is fetched.
        Also, the time taken to fetch that page is returned.
        Uses http_request_time() from Common.py module.
        """
        for self.page in range(self.pages):
            print("\nFetching from page: %d" % (self.page+1))
            self.logger.debug("fetching page %d/%d" % (self.page, self.pages))
            search = "usearch/%s/%d/" % (self.title, self.page + 1)
            self.soup, time = self.http_request_time(self.proxy + search)
            print("Page fetched!")
            self.logger.debug("Page fetched in %.2f sec!" % (time))
            self.total_fetch_time += time
            self.soup_dict[self.page] = self.soup

    def parse_html(self):
        """
        Parse HTML to get required results.

        Results are fetched in masterlist list.
        Also, a mapper[] is used to map 'index'
        with torrent name, link and magnetic link
        """
        masterlist = []
        try:
            for page in self.soup_dict:
                self.soup = self.soup_dict[page]
                content = self.soup.find('table', class_='data')
                data = content.find_all('tr', class_='odd')
                for i in data:
                    name = i.find('a', class_='cellMainLink').string
                    if name is None:
                        name = i.find('a', class_='cellMainLink').get_text().split("[[")[0]
                    # Handling Unicode characters in windows.
                    torrent_link = i.find('a', class_='cellMainLink')['href']
                    uploader_name = i.find('span', class_='lightgrey').get_text().split(" ")[-4]
                    category = i.find('span', class_='lightgrey').get_text().split(" ")[-2]
                    verified_uploader = i.find('a', {'title': 'Verified Torrent'})
                    if verified_uploader is not None:
                        uploader_name = self.colorify("yellow", uploader_name)
                        comment_count = i.find('a', class_='icommentjs').get_text()
                    if comment_count == '':
                        comment_count = 0
                    misc_details = i.find_all('td', class_='center')
                    size = misc_details[0].string
                    date_added = misc_details[1].string
                    seeds = self.colorify("green", misc_details[2].string)
                    leeches = self.colorify("red", misc_details[3].string)
                    magnet = i.find('a', {'title': 'Torrent magnet link'})['href']
                    self.index += 1
                    self.mapper.insert(self.index, (name, magnet, torrent_link))

                    self.mylist = [category, name, '--' + str(self.index) + '--', uploader_name, size, date_added, seeds, leeches, comment_count]
                    masterlist.append(self.mylist)

            if masterlist == []:
                print("\nNo results found for given input!\n")
                self.logger.debug("\nNo results found for given input! Exiting!")
                sys.exit(2)
            self.logger.debug("Results fetched successfully!")
            self.show_output(masterlist, self.output_headers)
        except Exception as e:
            self.logger.exception(e)
            print("Error message: %s" %(e))
            print("Something went wrong! See logs for details. Exiting!")
            sys.exit(2)


    def after_output_text(self):
        """
        After output is displayed, Following text is displayed on console.

        Text includes instructions, total torrents fetched, total pages,
        and total time taken to fetch results.
        """
        oplist = [self.index, self.total_fetch_time]
        self.after_output('kat', oplist)


    def select_torrent(self):
        """
        To select required torrent.

        Torrent is selected through index value.
        Prints magnetic link and upstream link to console.
        Also, torrent can be added directly to client
        (Note: Might not work as expected.)
        """
        self.logger.debug("torrent select!")
        temp = 9999
        while(temp != 0):
            try:
                temp = int(input("\n(0=exit)\nindex > "))
                self.logger.debug("selected index: %d" % (temp))
                if temp == 0:
                    self.logger.debug("Torrench quit!")
                    print("\nBye!\n")
                    break
                elif temp < 0:
                    print("\nBad Input!")
                    continue
                else:
                    selected_torrent, req_magnetic_link, req_torr_link = self.mapper[temp-1]
                    selected_torrent = self.colorify("yellow", selected_torrent)
                    print("Selected index [%d] - %s\n" % (temp, selected_torrent))
                    self.logger.debug("selected torrent: %s ; index: %d" % (selected_torrent, temp))
                    # Print Magnetic link / load magnet to client
                    temp2 = input("\n1. Print magnetic link [p]\n2. Load magnetic link to client [l]\n\nOption [p/l]: ")
                    temp2 = temp2.lower()
                    self.logger.debug("selected option: [%c]" % (temp2))
                    if temp2 == 'p':
                        self.logger.debug("printing magnetic link and upstream link")
                        print("\nMagnet link: {magnet}".format(magnet=self.colorify("red", req_magnetic_link)))
                        self.copy_magnet(req_magnetic_link)
                        upstream_link = self.colorify("yellow", self.proxy + req_torr_link)
                        print("\n\nUpstream Link: %s \n\n" % (upstream_link))
                    elif temp2 == 'l':
                        try:
                            self.logger.debug("Loading torrent to client")
                            self.load_torrent(req_magnetic_link)
                        except Exception as e:
                            self.logger.exception(e)
                            continue
            except (ValueError, IndexError, TypeError) as e:
                print("\nBad Input!")
                self.logger.exception(e)
                continue


def main(title, page_limit):
    """Execution begins here."""
    try:
        print("\n[KickassTorrents]\n")
        print("Obtaining proxies...")
        kat = KickassTorrents(title, page_limit)
        kat.check_proxy()
        kat.get_html()
        kat.parse_html()
        kat.after_output_text()
        kat.select_torrent()
    except KeyboardInterrupt:
        kat.logger.debug("Keyboard interupt! Exiting!")
        print("\n\nAborted!")


if __name__ == "__main__":
    print("Its a module!")
