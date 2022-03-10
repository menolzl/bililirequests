import requests
import pandas as pd
import json
import re
import datetime

headers = {"Cookie":"","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"}


def get_date():
    a = datetime.date(2022, 3, 8)
    b = datetime.date(2022, 3, 10)
    for i in range((b - a).days + 1):
        day = a + datetime.timedelta(days=i)
        yield day

def get_bvid():
    data = pd.read_excel('b站原创top.xlsx',sheet_name='弹幕需求目录')
    bvid = list(data['BVID'])
    return bvid


def get_oid(bvid):

    try:
        response = requests.get('https://api.bilibili.com/x/player/pagelist?bvid='+str(bvid)+'&jsonp=jsonp',headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)['data'][0]['cid']
    except requests.ConnectionError as e:
        print('Error', e.args)


def get_page(oid,dt):
    url = 'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid=' + str(oid) + '&date=' + str(dt)

    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_page(response):
    list = []
    result = response.split('\n')
    for i in result:
        pattern = re.compile('([\u4e00-\u9fa5]+)')
        data = re.findall(pattern,i)
        if data:
            list.append(data[0])
    return list


def save_data(data):
    with open(f'弹幕/b站top20弹幕1.txt', 'a',encoding="utf_8_sig") as f:
        for i in data:
            f.write(i+'\n')



if __name__ == '__main__':
    bvid = get_bvid()
    for bv in bvid:
        oid =  get_oid(bv)
        date = get_date()
        for dt in date:
            response =  get_page(oid,dt)
            list = parse_page(response)
            if list:
                save_data(list)
            else:
                print('No data in here!')
        print(f'{bv}已完成导入！')






