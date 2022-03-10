import requests
from lxml import etree
import re
import pandas as pd

base_url = 'https://www.bilibili.com/v/popular/rank/'

headers = {'Cookie':'','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}

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
    data.to_csv('b站原创top.csv',encoding='utf_8_sig',index=False)

