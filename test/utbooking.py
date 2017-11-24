import unittest
import sys
import os
pkg_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if pkg_path not in sys.path:
    sys.path.append(pkg_path)
from twmovieapi import mm, User


class TestBook(unittest.TestCase):
    def setUp(self):
        self.user = User(os.path.abspath('test/config.json'))

    def test_user(self):
        self.assertTrue(self.user.mail)
        self.assertTrue(self.user.passwd)

    def test_login(self):
        book = mm.Book(self.user)
        r = book.login()
        r = r.content.decode()
        self.assertNotEqual(r.find('會員資訊'), -1)

    def test_set_screening(self):
        book = mm.Book(self.user)
        book.login()

        info = mm.MovieInfo()
        for item in info.get('MM'):
            sid = item['id']
            break

        cid = info.getcid('MM')
        book.set_screenings(cid, sid)

    def test_set_ticket(self):
        book = mm.Book(self.user)
        book.login()

        info = mm.MovieInfo()
        for item in info.get('MM'):
            sid = item['id']
            break

        cid = info.getcid('MM')
        book.set_screenings(cid, sid)

        response = book.set_ticket(discounted=2)

    def test_get_seat(self):
        book = mm.Book(self.user)
        book.login()

        info = mm.MovieInfo()
        for item in info.get('MM'):
            sid = item['id']
            break

        cid = info.getcid('MM')
        book.set_screenings(cid, sid)

        response = book.set_ticket(discounted=2)
        # parse seat info
        seatdict = mm.seat.get_seat(response)

        # print seats layout
        mm.seat.print_seating_chart(mm.seat.gen_layout(seatdict))

    def test_book_comfirm(self):
        book = mm.Book(self.user)
        book.login()

        info = mm.MovieInfo()
        for item in info.get('MM'):
            sid = item['id']
            break

        cid = info.getcid('MM')
        book.set_screenings(cid, sid)

        response = book.set_ticket(discounted=2)
        seatdict = mm.seat.get_seat(response)
        # set seat
        response = book.set_seat([seatdict['B12'][0],
                                  seatdict['B11'][0]])
        self.assertNotEqual(response.content.decode().find('我已經閱讀並同意'),
                            -1)
        # book.confirm()

    # def test_movie_info(self):
    #     info = mm.MovieInfo()
    #     for m in info.get('MM'):
    #         self.assertNotEqual(m['name'], '')
    #         self.assertTrue(m['id'].isdigit())


if __name__ == '__main__':
    unittest.main()
