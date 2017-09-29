import click
import torrench.modules.thepiratebay as tpb_module
import torrench.modules.kickasstorrent as kat
import torrench.modules.skytorrents as sky
import torrench.modules.nyaa as nyaa_module
import torrench.modules.xbit as xbit_module
import torrench.modules.distrowatch as distrowatch
import torrench.modules.linuxtracker as linuxtracker
from torrench.utilities.Config import Config

def parser(q):

    if q[:2] == '!h':
        help()
    elif q[:2] == '!t':
        caller(q[:2], q[3:])
    elif q[:2] == '!k':
        caller(q[:2], q[3:])
    elif q[:2] == '!n':
        caller(q[:2], q[3:])

def set_modules():
    if Config().file_exists():
        _modules = {'!t': tpb_module,
                    '!n': nyaa_module,
                    '!k': kat,
                    '!x': xbit_module,
                    '!d': distrowatch.main,
                    '!lt': linuxtracker.main
                   }
        return _modules
    else:
        _public_modules = {'!d': distrowatch.main,
                            '!lt': linuxtracker.main
                          }
        return _public_modules

def caller(module, q):
    _modules = set_modules()
    if module in _modules:
        print('Using module `%s`.' % module)
        print(_modules[module])


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


@click.command()
@click.option('--interactive', '-i', is_flag=True)
def inter(interactive):
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
