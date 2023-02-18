import sys
from collections import namedtuple

from arsparge import Parser


data = {
    'CONTACT': {
        'Email': 'user@domain',
        'Discord': 'user#0000',
    },
    '': {
        'Github': 'link:github.com/user',
    }
}


colors = {
    'border': '1;34',
    'name': '1;31',
    'title': '0;31',
    'key': '0;33',
    'value': '0;32',
}


# bro i need no colorama
_color_names = list(colors.keys()) + ['reset', 'bold', 'under', 'reversed']
_defaults = ['\033['+x+'m' for x in '0147']
Color = namedtuple('Color', _color_names, defaults = _defaults)

# horizontal, vertical, top left, top right, bottom left, bottom right
Frame = namedtuple('Frame', ['horz', 'vert', 'tl', 'tr', 'bl', 'br'])


def center(text: str, length: int = 0) -> str:
    # global width
    length = len(text) if length == 0 else length
    space = width//2 - length//2
    bonus = width%2 - length%2
    return '{}{}{}'.format(' '*space, text, ' '*(space+bonus))


def wrap(text: str):
    # global edge
    return '{1}{0}{1}\n'.format(text, edge)


if __name__ == '__main__':

    options = [
        ['n', 'name', 'name=TEXT', 'set your nickname to TEXT', 'nickname'],
        ['w', 'width', 'width=NUMBER', 'set width of the card to NUMBER', '46'],
        ['f', 'frame', 'frame=TEXT', 'set chars of card\'s frame to TEXT', '-|╭╮╰╯'],
        ['', 'help', 'help', 'print this and exit', ''] ]
    args = Parser(sys.argv, options, desc='Business card generator', usage='[OPTIONS]')

    # Print help menu when --help used
    args('help') and exit(args.help())

    width = int(args('width')) - 2

    F = Frame(*args('frame'))
    C = Color(*[f'\033[{code}m' for code in colors.values()])

    edge = f'{C.border}{F.vert}{C.reset}'
    top = f'{C.border}{F.tl}{F.horz*width}{F.tr}\n'
    sep = f'{C.border}{F.vert}{" "*width}{F.vert}\n'
    bottom = f'{C.border}{F.bl}{F.horz*width}{F.br}{C.reset}\n'

    _name = args('name')
    _text = center(C.name+_name, len(_name))
    head = wrap(_text)

    body = []
    for item in data.keys():

        body.append(sep)
        if item != '':
            _text = center(C.title+item, len(item))
            body.append(wrap(_text))

        # loop over nested dict
        for key, val in data[item].items():
            _escaped = val.replace('link:', '', 1)
            _style = C.under * (_escaped != val)
            _segment = f'{C.key}{key}: {C.value}{_style}{_escaped}{C.reset}'
            _length = len(key+_escaped)+2
            _text = center(_segment, _length)
            body.append(wrap(_text))

    card = f'{top}{sep}{head}{"".join(body)}{sep}{bottom}'

    print(card, end='')
