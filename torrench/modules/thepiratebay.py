"""The Pirate Bay Module."""

import sys
import platform
import webbrowser
import logging
import torrench.modules.tpb_details as tpb_details
from torrench.utilities.Config import Config


class ThePirateBay(Config):
    """
    ThePirateBay class.

    This class fetches torrents from TPB proxy,
    and diplays results in tabular form.
    Further, torrent details can be fetched which are
    stored in dynamically-generated HTML page.
    Details are fetched from tpb_details module
    and stored in $HOME/.torrench/temp directory.

    All activities are logged and stored in a log file.
    In case of errors/unexpected output, refer logs.
    """

    def __init__(self, title, page_limit):
        """Initialisations."""
        Config.__init__(self)
        self.proxies = self.get_proxies('tpb')
        self.top = "/top/all"
        self.top48 = "/top/48hall"
        self.title = title
        self.pages = page_limit
        self.logger = logging.getLogger('log1')
        self.page = 0
        self.proxy = None
        self.soup = None
        self.non_color_name = None
        self.soup_dict = {}
        self.OS_WIN = False
        if platform.system() == "Windows":
            self.OS_WIN = True
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
                if self.soup == -1 or self.soup.a.string != 'The Pirate Bay':
                    print("Bad proxy!")
                    count += 1
                    if count == len(self.proxies):
                        print("No more proxies found! Exiting...")
                        sys.exit(2)
                    else:
                        continue
                else:
                    print("Proxy available. Performing test...")
                    url = proxy+"/search/hello/0/99/0"
                    self.logger.debug("Carrying out test for string 'hello'")
                    self.soup = self.http_request(url)
                    test = self.soup.find('div', class_='detName')
                    if test is not None:
                        self.proxy = proxy
                        print("Pass!")
                        self.logger.debug("Test passed!")
                        break
                    else:
                        print("Test failed!\nPossibly site not reachable. See logs.")
                        self.logger.debug("Test failed!")
            except (AttributeError, Exception) as e:
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
                search = "/search/%s/%d/99/0" % (self.title, self.page)
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

    def get_top_html(self):
        """To get top torrents."""
        try:
            print(self.colorify("green", "\n\n*Top 100 TPB Torrents*"))
            print("1. Top (ALL)\n2. Top (48H)\n")
            option = int(input("Option: "))
            if option == 1:
                self.logger.debug("Selected [TOP-ALL] (Option: %d)" % (option))
                self.soup, time = self.http_request_time(self.proxy + self.top)
            elif option == 2:
                self.logger.debug("Selected [TOP-48h] (Option: %d)" % (option))
                self.soup, time = self.http_request_time(self.proxy + self.top48)
            else:
                print("Bad Input! Exiting!")
                sys.exit(2)
            self.total_fetch_time = time
            self.soup_dict[0] = self.soup
        except ValueError as e:
            print("Bad input! Exiting!")
            self.logger.exception(e)
            sys.exit(2)

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
                content = self.soup.find('table', id="searchResult")
                if content is None:
                    print("\nNo results found for given input!")
                    self.logger.debug("No results found for given input! Exiting!")
                    sys.exit(2)
                data = content.find_all('tr')

                for i in data[1:]:
                    name = i.find('a', class_='detLink').string
                    uploader = i.find('font', class_="detDesc").a
                    if name is None:
                        name = i.find('a', class_='detLink')['title'].split(" ")[2:]
                        name = " ".join(str(x) for x in name)
                    if uploader is None:
                        uploader = i.find('font', class_="detDesc").i.string
                    else:
                        uploader = uploader.string
                    if self.OS_WIN:
                        # Handling Unicode characters in windows.
                        name = name.encode('ascii', 'replace').decode()
                    comments = i.find(
                        'img', {'src': '//%s/static/img/icon_comment.gif' % (self.proxy.split('/')[2])})
                    # Total number of comments
                    if comments is None:
                        comment = '0'
                    else:
                        comment = comments['alt'].split(" ")[-2]
                    # See if uploader is VIP/Truested/Normal Uploader
                    self.non_color_name = name
                    is_vip = i.find('img', {'title': "VIP"})
                    is_trusted = i.find('img', {'title': 'Trusted'})
                    if(is_vip is not None):
                        name = self.colorify("green", name)
                        uploader = self.colorify("green", uploader)
                    elif(is_trusted is not None):
                        name = self.colorify("magenta", name)
                        uploader = self.colorify("magenta", uploader)
                    categ = i.find('td', class_="vertTh").find_all('a')[0].string
                    sub_categ = i.find('td', class_="vertTh").find_all('a')[1].string
                    seeds = i.find_all('td', align="right")[0].string
                    leeches = i.find_all('td', align="right")[1].string
                    date = i.find('font', class_="detDesc").get_text().split(' ')[1].replace(',', "")
                    size = i.find('font', class_="detDesc").get_text().split(' ')[3].replace(',', "")
                    # Unique torrent id
                    torr_id = i.find('a', {'class': 'detLink'})["href"].split('/')[2]
                    # Upstream torrent link
                    link = "%s/torrent/%s" % (self.proxy, torr_id)
                    magnet = i.find_all('a', {'title': 'Download this torrent using magnet'})[0]['href']
                    self.index += 1
                    self.mapper.insert(self.index, (name, magnet, link))

                    self.mylist = [categ + " > " + sub_categ, name, "--" +
                        str(self.index) + "--", uploader, size, seeds, leeches, date, comment]
                    masterlist.append(self.mylist)
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
        try:
            if self.pages is None:
                exact_no_of_pages = 1
            else:
                exact_no_of_pages = self.index // 30
                has_extra_pages = self.index % 30
                if has_extra_pages > 0:
                    exact_no_of_pages += 1
            print("\nTotal %d torrents [%d pages]" % (self.index, exact_no_of_pages))
            print("Total time: %.2f sec" % (self.total_fetch_time))
            self.logger.debug("fetched ALL results in %.2f sec" % (self.total_fetch_time))
            print("\nFurther, a torrent's details can be fetched (Description, comments, download (Magnetic) Link, etc.)")
            print("Enter torrent's index value to fetch details (Maximum one index)\n")
        except Exception as e:
            self.logger.exception(e)
            print("Error message: %s" %(e))
            print("Something went wrong! See logs for details. Exiting!")
            sys.exit(2)

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
                    sys.exit(2)
                elif temp < 0:
                    print("\nBad Input!")
                    continue
                else:
                    selected_torrent, req_magnetic_link, torrent_link = self.mapper[temp-1]
                    print("Selected index [%d] - %s\n" % (temp, selected_torrent))
                    self.logger.debug("selected torrent: %s ; index: %d" % (self.non_color_name, temp))
                    temp2 = input("1. Print magnetic link [p]\n2. Get torrent details [g]\n\nOption [p/g]: ")
                    temp2 = temp2.lower()
                    self.logger.debug("selected option: [%c]" % (temp2))
                    if temp2 == 'p':
                        print("\nMagnetic link - %s" %
                              (self.colorify("red",  req_magnetic_link)))
                        self.logger.debug("printing magnetic link and upstream link")
                        print("\nUpstream link - %s" % (self.colorify("yellow", torrent_link)))
                        temp3 = input("\nLoad to torrent client? [y/n]: ")
                        if temp3 == 'y' or temp3 == 'Y':
                            try:
                                self.logger.debug("Opening magnetic link in browser...")
                                webbrowser.open_new_tab(req_magnetic_link)
                            except Exception as e:
                                self.logger.exception(e)
                                continue
                        else:
                            self.logger.debug("NOT Opening magnetic link in browser.")
                            pass
                    elif temp2 == 'g':
                        print("Fetching details for torrent index [%d] : %s" % (
                            self.index, selected_torrent))
                        self.logger.debug("fetching torrent details...")
                        file_url = tpb_details.get_details(torrent_link, str(self.index))
                        self.logger.debug("details fetched. saved in %s" % (file_url))
                        file_url = self.colorify("yellow", file_url)
                        print("File URL: %s \n" % (file_url))
                    else:
                        self.logger.debug("Inappropriate input! Should be [p/g] only!")
                        print("Bad input!")
                        continue
            except (ValueError, IndexError, TypeError) as e:
                print("\nBad Input!")
                self.logger.exception(e)
                continue


def main(title, page_limit):
    """Execution begins here."""
    try:
        print("\n[The Pirate Bay]\n")
        print("Obtaining proxies...")
        tpb = ThePirateBay(title, page_limit)
        tpb.check_proxy()
        if title is None:
            tpb.get_top_html()
        else:
            tpb.get_html()
        tpb.parse_html()
        tpb.after_output_text()
        tpb.select_torrent()
    except KeyboardInterrupt:
        tpb.logger.debug("Keyboard interupt! Exiting!")
        print("\n\nAborted!")


if __name__ == "__main__":
    print("Its a module!")
