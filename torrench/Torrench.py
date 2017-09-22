"""Torrench Module."""

import os
import sys
import argparse
import logging
from torrench.utilities.Config import Config


class Torrench(Config):
    """
    Torrench class.

    This class resolves input arguments.
    Following arguments are present -

    positional arguments:
      search                Enter search string

    optional arguments:
      -h, --help            show this help message and exit
      -d, --distrowatch     Search distrowatch
      -t, --thepiratebay    Search thepiratebay (TPB)
      -k, --kickasstorrent  Search KickassTorrent (KAT)
      -s, --skytorrents     Search SkyTorrents
      -n, --nyaa            Search Nyaa.si
      --top                 Get top torrents
      -p LIMIT, --page-limit LIMIT
                            Number of pages to fetch results from (1 page = 30 results). [default: 1]
      -c, --clear-html      Clear all [TPB] torrent description HTML files and exit.
      -v, --version         Display version and exit.
    """

    def __init__(self):
        """Initialisations."""
        Config.__init__(self)
        self.__version__ = "Torrench (1.0.52)"
        self.logger = logging.getLogger('log1')
        self.args = None
        self.input_title = None
        self.page_limit = 0

    def define_args(self):
        """All input arguments are defined here."""
        self.logger.debug("command-input: %s" % (sys.argv))
        parser = argparse.ArgumentParser(description="Command-line torrent search tool.")
        parser.add_argument("-d",
                            "--distrowatch",
                            action="store_true",
                            help="Search distrowatch")
        parser.add_argument("-t",
                            "--thepiratebay",
                            action="store_true",
                            help="Search thepiratebay (TPB)")
        parser.add_argument("-k",
                            "--kickasstorrent",
                            action="store_true",
                            help="Search KickassTorrent (KAT)")
        parser.add_argument("-x",
                            "--xbit",
                            action="store_true",
                            help="Search XBit.pw")
        parser.add_argument("search",
                            help="Enter search string",
                            nargs="?",
                            default=None)
        parser.add_argument("-s",
                            "--skytorrents",
                            action="store_true",
                            help="Search SkyTorrents")
        parser.add_argument("-n",
                            "--nyaa",
                            action="store_true",
                            help="Search Nyaa")
        parser.add_argument("-x",
                            "--xbit",
                            action="store_true",
                            help="Search XBit.pw")
        parser.add_argument("--top",
                            action="store_true",
                            default=False,
                            help="Get top torrents")

        parser.add_argument("-p",
                            "--page-limit",
                            type=int,
                            help="Number of pages to fetch results from (1 page = 30 results).\n [default: 1]",
                            default=1,
                            dest="limit")
        parser.add_argument("-c",
                            "--clear-html",
                            action="store_true",
                            default=False,
                            help="Clear all [TPB] torrent description HTML files and exit.")
        parser.add_argument("-v",
                            "--version",
                            action='version',
                            version=self.__version__,
                            help="Display version and exit.")
        self.args = parser.parse_args()

    def remove_temp_files(self):
        """
        To remove TPB HTML files (-c).

        Clearing HTML files only works for TPB (-t)
        (since only TPB generates HTML for torrent descriptions)
        Default location for temp files is
        ~/.torrench/temp (Windows/linux)
        """
        self.logger.debug("Selected -c :: remove tpb temp html files.")
        home = os.path.expanduser(os.path.join('~', '.torrench'))
        temp_dir = os.path.join(home, "temp")
        self.logger.debug("temp directory default location: %s" % (temp_dir))
        if not os.path.exists(temp_dir):
            print("Directory not initialised. Exiting!")
            self.logger.debug("directory not found")
            sys.exit(2)
        files = os.listdir(temp_dir)
        if not files:
            print("Directory empty. Nothing to remove")
            self.logger.debug("Directory empty!")
            sys.exit(2)
        else:
            for count, file_name in enumerate(files, 1):
                os.remove(os.path.join(temp_dir, file_name))
            print("Removed {} file(s).".format(count))
            self.logger.debug("Removed {} file(s).".format(count))
            sys.exit(2)

    def verify_input(self):
        """To verify if input given is valid or not."""
        if self.input_title is None:
            self.logger.debug("Bad input! Input string expected! Got 'None'")
            print("\nInput string expected.\nUse --help for more\n")
            sys.exit(2)

        if self.page_limit <= 0 or self.page_limit > 50:
            self.logger.debug("Invalid page_limit entered: %d" % (tr.page_limit))
            print("Enter valid page input [0<p<=50]")
            sys.exit(2)

    def resolve_args(self):
        """Resolve input arguments."""
        _PRIVATE_MODULES = (
            self.args.thepiratebay,
            self.args.kickasstorrent,
            self.args.skytorrents,
            self.args.nyaa,
            self.args.xbit
        ) # These modules are only enabled through manual configuration.
        if self.args.clear_html:
            if not self.args.thepiratebay:
                print("error: use -c with -t")
                sys.exit(2)
            else:
                self.remove_temp_files()


        if any(_PRIVATE_MODULES):
            if not self.file_exists():
                print("\nConfig file not configured. Configure to continue. Read docs for more info.\n")
                print("Config file either does not exist or is not enabled! Exiting!")
                sys.exit(2)
            else:
                if self.args.thepiratebay:
                    self.logger.debug("using thepiratebay")
                    if self.args.top:
                        self.logger.debug("selected TPB TOP-torrents")
                        self.input_title = None
                        self.page_limit = None
                    self.logger.debug("Input title: [%s] ; page_limit: [%s]" % (self.input_title, self.page_limit))
                    import torrench.modules.thepiratebay as tpb
                    tpb.main(self.input_title, self.page_limit)
                elif self.args.kickasstorrent:
                    self.logger.debug("Using kickasstorrents")
                    self.logger.debug("Input title: [%s] ; page_limit: [%s]" % (self.input_title, self.page_limit))
                    import torrench.modules.kickasstorrent as kat
                    kat.main(self.input_title, self.page_limit)
                elif self.args.skytorrents:
                    self.logger.debug("Using skytorrents")
                    if self.args.top:
                        self.logger.debug("selected SkyTorrents TOP-torrents")
                        self.input_title = None
                        self.page_limit = None
                    self.logger.debug("Input title: [%s] ; page_limit: [%s]" % (self.input_title, self.page_limit))
                    import torrench.modules.skytorrents as sky
                    sky.main(self.input_title, self.page_limit)
                elif self.args.nyaa:
                    self.logger.debug("Using Nyaa.si")
                    import torrench.modules.nyaa as nyaa
                    nyaa.main(self.input_title)
                elif self.args.xbit:
                    self.logger.debug("Using XBit.pw")
                    self.logger.debug("Input title: [%s]" % (self.input_title))
                    import torrench.modules.xbit as xbit
                    xbit.main(self.input_title)
        elif self.args.distrowatch:
            self.logger.debug("Using distrowatch")
            self.logger.debug("Input title: [%s]" % (self.input_title))
            import torrench.modules.distrowatch as distrowatch
            distrowatch.main(self.input_title)
        else:
            self.logger.debug("Using linuxtracker")
            self.logger.debug("Input title: [%s]" % (self.input_title))
            import torrench.modules.linuxtracker as linuxtracker
            linuxtracker.main(self.input_title)


def main():
    """Execution begins here."""
    try:
        tr = Torrench()
        tr.define_args()
        if tr.args.top:
            if tr.args.thepiratebay or tr.args.skytorrents:
                tr.resolve_args()
            else:
                print("error: --top is only supported with -t/-s")
                sys.exit(2)
        else:
            tr.input_title = tr.args.search
            tr.page_limit = tr.args.limit
            if not tr.args.clear_html:
                tr.verify_input()
                tr.input_title = tr.input_title.replace("'", "")
            tr.resolve_args()
    except KeyboardInterrupt as e:
        tr.logger.debug("Keyboard interupt! Exiting!")
        print("\n\nAborted!")

if __name__ == '__main__':
    main()