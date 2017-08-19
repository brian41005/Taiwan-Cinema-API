import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from twmovieapi import user, mm

u = user.User('config.json')
book = mm.Book(u)

book.login()

info = mm.MovieInfo()
for m, d, t in info.get('MM'):
    print(m, d, t)
    sid = t['id']
    break
cid = info.getcid('MM')

book.set_screenings(cid, sid)
ticketdict = {'std': 0,
              'discount': 1,
              'heart': 0,
              'old': 0
              }
response = book.set_ticket(ticketdict)

# parse seat info
seatdict = mm.seat.get_seat(response)

# print layout
layout = mm.seat.gen_layout(seatdict)
mm.seat.print_seating_chart(layout)
