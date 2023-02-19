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

# t = top, b = bottom, l = left, r = right
Border = namedtuple('Border', ['horz', 'vert', 'tl', 'tr', 'bl', 'br'])


def center_and_wrap(text: str, length: int) -> str:
    # global width
    # global edge
    space = width//2 - length//2
    bonus = width%2 - length%2
    return f'{edge}{" "*space}{text}{" "*(space+bonus)}{edge}\n'


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

    B = Border(*args('frame'))
    C = Color(*[f'\033[{code}m' for code in colors.values()])

    edge = f'{C.border}{B.vert}{C.reset}'
    top = f'{C.border}{B.tl}{B.horz*width}{B.tr}\n'
    sep = f'{C.border}{B.vert}{" "*width}{B.vert}\n'
    bottom = f'{C.border}{B.bl}{B.horz*width}{B.br}{C.reset}\n'

    _name = args('name')
    head = center_and_wrap(C.name+_name, len(_name))

    body = []
    for item in data.keys():

        body.append(sep)
        if item != '':
            body.append(center_and_wrap(C.title+item, len(item)))

        # loop over nested dict
        for key, val in data[item].items():
            _escaped = val.replace('link:', '', 1)
            _style = C.under * (_escaped != val)
            _segment = f'{C.key}{key}: {C.value}{_style}{_escaped}{C.reset}'
            _length = len(key+_escaped)+2
            body.append(center_and_wrap(_segment, _length))

    card = f'{top}{sep}{head}{"".join(body)}{sep}{bottom}'

    print(card, end='')
