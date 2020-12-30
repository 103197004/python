# -*- coding: UTF-8 -*-
import requests
import json
import sys
import importlib
importlib.reload(sys)
#sys.setdefaultencoding('utf8')
import csv
import time
import random

fileName = "output.csv"
web_key = 'KpEnREo2aOshRY5MEPILuzyYLlIGIyWQ'
poi_url = "http://api.map.baidu.com/place/v2/search?query="
aoi_url = "https://ditu.amap.com/detail/get/detail"
city_name = "香港"
# classes = ['酒店','购物','生活服务','丽人','旅游景点','休闲娱乐','运动健身','教育培训','文化传媒','医疗','交通设施','金融','房地产','公司企业','政府机构','行政地标']
classes = ['酒店']

#根据城市名称和分类关键字获取poi数据
def getpois(keywords,wr):
    i = 0
    poilist = []
    while True : #使用while循环不断分页获取数据
       result = getpoi_page(keywords, i)
       # 将字符串转换为json
       data = result['results']
       if len(data) == 0:
           break
       handle(data,wr)
       poilist.extend(data)
       i = i + 1
       if i > 2:
         break
       time.sleep(random.randint(3,5)) 
    return poilist
    
#单页获取pois
def getpoi_page(keywords, page):
    req_url = poi_url + keywords + "&tag=" + keywords + "&region=" +city_name + "&city_limit=true&scope=2&coord_type=1&page_size=20&page_num=" + str(page) + "&output=json&ak="+ web_key
    data = ''
    with requests.get(req_url) as f:
      data = f.json()
      # data = data.decode('utf-8')
    return data
def handle(data,wr):
    for da in data:
         str1 = ''
         str1 += da['name'] +','
         arr = da['location']
         lat = arr['lat']
         lng = arr['lng']
         str1+=str(lat)+','
         str1+=str(lng)+','
         str1+= da['address'] +','
         str1+= da['area'] +','
         str1+= da['uid'] +','
         detail_info = da['detail_info']
         str1+= detail_info['type']
         str1+= '\n'
         wr.writer(str1)

if __name__ == '__main__':
  f = open(fileName,'a',encoding='utf-8')
  head = ['name','lat','lng','address','area','uid','type']
  ww = csv.DictWriter(f,head)
  ww.writeheader()
  for cls in classes:
    poilist = getpois(cls,ww)
    f.close()
