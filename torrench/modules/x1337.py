"""1337x Module."""

import sys
import platform
import logging
from torrench.utilities.Config import Config


class x1337(Config):
    """
    1337x class.

    This class fetches torrents from 1337x website,
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
        self.proxies = self.get_proxies('1337x')
        self.proxy = None
        self.title = title
        self.pages = page_limit
        self.logger = logging.getLogger('log1')
        self.OS_WIN = False
        if platform.system() == "Windows":
            self.OS_WIN = True
        self.index = 0
        self.page = 0
        self.total_fetch_time = 0
        self.mylist = []
        self.mapper = []
        self.soup_dict = {}
        self.output_headers = [
                'CATEG', 'NAME', 'INDEX', 'SE', 'LE', 'TIME', 'SIZE', 'UL', 'C']

    def check_proxy(self):
        """
        To check proxy availability.

        Proxy is checked in two steps:
        1. To see if proxy 'website' is available.
        2. A test is carried out with a sample string 'hello'.
        If results are found, test is passed, else test failed!

        This class inherits Config class. Config class inherits
        Common class. The Config class provides proxies list fetched
        from config file. The Common class consists of commonly used
        methods.

        In case of failiur, next proxy is tested with same procedure.
        This continues until working proxy is found.
        If no proxy is found, program exits.
        """
        count = 1
        for proxy in self.proxies:
            print("Trying %s" % (self.colorify("yellow", proxy)))
            self.logger.debug("Trying proxy: %s" % (proxy))
            self.soup = self.http_request(proxy)
            try:
                if self.soup == -1 or "1337x" not in self.soup.head.title.string:
                    print("Bad proxy!")
                    count += 1
                    if count == len(self.proxies):
                        print("No more proxies found! Exiting...")
                        sys.exit(2)
                    else:
                        continue
                else:
                    print("Proxy available. Performing test...")
                    url = proxy+"/search/hello/1/"
                    self.logger.debug("Carrying out test for string 'hello'")
                    self.soup = self.http_request(url)
                    test = self.soup.find('table', class_='table-list')
                    if test is not None:
                        self.proxy = proxy
                        print("Pass!")
                        self.logger.debug("Test passed!")
                        break
                    else:
                        print("Test failed!\nPossibly site not reachable. (See logs)")
                        self.logger.debug("Test failed!")
            except (AttributeError, Exception) as e:
                print("Proxy not available\n")
                self.logger.exception(e)
                pass

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
                search = "/search/{}/{}/".format(self.title, self.page+1)
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
                content = self.soup.find('table', class_='table-list')
                if content is None:
                    print("\nNo results found for given input!")
                    self.logger.debug("No results found for given input! Exiting!")
                    sys.exit(2)
                results = content.find_all('tr')
                for result in results[1:]:
                    content = result.findAll('td')
                    if len(content[0].findAll(text=True)) == 2:
                        name, comments = content[0].findAll(text=True)
                    else:
                        name = content[0].findAll(text=True)[0]
                        comments = 0
                    link = content[0].findAll('a')[1]['href']
                    link = self.proxy + link
                    category = content[0].a.i['class'][0].split('-')[1]
                    category = category.title()
                    seeds = content[1].string
                    leeches = content[2].string
                    if not self.OS_WIN:
                        seeds = self.colorify("green", seeds)
                        leeches = self.colorify("red", leeches)
                    date = content[3].string
                    size = content[4].findAll(text=True)[0]
                    uploader = content[5].string
                    uploader_status = content[5]['class'][1]
                    if uploader_status == 'vip':
                        name = self.colorify("cyan", name)
                        uploader = self.colorify("cyan", uploader)
                    self.index += 1
                    self.mapper.insert(self.index, (name, link))
                    self.mylist = [category, name, "--" +
                        str(self.index) + "--", seeds, leeches, date, size, uploader, comments]
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

        Text includes total torrents fetched, total pages,
        and total time taken to fetch results.
        """
        oplist = [self.index, self.total_fetch_time]
        self.after_output('x1337', oplist)

    def select_torrent(self):
        """
        To select required torrent.
        Torrent is selected through index value.
        Two options are present:
        1. To print magnetic link and upstream link to console.
        Further, torrent can be added directly to client (Note: May not work everytime.)
        2. To fetch torrent details (saved in dynamically generated .html file)
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
                    selected_torrent, torrent_link = self.mapper[temp-1]
                    print("Selected index [%d] - %s\n" % (temp, selected_torrent))
                    self.logger.debug("selected torrent: %s ; index: %d" % (selected_torrent, temp))
                    temp2 = input("1. Print links [p]\n2. Load magnetic link to client [l]\n\nOption [p/l]: ")
                    temp2 = temp2.lower()
                    self.logger.debug("selected option: [%c]" % (temp2))
                    if temp2 == 'p':
                        self.logger.debug("printing magnetic link and upstream link")
                        req_magnetic_link = self.get_torrent_info(torrent_link)
                        print("\nMagnetic link - %s" % (self.colorify("red",  req_magnetic_link)))
                        self.copy_magnet(req_magnetic_link)
                        print("\n\nUpstream link - %s\n" % (self.colorify("yellow", torrent_link)))
                    elif temp2 == 'l':
                        try:
                            self.logger.debug("Loading magnetic link to client")
                            req_magnetic_link = self.get_torrent_info(torrent_link)
                            self.load_torrent(req_magnetic_link)
                        except Exception as e:
                            self.logger.exception(e)
                            continue
                    else:
                        self.logger.debug("Inappropriate input! Should be [p/l] only!")
                        print("Bad input!")
                        continue
            except (ValueError, IndexError, TypeError) as e:
                print("\nBad Input!")
                self.logger.exception(e)
                continue

    def get_torrent_info(self, link):
        """Module to get magnetic link of torrent.

        Magnetic link is fetched from torrent's info page.
        """
        print("Fetching magnetic link...")
        self.logger.debug("Fetching magnetic link")
        soup = self.http_request(link)
        magnet = soup.find('ul', class_="download-links-dontblock").a['href']
        return magnet



def main(title, page_limit):
    """Execution begins here."""
    print("\n[1337x]\n")
    print("Obtaining proxies...")
    x13 = x1337(title, page_limit)
    x13.check_proxy()
    x13.get_html()
    x13.parse_html()
    x13.after_output_text()
    x13.select_torrent()
