import requests
import pandas as pd
import json
import re
import datetime

headers = {"Cookie":"","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"}

# 制作一个生成器，遍历需要抓取的日期
def get_date():
    a = datetime.date(2022, 3, 8)
    b = datetime.date(2022, 3, 10)
    for i in range((b - a).days + 1):
        day = a + datetime.timedelta(days=i)
        yield day
        
        
# 获取需要抓取的视频的BVID
def get_bvid():
    data = pd.read_excel('b站原创top.xlsx',sheet_name='弹幕需求目录')
    bvid = list(data['BVID'])
    return bvid


# 以BVID请求并获取对应的oid
def get_oid(bvid):
    try:
        response = requests.get('https://api.bilibili.com/x/player/pagelist?bvid='+str(bvid)+'&jsonp=jsonp',headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)['data'][0]['cid']
    except requests.ConnectionError as e:
        print('Error', e.args)


# 请求弹幕数据
def get_page(oid,dt):
    url = 'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid=' + str(oid) + '&date=' + str(dt)

    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError as e:
        print('Error', e.args)

        
# 将抓取结果按列拆分得到结果列表，正则每个元素的中文部分。
def parse_page(response,bv):

    list = ['bvid,弹幕']       # 以此为csv第一行标题
    result = response.split('\n')
    for i in result:
        pattern = re.compile('([\u4e00-\u9fa5]+)')
        data = re.findall(pattern,i)
        if data:
            list.append(f'{bv},{data[0]}')
    return list


# 标题为第一次写入，如果标题已有写入则说明文件已创建，判断i是否为标题内容，有则跳过以防重复写入。
def save_data(data):
    path = '弹幕/b站弹幕.csv'
    if os.path.exists(path):
        with open(path, 'a',encoding="utf_8_sig") as f:
            for i in data:
                if i != 'bvid,弹幕':
                    f.write(i + '\n')
                else:
                    continue
    else:
        with open(path, 'a',encoding="utf_8_sig") as f:
            for i in data:
                f.write(i + '\n')



# 先获取oid，拿到oid后，按照需要的日期循环请求获取弹幕并装入list中，所有请求完成后将list存入csv文件。
if __name__ == '__main__':
    bvid = get_bvid()
    for bv in bvid:
        oid =  get_oid(bv)
        date = get_date()
        for dt in date:
            response =  get_page(oid,dt)
            list = parse_page(response,bv)
            if list:
                save_data(list)
            else:
                print('No data in here!')
        print(f'{bv}已完成导入！')






