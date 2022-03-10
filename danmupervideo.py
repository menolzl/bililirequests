import requests
import pandas as pd
import json
import re
import datetime

headers = {"Cookie":"buvid3=472C2412-7550-D2CF-70F4-A1DD208F295B66351infoc; i-wanna-go-back=-1; _uuid=986D515D-6176-79A4-28C8-F5105732F8C91065827infoc; buvid4=18C58428-3E9A-3118-941E-33F16F6E873A67496-022030823-9E/zTJJxAKuUmUVtWG83gQ%3D%3D; buvid_fp_plain=undefined; LIVE_BUVID=AUTO1816467533827294; blackside_state=1; rpdid=|(um|k~|J~kR0J'uYRY~lR|)k; CURRENT_QUALITY=0; CURRENT_BLACKGAP=0; PVID=1; fingerprint=6a1fdf384fa4103e094963ef3933bdb1; CURRENT_FNVAL=4048; b_lsid=DF25A12B_17F7265F6AB; b_ut=5; innersign=1; bsource=search_baidu; bp_video_offset_1379528=635831292200484900; buvid_fp=472C2412-7550-D2CF-70F4-A1DD208F295B66351infoc; SESSDATA=7afcfc58%2C1662446427%2C50c6f%2A31; bili_jct=09e38be67a3a9b0e69993dec4c979e12; DedeUserID=1379528; DedeUserID__ckMd5=e69363711611e319; sid=749yciex","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"}


def get_date():
    a = datetime.date(2022, 3, 8)
    b = datetime.date(2022, 3, 10)
    for i in range((b - a).days + 1):
        day = a + datetime.timedelta(days=i)
        yield day

def get_bvid():
    data = pd.read_excel('D://桌面/b站原创top.xlsx',sheet_name='弹幕需求目录')
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


def save_data(data,bvid):
    with open(f'D:/桌面/弹幕/{bvid}.txt', 'a',encoding="utf_8_sig") as f:
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
            save_data(list,bv)
        print(f'{bv}已完成！')






