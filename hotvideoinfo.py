import requests
from lxml import etree
import re
import pandas as pd

base_url = 'https://www.bilibili.com/v/popular/rank/'

headers = {'Cookie':'innersign=0; buvid3=472C2412-7550-D2CF-70F4-A1DD208F295B66351infoc; i-wanna-go-back=-1; b_lsid=8C5CBB4B_17F6A263F35; _uuid=986D515D-6176-79A4-28C8-F5105732F8C91065827infoc; buvid4=18C58428-3E9A-3118-941E-33F16F6E873A67496-022030823-9E/zTJJxAKuUmUVtWG83gQ%3D%3D; fingerprint=dfac9c33c01ee95d803470847cb6af0d; buvid_fp_plain=undefined; buvid_fp=6a1fdf384fa4103e094963ef3933bdb1; SESSDATA=800d70de%2C1662305379%2C01502%2A31; bili_jct=a0450f50fe222d23a1a016452f04e5f9; DedeUserID=1379528; DedeUserID__ckMd5=e69363711611e319; sid=i7mi2e85; b_ut=5; LIVE_BUVID=AUTO1816467533827294; CURRENT_BLACKGAP=0; CURRENT_FNVAL=80','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}

dict = {'全区':'all','国创相关':'guochuang','动画':'douga','音乐':'music','舞蹈':'dance','游戏':'game','知识':'knowledge','科技':'tech','运动':'sports','汽车':'car','生活':'life','美食':'food','动物圈':'animal','鬼畜':'kichiku','时尚':'fashion','娱乐':'ent','影视':'cinephile','原创':'origin','新人':'rookie'}
# dict = {'全区':'all'}
pd.options.display.max_columns= 999

def get_page(page):
    url = base_url+page

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
    except requests.ConnectionError as e:
        print('Error', e.args)

def parse_page(response,area):

    html = etree.HTML(response.text)
    result = []
    rank = html.xpath('//div/div[1]/i/span/text()')
    title = html.xpath('//div[@class="info"]/a/text()')
    uppers = html.xpath('//div/div[2]/div/a/span/text()')
    brocast = html.xpath('//div/div[2]/div/div/span[1]/text()')
    comment = html.xpath('//div/div[2]/div/div/span[2]/text()')
    link = html.xpath('//div[@class="info"]/a/@href')
    upurl = html.xpath('//div/div[2]/div/a/@href')
    for p,x,u,y,z,k,o in zip(rank,title,uppers,brocast,comment,link,upurl):
        u = re.sub('\n', '', str(u))
        y = re.sub('\n','',str(y))
        z = re.sub('\n', '', str(z))
        k = re.sub('//','',str(k))
        o = re.sub('//','',str(o))
        dict = {'分区':area,'排名':p,'标题':x,'up主':u.strip(),'播放量':y.strip(),'弹幕数':z.strip(),'链接':k,'up主地址':o}
        result.append(dict)
    return result

if __name__ == '__main__':

    data = pd.DataFrame()
    for k,v in dict.items():
        response = get_page(v)
        htmls = parse_page(response,k)
        df = pd.DataFrame(htmls)
        data = pd.concat([data,df])
        print(f'{k}分区已完成！')
    data.to_csv('D://桌面/b站原创top.csv',encoding='utf_8_sig',index=False)

