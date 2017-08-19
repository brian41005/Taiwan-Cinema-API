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
        self.s = requests.Session()
        self.url = 'https://www.miramarcinemas.com.tw/booking.aspx'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
        r = self.s.get(self.url)
        self.soup = BeautifulSoup(r.content.decode(), 'lxml')
        self.payload = {'__EVENTTARGET': 'ctl00$content$CinemaList',
                        '__EVENTARGUMENT': '',
                        '__LASTFOCUS': ''}

        self._update_event_valid()
        self.cinemaList = filterby(self.soup, 'ctl00$content$CinemaList')

    def _update_event_valid(self):
        EVENTVALIDATION = self.soup.find(
            'input', attrs={'name': '__EVENTVALIDATION'})['value']
        VIEWSTATE = self.soup.find(
            'input', attrs={'name': '__VIEWSTATE'})['value']
        VIEWSTATEGENERATOR = self.soup.find(
            'input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
        self.payload['__EVENTVALIDATION'] = EVENTVALIDATION
        self.payload['__VIEWSTATE'] = VIEWSTATE
        self.payload['__VIEWSTATEGENERATOR'] = VIEWSTATEGENERATOR

    def select(self, f, payload):
        self.payload.update(payload)
        r = self.s.post(self.url, data=self.payload)
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
                for t in timeList:
                    name, _, left = t['name'].replace('\t', ' ').split()
                    t['name'] = name
                    t['left'] = left
                    yield m, d, t
