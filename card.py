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


if __name__ == '__main__':

    options = [
        ['n', 'name', 'name=TEXT', 'set your name or nickname to TEXT', 'nickname'],
        ['s', 'size', 'size=NUMBER', 'set width of the card to NUMBER of chars', '46'],
        ['f', 'frame', 'frame=TEXT', 'set chars of card\'s frame to TEXT', '-|╭╮╰╯'],
        ['', 'help', 'help', 'print this and exit', ''] ]
    args = Parser(sys.argv, options, desc='Business card generator', usage='[OPTIONS]')

    # Print help menu when --help used
    args('help') and exit(args.help())

    name = args('name')
    size = int(args('size')) - 2

    Frame = namedtuple('Frame', ['horz', 'vert', 'tl', 'tr', 'bl', 'br'])
    F = Frame(*args('frame'))

    _color_names = list(colors.keys()) + ['reset', 'bold', 'underline', 'reversed']
    _defaults = ['\033['+x+'m' for x in '0147']
    Color = namedtuple('Color', _color_names, defaults = _defaults)
    C = Color(*['\033['+x+'m' for x in colors.values()])

    OFFSET = { (1, 0): 1, (1, 1): 0, (0, 0): 0, (0, 1): -1 }

    edge = '{}{}{}'.format(C.border, F.vert, C.reset)
    top = '{}{}{}{}\n'.format(C.border, F.tl, F.horz*size, F.tr)
    sep = '{}{}{}{}\n'.format(C.border, F.vert, ' '*size, F.vert)
    bottom = '{}{}{}{}{}\n'.format(C.border, F.bl, F.horz*size, F.br, C.reset)

    body = []
    for item in data.keys():

        body.append(sep)
        if item:
            space = size//2-len(item)//2
            bonus = OFFSET[(size%2, len(item)%2)]
            line = '{}{}{}{}{}{}\n'.format(edge, ' '*space, C.title, item, ' '*(space+bonus), edge)
            body.append(line)

        # loop nested dict
        for key, val in data[item].items():
            vval = val
            val = val.replace('link:', '', 1)
            content_len = len(key+val)+2
            space = size//2-content_len//2
            bonus = OFFSET[(size%2, content_len%2)]
            if vval.startswith('link:'):
                val = '{}{}{}'.format(C.underline, val, C.reset)
            line = '{}{}{}{}: {}{}{}{}\n'.format(edge, ' '*space, C.key, key, C.value, val, ' '*(space+bonus), edge)
            body.append(line)

    space = size//2-len(name)//2
    bonus = OFFSET[(size%2, len(name)%2)]
    head = edge+' '*space+C.name+name+' '*(space+bonus)+edge+'\n'

    card = top + sep + head + ''.join(body) + sep + bottom

    print(card, end='')
