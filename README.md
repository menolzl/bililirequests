# bilibli视频排行榜数据爬虫 

该项目基于python对bilibli的热门排行top100视频的信息进行抓取，并以此为基础抓取top100up主信息及弹幕信息。

**代码主要分三个：**
 *  **1 hotvideoinfo.py** 用于抓取b站热门视频榜的一些信息
 *  **2 upinfo.py** 以 1 hotvideoinfo.py 为基础抓取up主的基本信息
 *  **3 danmu.py** 以 1 hotvideoinfo.py 为基础抓取视频弹幕
 
***ps**:代码无法直接使用，需要补充cookie，另2 upinfo.py还需补充代理。*

***本代码仅供学习使用。***

另附基于此代码获取的数据制作的数据浅析报告，基于powerbi:
[数据分析报告]:https://app.powerbi.com/view?r=eyJrIjoiNWRlOTdhOWUtMTA2OC00MzhhLTg1YzQtMGY2YmRkNWU2M2JiIiwidCI6IjUxZDU0NDY4LWE1ZTAtNDhjMi05MTE2LTJiYjFiOWQ2YTVkOSIsImMiOjN9
