import sys
from collections import namedtuple

from arsparge import Parser


data = {
    'CONTACT': {
        'Email': 'user@domain.org',
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

Color = namedtuple('Color',
                   [*colors.keys(), 'reset', 'bold', 'under', 'reversed'],
                   defaults=('\033['+x+'m' for x in '0147'))
Border = namedtuple('Border', ['horz', 'vert', 'tl', 'tr', 'bl', 'br'])
Frame = namedtuple('Frame', ['top', 'bottom', 'sep', 'edge'])

def center_and_wrap(text: str, length: int, frame: namedtuple) -> str:
    space = width//2 - length//2
    bonus = width%2 - length%2
    return frame.edge + " "*space + text + " "*(space+bonus) + frame.edge

def get_frame(width: int, border: namedtuple, color: namedtuple) -> namedtuple:
    top = color.border + border.tl + border.horz*width + border.tr
    bottom = color.border + border.bl + border.horz*width + border.br + color.reset
    sep = color.border + border.vert + " "*width + border.vert
    edge = color.border + border.vert + color.reset
    return Frame(top, bottom, sep, edge)

def get_body(color: namedtuple, frame: namedtuple):
    body = list()
    for name, content in data.items():

        body.append(frame.sep)
        if name != '':
            body.append(center_and_wrap(color.title+name, len(name), frame))

        # loop over nested dict
        for key, val in content.items():
            _escaped = val.replace('link:', '', 1)
            _style = color.under if _escaped != val else ''
            _segment = color.key + key + ': ' + color.value + _style + _escaped + color.reset
            _length = len(key+_escaped)+2
            body.append(center_and_wrap(_segment, _length, frame))

    return body

def get_card(head: str, body: list, frame: namedtuple):
    segments = [frame.top, frame.sep, head] + body + [frame.sep, frame.bottom]
    return "\n".join(segments)


if __name__ == '__main__':

    options = [
        ['n', 'name', 'name=TEXT', 'set your nickname to TEXT', 'nickname'],
        ['w', 'width', 'width=NUMBER', 'set width of the card to NUMBER', '46'],
        ['f', 'frame', 'frame=TEXT', 'set chars of card\'s frame to TEXT', '-|╭╮╰╯'],
        ['', 'help', 'help', 'print this and exit', '']]

    args = Parser(argv=sys.argv,
                  options=options,
                  desc='Textual business card generator',
                  usage='[OPTIONS]')

    # Print help menu when --help used
    args('help') and exit(args.help())

    width = int(args('width')) - 2
    border = Border(*args('frame'))
    color = Color(*[f'\033[{code}m' for code in colors.values()])
    frame = get_frame(width, border, color)
    name = args('name')
    head = center_and_wrap(color.name+name, len(name), frame)
    body = get_body(color, frame)

    card = get_card(head, body, frame)
    print(card)

