import click

def parser(query):
    if query[:2] == '!h':
        help()

def caller(query):
    pass

def help():
    help_text = """
        Available commands:
    !n <string> - Search on nyaa.si for anime.
    !t <string> - Search on ThePirateBay.
    !k <string> - Search on KickAssTorrents.
    !x <string> - Search on XBit.pw
    """
    print(help_text)

def nyaa():
    pass

def xbit():
    pass

def tpb():
    pass

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
    inter()