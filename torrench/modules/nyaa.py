"""nyaa.si module."""

import logging
import platform
import sys

from torrench.utilities.Config import Config


class Nyaa(Config):
    """
    Nyaa.si class.

    This class fetches results from nyaa.si
    and displays in tabular form.

    Known problems:
    - If the torrent name in the website is too long (200 chars+) the table will be displayed incorrectly in the terminal.
    Possible fixes:
    - Cut the name if the name is too big.
    """

    def __init__(self, title, page_limit):
        """Class constructor"""
        Config.__init__(self)
        self.proxies = self.get_proxies('nyaa')
        self.proxy = self.proxies[0]
        self.title = title
        self.pages = page_limit
        self.logger = logging.getLogger('log1')
        self.index = 0
        self.mapper = []
        self.mylist_crossite = []
        self.masterlist_crossite = []
        self.page = 0
        self.soup = None
        self.total_fetch_time = 0
        self.soup_dict = {}
        self.OS_WIN = False
        if platform.system() == "Windows":
            self.OS_WIN = True
        self.output_headers = ['NAME', 'INDEX', 'SIZE', 'SE/LE', 'COMPLETED']

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
                print("Fetching from page: %d" % (self.page+1))
                search = "/?f=0&c=0_0&q={}&s=seeders&o=desc&p={}".format(self.title, self.page+1)
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
        with torrent name and link
        """
        masterlist = []
        try:
            for page in self.soup_dict:
                self.soup = self.soup_dict[page]
                results = self.soup.findAll('tr', class_='success')
                if results == []:
                    return
                for result in results:
                    pre_data = result.findAll('a')
                    name = pre_data[-3].string
                    link = pre_data[-3]['href']
                    magnet = pre_data[-1]['href']
                    data = result.findAll('td')
                    size = data[3].string
                    date = data[4].string
                    seeds = data[5].string
                    leeches = data[6].string
                    completed = data[7].string
                    if not self.OS_WIN:
                        seeds_color = self.colorify("green", seeds)
                        leeches_color = self.colorify("red", leeches)
                    else:
                        seeds_color = seeds
                        leeches_color = leeches
                    self.index += 1
                    self.mapper.insert(self.index, (name, magnet, self.proxy+link))
                    self.mylist = [name, "--" +
                        str(self.index) + "--", seeds_color + '/' + leeches_color, date, size, completed]
                    masterlist.append(self.mylist)
                    self.mylist_crossite = [name, self.index, size, seeds+'/'+leeches, date]
                    self.masterlist_crossite.append(self.mylist_crossite)
            self.logger.debug("Results fetched successfully!")
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
        self.after_output('nyaa', oplist)
        self.logger.debug("Selecting torrent")
        while True:
            index = self.select_index(len(self.mapper))
            if index == 0:
                continue
            self.select_option(self.mapper, index, 'nyaa')


def main(title, page_limit):
    """
    Execution will begin here.
    """
    try:
        print("\n[Nyaa.si]\n")
        nyaa = Nyaa(title, page_limit)
        nyaa.get_html()
        masterlist = nyaa.parse_html()
        if masterlist is None:
            print("\nNo results found for given input!")
            nyaa.logger.debug("\nNo results found for given input! Exiting!")
            sys.exit(2)
        nyaa.post_fetch(masterlist)
    except KeyboardInterrupt:
        nyaa.logger.debug("Interrupt detected. Terminating.")
        print("Terminated")


def cross_site(title, page_limit):
    nyaa = Nyaa(title, page_limit)
    return nyaa


if __name__ == "__main__":
    print("Modules are not supposed to be run standalone")
