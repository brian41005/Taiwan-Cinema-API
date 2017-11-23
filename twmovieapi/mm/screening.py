import json
import os
import sys
import time
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup


def filterby(soup, name):
    temp = soup.find('select', attrs={'name': name}).find_all(
        value=lambda value: value != '')
    return [{'name': i.string, 'id': i['value']} for i in temp]


class MovieInfo(object):
    def __init__(self):
        self.cinemahash = {
            'MM': '1001|MM',
            'MMIMAX': '1001|MMIMAX',
            'TAI': '1004|TAI',
            'TRC': '1004|TRC',
            'TAIIMA': '1004|TAIIMA',
            'NH': '1005|NH'
        }
        self.session = requests.Session()
        self.url = 'https://www.miramarcinemas.com.tw/booking.aspx'
        # self.header = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
        self._init()
        self.is_executed = False
        # self.cinemaList = filterby(self.soup, 'ctl00$content$CinemaList')

    def _init(self):
        r = self.session.get(self.url)
        self.soup = BeautifulSoup(r.content.decode(), 'lxml')
        self.payload = {'__EVENTTARGET': 'ctl00$content$CinemaList',
                        '__EVENTARGUMENT': '',
                        '__LASTFOCUS': ''}

        self._update_event_valid()

    def _update_event_valid(self):
        event_valid = ['__EVENTVALIDATION',
                       '__VIEWSTATE',
                       '__VIEWSTATEGENERATOR']
        for each_tuple in event_valid:
            new_state = self.soup.find(
                'input', attrs={'name': each_tuple})['value']
            self.payload[each_tuple] = new_state

    def select(self, f, payload):
        self.payload.update(payload)
        r = self.session.post(self.url, data=self.payload)
        self.soup = BeautifulSoup(r.content.decode(), 'lxml')
        self._update_event_valid()
        return filterby(self.soup, f)

    def getcid(self, cinema):
        '''
        Return cid

        cinema: string
            'MM'      美麗華大直影城

            'MMIMAX'  IMAX影廳(大直)

            'TAI'     美麗華台茂影城

            'TRC'     Royal Club皇家廳(台茂)

            'TAIIMAX' IMAX影廳(台茂)

            'NH'      美麗華大直皇家影城

        '''
        return self.cinemahash[cinema].split('|')[0]

    def get(self, cinema):
        '''
        A generator

        cinema: string
            'MM'      美麗華大直影城

            'MMIMAX'  IMAX影廳(大直)

            'TAI'     美麗華台茂影城

            'TRC'     Royal Club皇家廳(台茂)

            'TAIIMAX' IMAX影廳(台茂)

            'NH'      美麗華大直皇家影城

        '''
        if self.is_executed:
            self._init()

        self.is_executed = True
        cid = self.cinemahash[cinema]
        payload = {'ctl00$content$CinemaList': cid,
                   'ctl00$content$MovieList': ''}
        movieList = self.select('ctl00$content$MovieList', payload)
        for m in movieList:
            payload = {'ctl00$content$CinemaList': cid,
                       'ctl00$content$MovieList': m['id']}
            dateList = self.select('ctl00$content$DateList', payload)
            for d in dateList:
                payload = {'ctl00$content$CinemaList': cid,
                           'ctl00$content$MovieList': m['id'],
                           'ctl00$content$DateList': d['id']}
                timeList = self.select('ctl00$content$TimerList', payload)
                d['date'] = d.pop('name')

                for t in timeList:
                    name, _, left = t.pop('name').replace('\t', ' ').split()
                    t['time'] = name
                    t['left'] = left
                    # yield m, d, t
                    result = {}
                    for each in (m, d, t):
                        result.update(each)
                    yield result
