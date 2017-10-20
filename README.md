# Taiwan Movie Booking API

[![pythonversion](https://img.shields.io/badge/python-3.4+-blue.svg)]()
[![license](https://img.shields.io/badge/license-BSD--3-blue.svg)]()

This package can get movie info and seats layout ,using your own account to book movie ticket.

But it's still under development, I just completed one of subpackage, mm(mirama).

`Note: This is a third party package, not official`


## Dependencies

* [requests](http://docs.python-requests.org/en/master/)
* [bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [lxml](http://lxml.de/)
```
pip install requests bs4 lxml
```
## Usage

### Config file
* In ./config.json

```json
{
    "mail": "1234@gmail.com",
    "passwd": "1234",
    "phone": "0970000000",
    "name": "GEEK Ma",
    "candidate":["I11","I12"]
}
```
* usage
```python
from twmovieapi import user

me = user.User()
print(me.mail)
print(me.phone)
print(me.name)
print(me.candidate)
```
output

```
brian41005@gmail.com
0970000000
bm
['I11', 'I12']
```
### Get screenings info
* Get info
```python
from twmovieapi import mm

# get mirama movie screenings info
info = mm.MovieInfo()

for m, d, t in info.get('MM'):
    print(m, d, t)
    break
```
output

```
{'name': '(中文版)CARS 3 閃電再起', 'id': '(CHI)CARS 3'} {'name': '8 月 20日 星期日', 'id': '20170820000000'} {'name': '09:25', 'id': '787544', 'left': '239'}
```

### Get seat
```python
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

```
Output

![seatLayout](img/seatLayout.PNG)

### Booking usage
```python
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
ticketdict = {'std': 0,
              'discount': 2,
              'heart': 0,
              'old': 0
              }
response = book.set_ticket(ticketdict)

# parse seat info
seatdict = mm.seat.get_seat(response)

# print seats layout
mm.seat.print_seating_chart(mm.seat.gen_layout(seatdict))

# set seat
response = book.set_seat([seatdict['B12'][0],
                          seatdict['B11'][0]])
```
then you can parse response
```python
# you will seat final confirm page
print(response.content.decode())
```

After setting seat, you will find some strings that are about final confirm, 
e.g. "我已經閱讀並同意" or something else.

Mostly, it will succeed, but in some cases:

* B9 B10 B11 B12 anyone of them has been booked

* your ticketdict {'std': 0,'discount': 2,'heart': 0,'old': 0} is different from your [seatdict['B12'][0], seatdict['B11'][0], seatdict['B9'][0],seatdict['B10'][0]]

It will got seats that you don't expect.

In my observation, their system will put default seats instead of your setting.

Finally
```python
# confirm
book.confirm()
```
## About this API