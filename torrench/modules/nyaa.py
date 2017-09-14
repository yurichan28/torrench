"""nyaa.si module"""

import sys
import logging
from torrench.utilities.Config import Config

class NyaaTracker(Config):
    """
    Nyaa.si class.

    This class fetches results from nyaa.si
    and displays in tabular form.
    Selected torrent is downloaded to hard-drive.

    Default download location is $HOME/Downloads/torrench

    Known problems:
    - If the torrent name in the website is too long (200 chars+) the table will be displayed incorrectly in the terminal.
    Possible fixes:
    - Cut the name if the name is too big.
    """

    def __init__(self, title):
        """Class constructor"""
        Config.__init__(self)
        self.title = title
        self.logger = logging.getLogger('log1')
        self.output_headers = ['NAME', 'INDEX', 'SIZE', 'S', 'L']
        self.index = 0
        self.categ_url_code = '0_0'
        self.category_mapper = []
        self.mapper = []
        self.proxy = self.check_proxy('nyaa')
        self.search_parameter = "/?f=0&c=0_0&q={query}&s=seeders&o=desc".format(query=self.title)
        self.soup = self.http_request(self.proxy+self.search_parameter)

    def check_proxy(self, proxy):
        _torrench_proxies = self.get_proxies(proxy)
        counter = 0
        try:
            if _torrench_proxies:
                for proxy in _torrench_proxies:
                    print("Testing: {proxy}".format(proxy=self.colorify("yellow", proxy)))
                    proxy_soup = self.http_request(proxy+'/?f=0&c=0_0&q=hello&s=seeders&o=desc')
                    self.logger.debug("Testing {proxy} as a possible candidate.".format(proxy=proxy))
                    if not proxy_soup.find_all('td', {'colspan': '2'}):
                        print("{proxy} was a bad proxy. Trying next proxy.".format(proxy=proxy))
                        counter += 1
                        if counter == len(_torrench_proxies):
                            self.logger.debug("Proxy list finished. No valid proxies were found.")
                            print("Failed to find any valid proxies. Terminating.")
                            sys.exit(2)
                    else:
                        print("Proxy `{proxy}` is available. Connecting.".format(proxy=proxy))
                        self.logger.debug("Proxy `{proxy}` is a valid proxy.")
                        return proxy
                print("No proxies were given.")
                sys.exit(2)
        except (IndexError, ValueError) as error:
            print("Something went wrong. Logging and terminating.")
            print("The exception was: ")
            print(error)
            self.logger.exception(error)

    def display_categories(self):
        """
        Display the categories available in the website.
        The categories in this scraper have been hardcoded since they are dynamically generated
        in the website.

        @datafanatic:
        An easy way to solve this would be using PhantomJS or Selenium, but it would add unecessary
        overhead to the program. As such, I'll leave it up to future contributors the decision
        of whether to add it or keep using the following method.
        """
        self.logger.debug("Displaying categories in the nyaa module")
        categories = {'All categories': '0_0',
                      'Anime': '1_0',
                      'Audio': '2_0',
                      'Literature': '3_0',
                      'Live Action': '4_0',
                      'Pictures': '5_0',
                      'Software': '6_0'
                     }
        count = len(categories.keys())
        for idx, item in enumerate(categories):
            self.category_mapper.insert(idx, (idx, item, categories[item]))
            print("[{index}] {category}".format(index=idx, category=item))
        self.logger.debug("Total categories displayed: %d", count)

    def select_category(self):
        """
        Select a category from the list.

        Categories are associated with an index, and
        can be selected using that index. Each category has an unique index and url code.
        The URL code is mapped to the category index.
        """
        self.logger.debug("Prompting for category in the nyaa module")
        try:
            prompt = int(input("\nSelect category (0=none): "))
            self.logger.debug("Selected index `%d` in the nyaa module", prompt)
            if prompt == 0:
                self.categ_url_code = self.category_mapper[0][2]
                print("Selected category: {category}".format(category=self.category_mapper[0][1]))
            else:
                selected_category, self.categ_url_code = self.category_mapper[prompt], self.category_mapper[prompt][2]
                print("Selected [{idx}]: {category} ".format(idx=prompt,
                                                             category=selected_category[1]))
                self.logger.debug("Selected category %s with index %d", selected_category[1], prompt)
                self.logger.debug("Category URL code: `%s`", selected_category[2])
        except (ValueError, IndexError, KeyError) as killed:
            self.logger.exception(killed)
            print("Input needs to be an integer number.")
            sys.exit(2)

    def parse_name(self):
        """
        Parse torrent name
        """
        t_names = []
        for name in self.soup.find_all('td', {'colspan': '2'}):
            t_names.append(name.get_text().replace('\n', ''))
        if t_names:
            return t_names
        return "Unable to parse torrent name."

    def parse_urls(self):
        t_urls = []
        for url in self.soup.find_all('a'):
            try:
                if url.get('href').startswith('/download/'):
                    t_urls.append('https://nyaa.si'+url['href'])
            except AttributeError:
                pass
        if t_urls:
            return t_urls
        return "Unable to parse torrent URLs."

    def parse_sizes(self):
        t_size = []
        for size in self.soup.find_all('td', {'class': 'text-center'}):
            if size.get_text().endswith(("GiB", "MiB")):
                t_size.append(self.colorify("yellow", size.get_text()))
            else:
                pass
        if t_size:
            return t_size
        return "Unable to parse size of files."

    def parse_seeds(self):
        t_seeds = []
        for seed in self.soup.find_all('td', {'style': 'color: green;'}):
            t_seeds.append(self.colorify("green", seed.get_text()))
        if t_seeds:
            return t_seeds
        return "Unable to parse seeds"

    def parse_leeches(self):
        t_leeches = []
        for leech in self.soup.find_all('td', {'style': 'color: red;'}):
            t_leeches.append(self.colorify("red", leech.get_text()))
        if t_leeches:
            return t_leeches
        return "Unable to parse leechers"

    def fetch_results(self):
        """
        Fetch results for a given query.

        @datafanatic:
        Work in progress
        """
        print("Fetching results")
        self.logger.debug("Fetching...")
        self.logger.debug("URL: %s", self.url)
        try:
            name = self.parse_name()
            urls = self.parse_urls()
            sizes = self.parse_sizes()
            seeds = self.parse_seeds()
            leeches = self.parse_leeches()
            self.index = len(urls)
        except (KeyError, AttributeError) as e:
            print("Something went wrong. Logging and terminating.")
            self.logger.exception(e)
            print("OK. Terminating.")
        if self.index == 0:
            print("No results were found for the given query. Terminating")
            self.logger.debug("No results were found for `%s`.", self.title)
            return -1
        self.logger.debug("Results fetched. Showing table.")
        self.mapper.insert(self.index+1, (name, urls))
        return list(zip(name, ["--"+str(idx)+"--" for idx in range(self.index)], sizes, seeds, leeches))

    def select_torrent(self):
        """
        Select torrent from table using index.
        """
        while True:
            try:
                prompt = int(input("(0 to terminate) Index> "))
                if prompt == 0:
                    print("Bye!")
                    break
                else:
                    selected_index, download_url = self.mapper[0][0][prompt], self.mapper[0][1][prompt]
                    print("Downloading: \n" + selected_index)
                    self.get_torrent(download_url, selected_index)
            except IndexError as e:
                self.logger.exception(e)
                print("Invalid index.")

    def get_torrent(self, url, name):
        """
        Download the .torrent file to the computer.
        """
        self.download(url, name+'.torrent')

def main(title):
    """
    Execution will begin here.
    """
    try:
        print("[Nyaa.si]")
        nyaa = NyaaTracker(title)
        results = nyaa.fetch_results()
        nyaa.show_output([result for result in results], nyaa.output_headers)
        nyaa.select_torrent()
    except KeyboardInterrupt:
        nyaa.logger.debug("Interrupt detected. Terminating.")
        print("Terminated")

if __name__ == "__main__":
    main("naruto")
    #print("Modules are not supposed to be run standalone.")