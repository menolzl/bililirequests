import requests
import pandas as pd

headers = {"Cookie":"buvid3=472C2412-7550-D2CF-70F4-A1DD208F295B66351infoc; i-wanna-go-back=-1; _uuid=986D515D-6176-79A4-28C8-F5105732F8C91065827infoc; buvid4=18C58428-3E9A-3118-941E-33F16F6E873A67496-022030823-9E/zTJJxAKuUmUVtWG83gQ%3D%3D; fingerprint=dfac9c33c01ee95d803470847cb6af0d; buvid_fp_plain=undefined; buvid_fp=6a1fdf384fa4103e094963ef3933bdb1; SESSDATA=800d70de%2C1662305379%2C01502%2A31; bili_jct=a0450f50fe222d23a1a016452f04e5f9; DedeUserID=1379528; DedeUserID__ckMd5=e69363711611e319; sid=i7mi2e85; b_ut=5; LIVE_BUVID=AUTO1816467533827294; blackside_state=1; rpdid=|(um|k~|J~kR0J'uYRY~lR|)k; CURRENT_QUALITY=0; CURRENT_BLACKGAP=0; PVID=6; innersign=1; bp_video_offset_1379528=635639736671666200; b_lsid=964A7CAD_17F6F2CB69E; CURRENT_FNVAL=80","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"}

def get_url():
    data = pd.read_excel('D://桌面/b站原创top.xlsx', sheet_name='全区')
    uid = list(data['up主ID'])
    return uid

def get_page(uid):
    response1 = requests.get('https://api.bilibili.com/x/space/acc/info?mid=' + str(uid) + '&jsonp=jsonp', headers=headers)
    response2 = requests.get('https://api.bilibili.com/x/relation/stat?vmid=' + str(uid) + '&jsonp=jsonp', headers=headers)
    return response1.json() , response2.json()



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
        dict = parse_page(*json)
        list.append(dict)
        print(f'{url} 已完成')
    data = pd.DataFrame(list)
    data.to_csv('D://桌面/top100up主.csv', encoding='utf_8_sig', index=False)
    print('--全部完成--')




