import functools
import math
import operator
import os

import requests

from PIL import Image, ImageChops, ImageStat


def getimg(filename, session=None):
    '''
    session: requests's session

    '''
    if session:
        response = session.get(filename, stream=True)
        response.raw.decode_content = True
        img = Image.open(response.raw).convert('LA')
        return img
    else:
        return Image.open(filename).convert('LA')


def get_digit():
    mypath = os.path.join(os.path.dirname(__file__), 'digit')
    img_list = []
    files = [f for f in os.listdir(
        mypath) if os.path.isfile(os.path.join(mypath, f))]
    for f in files:
        filename = os.path.join(mypath, f)
        img_list.append(getimg(filename))
    return img_list


def compare(img1, img2):
    h = ImageChops.difference(img1, img2).histogram()

    sq = (value * ((idx % 256)**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares / float(img2.size[0] * img2.size[1]))
    return rms


def argmin(img, candidate):
    result = []
    for c in candidate:
        result.append(compare(img, c))
    return result.index(min(result)) + 1


if __name__ == '__main__':
    s = requests.Session()
    s.get('https://www.miramarcinemas.com.tw/member_login.aspx')

    urls = ['https://www.miramarcinemas.com.tw/draw.ashx?r_id=num%d&t=636468952047677500' %
            (i) for i in range(1, 5)]
    img = getimg(urls[0], s)
    img.save('QQ.png')
    print(argmin(img, get_digit()))
