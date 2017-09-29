import click
import torrench.modules.thepiratebay as tpb_module
import torrench.modules.kickasstorrent as kat
import torrench.modules.skytorrents as sky
import torrench.modules.nyaa as nyaa_module
import torrench.modules.xbit as xbit_module
import torrench.modules.distrowatch as distrowatch
import torrench.modules.linuxtracker as linuxtracker
from torrench.utilities.Config import Config

def parser(query):
    """
    :query: String to query the module.
    """
    if query[:2] == '!h' or query == 'help':
        interactive_help()
    elif query[:2] == '!t':
        caller(query[:2], query[3:])
    elif query[:2] == '!k':
        caller(query[:2], query[3:])
    elif query[:2] == '!n':
        caller(query[:2], query[3:])
    else:
        print('Invalid command! Try `!h` or `help` for help.')

def set_modules():
    """
    Map functions to commands and return dictionary.
    """
    if Config().file_exists():
        _modules = {'!t': tpb_module,
                    '!n': nyaa_module,
                    '!k': kat,
                    '!x': xbit_module,
                    '!d': distrowatch,
                    '!l': linuxtracker,
                    '!s': sky
                   }
        return _modules
    else:
        _public_modules = {'!d': distrowatch,
                           '!l': linuxtracker
                          }
        return _public_modules

def caller(module, query):
    """
    Send queries to their respective modules.

    :module: Module to use in query.
    :query: String to search for.
    """
    _modules = set_modules()
    if module in _modules:
        print(module)
        if module in ['!t', '!k', '!s']:
            _modules[module].main(query, page_limit=1)
        else:
            _modules[module].main(query)


def interactive_help():
    """
    Display help
    """
    help_text = """
        Available commands:
    !h <string> - Help text (this)
    !n <string> - Search on nyaa.si for anime.
    !t <string> - Search on ThePirateBay.
    !k <string> - Search on KickAssTorrents.
    !s <string> - Search on SkyTorrents
    !x <string> - Search on XBit.pw
    !t <string> - Search on LinuxTorrents

    Some commands are only available after a `config.ini` file has been set.
    See the documentation for more information.
    """
    print(help_text)


@click.command()
@click.option('--interactive', '-i', is_flag=True)
def inter(interactive):
    """
    Execution will start here.
    """
    if interactive:
        print("Interactive mode is ENABLED!")
        try:
            while True:
                data = input('torrench > ')
                parser(data)
        except KeyboardInterrupt:
            print('Terminated.')
    else:
        print("not enabled")

if __name__ == '__main__':
    inter(None)
