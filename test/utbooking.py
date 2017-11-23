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

    def test_book_login(self):
        book = mm.Book(self.user)
        r = book.login()
        r = r.content.decode()
        self.assertNotEqual(r.find('會員資訊'), -1)

    def test_movie_info(self):
        info = mm.MovieInfo()
        for m in info.get('MM'):
            self.assertNotEqual(m['name'], '')
            self.assertTrue(m['id'].isdigit())


if __name__ == '__main__':
    unittest.main()
