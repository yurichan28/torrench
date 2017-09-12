"""nyaa.si module"""

import sys
import logging
from torrench.utilities.Common import Common

class NyaaTracker(Common):
    """
    Nyaa.si class.

    This class fetches results from nyaa.si
    and displays in tabular form.
    Selected torrent is downloaded to hard-drive.

    Default download location is $HOME/Downloads/torrench
    """

    def __init__(self, title):
        """Class constructor"""
        Common.__init__(self)
        self.title = title
        self.logger = logging.getLogger('log1')
        self.output_headers = ['NAME', 'INDEX', 'SIZE', 'S', 'L', 'COMPLETED', 'ADDED']
        self.categ_url = "https://nyaa.si"
        self.index = 0
        self.categ_url_code = '0_0'
        self.mylist = []
        self.category_mapper = []
        self.mapper = []
        self.url = "https://nyaa.si/?f=0&c={category}&q={query}".format(category=self.categ_url_code,
                                                                        query=self.title)


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
                print("cat mapper %s" % self.category_mapper[0][2])
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

    def fetch_results(self):
        """
        Fetch results for a given query.

        @datafanatic:
        Work in progress
        """
        from requests import get
        from bs4 import BeautifulSoup
        print("Fetching results")
        self.logger.debug("Fetching...")
        self.logger.debug("Category URL code: %d\nURL: %s", self.categ_url_code, self.url)
        print(self.categ_url_code)
        print(self.url)
        req = get(self.url)
        soup = BeautifulSoup(req.text, 'html.parser')
        for item in soup.find_all('td', {'colspan': '2'}):
            t_names = [name.get_text() for x in item.find_all('td', {'colspan': '2'})]
            t_url = ['https://nyaa.si'+x['href'] for x in soup.find_all('a') if x['href'].startswith('/download')]
            t_size = item.find_all('td', {'class': 'text-center'}).get_text().endswith(("GiB", "MiB")).get_text()
        
        self.index = len(t_titles)
        #self.mapper.insert(self.index, (*titles, 1))
        #return self.mapper

    def select_torrent(self):
        """
        TODO
        """
        pass

    def get_torrent(self):
        """
        TODO
        """
        pass

def main(title):
    """
    Execution will begin here.
    """
    try:
        print("[Nyaa.si]")
        nyaa = NyaaTracker(title)
        prompt = input("Display categories? [y/n]: ")
        if prompt.lower() == 'y':
            nyaa.logger.debug("Displaying categories: %c", prompt)
            #nyaa.display_categories()
            #nyaa.select_category()
        else:
            nyaa.categ_url_code = '0_0'
            nyaa.logger.debug("Not displaying categories.")
        results = nyaa.fetch_results()
        nyaa.show_output(results, nyaa.output_headers)
        nyaa.select_torrent()
    except KeyboardInterrupt:
        nyaa.logger.debug("Interrupt detected. Terminating.")
        print("Terminated")

if __name__ == "__main__":
    main("naruto")
