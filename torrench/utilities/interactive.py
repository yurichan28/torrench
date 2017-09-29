import click
import torrench.modules
from torrench.utilities.Config import Config

def parser(q):

    if q[:2] == '!h':
        help()
    elif q[:2] == '!t':
        tpb(q[3:]) if q[3:] else print('Empty query.')
    elif q[:2] == '!k':
        caller(q[:2], q[3:])
    elif q[:2] == '!n':
        nyaa(None)


def caller(module, q):
    if config_check():
        _modules = {'private_modules': {'!t': torrench.modules.thepiratebay.main,
                                        '!n': torrench.modules.nyaa.main,
                                        '!k': torrench.modules.kickasstorrent.main,
                                        '!x': torrench.modules.xbit.main
                                        }
                    }
        if module in _modules['private_modules']:
            print('Using module `%s`.' % module)
    else:
        _modules = {'public_modules': {'!d': torrench.modules.distrowatch,
                                       '!lt': torrench.modules.linuxtracker}}


def config_check():
    if not Config().file_exists():
        print("Missing configuration. See the documentation.")
        return 0
    return 1


def help():
    help_text = """
        Available commands:
    !h <string> - Help text (this)
    !n <string> - Search on nyaa.si for anime.
    !t <string> - Search on ThePirateBay.
    !k <string> - Search on KickAssTorrents.
    !x <string> - Search on XBit.pw
    !t <string> - Search on LinuxTorrents

    Some commands are only available after a `config.ini` file has been set.
    See the documentation for more information.
    """
    print(help_text)


def nyaa(q):
    print('Searching for {query} in Nyaa.'.format(query=q))
    torrench.modules.nyaa.main(q)


def xbit(q):
    print('Searching for {query} in XBit.'.format(query=q))
    torrench.modules.xbit.main(q)


def tpb(q):
    print('Searching for {query} on TPB.'.format(query=q))
    torrench.modules.thepiratebay.main(q, 1)


@click.command()
@click.option('--interactive', '-i', is_flag=True)
def inter(interactive):
    if interactive:
        print("Interactive mode is ENABLED!")
        data = input('torrench > ')
        parser(data)
    else:
        print("not enabled")

if __name__ == '__main__':
    inter(None)