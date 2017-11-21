import lxml
import requests
from bs4 import BeautifulSoup
from . import ocr


class Book(object):
    def __init__(self, user):
        self.s = requests.Session()
        self.s.headers.update(
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.360',
             'Connection': 'keep-alive'
             })
        self.user = user
        self.r = None
        self.digits = ocr.get_digit()

    def login(self):
        url = 'https://www.miramarcinemas.com.tw/member_login.aspx'
        soup = BeautifulSoup(self.s.get(url).content.decode(), 'lxml')
        captcha_urls = ['https://www.miramarcinemas.com.tw/draw.ashx?r_id=num%d&t=636468952047677500' %
                        (i) for i in range(1, 5)]
        captcha = ''
        for captcha_url in captcha_urls:
            img = ocr.getimg(captcha_url, self.s)
            captcha += str(ocr.argmin(img, self.digits))

        VIEWSTATE = soup.find_all(
            'input', attrs={'name': '__VIEWSTATE'})[0]['value']
        VIEWSTATEGENERATOR = soup.find_all(
            'input', attrs={'name': '__VIEWSTATEGENERATOR'})[0]['value']
        EVENTVALIDATION = soup.find_all(
            'input', attrs={'name': '__EVENTVALIDATION'})[0]['value']

        data = {'__VIEWSTATE': VIEWSTATE,
                '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
                '__EVENTVALIDATION': EVENTVALIDATION,
                'ctl00$content$account': self.user.mail,
                'ctl00$content$password': self.user.passwd,
                'ctl00$content$txtValidate': captcha}
        self.r = self.s.post(
            'https://www.miramarcinemas.com.tw/member_login.aspx',
            data=data)
        # print(self.r.content.decode())
        return self.r

    def set_screenings(self, cid, sid):
        self.cid = str(cid)
        self.sid = str(sid)
        # passr = self.s.get('http://www.miramarcinemas.com.tw/booking_data.aspx',
        #                    params={'cid': cid, 'sid': sid, })

    def set_ticket(self, *, std=0, discounted=0, disabled=0, old=0):
        '''
        std: int

        discointed: int

        disabled: int

        old: int
        '''
        if sum([std, disabled, discounted, old]) == 0:
            raise ValueError('std, disabled, discounted, old should be set')
        url = 'http://www.miramarcinemas.com.tw/booking_seat.aspx'
        self.r = self.s.post(url,
                             data={'iptCine': self.cid,
                                   'iptSess': self.sid,
                                   'ticket_0001': str(std),
                                   'price_0001': '260',
                                   'name_0001': '全票',
                                   'ticket_0581': str(discounted),
                                   'price_0581': '260',
                                   'name_0581': '優待票',
                                   'ticket_0345': str(disabled),
                                   'price_0345': '155',
                                   'name_0345': '愛心票',
                                   'ticket_0015': '0',
                                   'price_0015': str(old),
                                   'name_0015': '敬老票'
                                   })
        return self.r

    def set_seat(self, seats):
        soup = BeautifulSoup(self.r.content.decode(), 'lxml')
        url = 'http://www.miramarcinemas.com.tw/booking_seat.aspx'
        r = self.s.post(url,
                        data={'__EVENTTARGET':        'ctl00$content$btnNext',
                              '__EVENTARGUMENT':      soup.find_all('input', attrs={'name': '__EVENTARGUMENT'})[0]['value'],
                              '__VIEWSTATE':          soup.find_all('input', attrs={'name': '__VIEWSTATE'})[0]['value'],
                              '__VIEWSTATEGENERATOR':   soup.find_all('input', attrs={'name': '__VIEWSTATEGENERATOR'})[0]['value'],
                              '__EVENTVALIDATION':       soup.find_all('input', attrs={'name': '__EVENTVALIDATION'})[0]['value'],
                              'ctl00$content$iptCinema': self.cid,
                              'ctl00$content$iptSession': self.sid,
                              'seatNo': seats})
        confirm_url = 'http://www.miramarcinemas.com.tw/booking_confirm.aspx'
        self.r = self.s.get(confirm_url)  # 少了這一個
        return self.r

    def confirm(self):
        soup = BeautifulSoup(self.r.content.decode(), 'lxml')
        data = {'__EVENTTARGET': 'ctl00$content$ctl01',
                '__EVENTARGUMENT':  '',
                '__VIEWSTATE': soup.find_all('input', attrs={'name': '__VIEWSTATE'})[0]['value'],
                '__VIEWSTATEGENERATOR': soup.find_all('input', attrs={'name': '__VIEWSTATEGENERATOR'})[0]['value'],
                '__EVENTVALIDATION': soup.find_all('input', attrs={'name': '__EVENTVALIDATION'})[0]['value'],
                'ctl00$content$userMail': self.user.mail,
                'ctl00$content$userName': self.user.name,
                'ctl00$content$userPhone': self.user.phone,
                'ctl00$content$wsessid': soup.find_all('input', attrs={'name': 'ctl00$content$wsessid'})[0]['value'],
                'ctl00$content$wcineid': soup.find_all('input', attrs={'name': 'ctl00$content$wcineid'})[0]['value'],
                'ctl00$content$iptTotal': soup.find_all('input', attrs={'name': 'ctl00$content$iptTotal'})[0]['value'],
                'ctl00$content$orderNo': '',
                }
        url = 'http://www.miramarcinemas.com.tw/booking_confirm.aspx'
        self.r = self.s.post(url, data=data)
        return self.r
