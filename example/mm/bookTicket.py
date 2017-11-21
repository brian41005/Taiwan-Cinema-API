import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from twmovieapi import mm, user

usr = user.User('config.json')
book = mm.Book(usr)

# login
book.login()

# select movie
info = mm.MovieInfo()
for m, d, t in info.get('MM'):
    print(m, d, t)
    sid = t['id']
    break
cid = info.getcid('MM')

# set cinema and movie
book.set_screenings(cid, sid)

# set ticket

response = book.set_ticket(discounted=2)

# parse seat info
seatdict = mm.seat.get_seat(response)

# print seats layout
mm.seat.print_seating_chart(mm.seat.gen_layout(seatdict))

# set seat
response = book.set_seat([seatdict['B12'][0],
                          seatdict['B11'][0]])

# you will seat final confirm page
print(response.content.decode())

# confirm
#
#  book.confirm()
