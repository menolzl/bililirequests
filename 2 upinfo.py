import requests
import pandas as pd

headers = {"Cookie":"","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"}

# proxy = '...:'
# proxies = {'http':'http://'+proxy,'https':'https://'+proxy,}

def get_url():
    data = pd.read_excel('b站原创top.xlsx', sheet_name='全区')
    uid = list(data['up主ID'])
    return uid

def get_page(uid):
    response1 = requests.get('https://api.bilibili.com/x/space/acc/info?mid=' + str(uid) + '&jsonp=jsonp',proxies=proxies,headers=headers)
    response2 = requests.get('https://api.bilibili.com/x/relation/stat?vmid=' + str(uid) + '&jsonp=jsonp',proxies=proxies,headers=headers)
    if response1 ==200:
        return response1.json() , response2.json()
    else:
        return 0



def parse_page(response1,response2):
    dict = {}
    dict['用户ID'] = response1.get('data').get('mid')
    dict['名称'] = response1.get('data').get('name')
    dict['级别'] = response1.get('data').get('level')
    dict['成就'] = response1.get('data').get('official').get('title')
    dict['签名'] = response1.get('data').get('sign')
    dict['粉丝数'] = response2.get('data').get('follower')
    return dict


if __name__ == '__main__':
    urls = get_url()
    list = []
    for url in urls:
        json = get_page(url)
        if json == 0:
            print(f'{url}抓取失败')
            continue
        else:
            dict = parse_page(*json)
            list.append(dict)
            print(f'{url} 已完成')
    data = pd.DataFrame(list)
    data.to_csv('top100up主.csv', encoding='utf_8_sig', index=False)
    print('--全部完成--')




