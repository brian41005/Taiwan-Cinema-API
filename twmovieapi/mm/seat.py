from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


class Color:
    RESET = '\033[0m'
    F_BLACK = '\033[30m'
    B_GREEN = '\033[42m'
    B_RED = '\033[41m'
    B_BLACK = '\033[40m'


def get_seat(r):
    soup = BeautifulSoup(r.content.decode(), 'lxml')
    soup = soup.find('div', attrs={'id': 'seatLabel',
                                   'class': 'seat-selection'}).table
    seatdict = {}
    for s in soup.find_all('td'):
        try:
            key = s.div.string
            seatdict[key] = [s.input['value'],
                             s.div['class'][0] == 'seat-normal']
        except TypeError:
            pass
    return seatdict


def gen_layout(seatdict):
    row = sorted([int(v[0].split('|')[-2])
                  for k, v in seatdict.items()])[-1] + 1
    col = sorted([int(v[0].split('|')[-1])
                  for k, v in seatdict.items()])[-1] + 1
    array = [[None for c in range(col)] for r in range(row)]
    for k, v in seatdict.items():
        seatNo, state = v
        rr, rc = seatNo.split('|')[-2:]
        rr, rc = int(rr), int(rc)

        array[row - rr - 1][col - rc - 1] = [k, state]
    return array


def print_seating_chart(seatingChart):
    print(Color.F_BLACK, end='')
    for r in seatingChart:
        for c in r:
            if c is None:
                print(Color.B_BLACK + '%3s' % (''), end=' ')
            else:
                back = Color.B_GREEN if c[1] else Color.B_RED
                print(back + '%3s' % (c[0]), end=' ')
        print(Color.B_BLACK)
    print(Color.RESET)


def match(seatdict, your_preference):
    pass
