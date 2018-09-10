# -*- coding: utf-8 -*-
import os
import time
import uuid

from sqlalchemy.orm import scoped_session, sessionmaker
from Linjia.commons import base_model as model
from Linjia.models import Icon

session = scoped_session(sessionmaker(autocommit=False, autoflush=False,  bind=model.mysql_engine))
base_dir = os.path.abspath(os.path.dirname(__file__))
file_name = os.path.join(base_dir, 'ico.txt')
img_dir = os.path.join(base_dir, 'ico')
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36'
}
page = 1

def get_icos(page):
    url = 'http://m.ziroom.com/v7/room/list.json?city_code=110000&page=%s&type=1' \
          '&price=&face=&rface=&hface=&feature=&around=&leasetype=&tag=&version=&area=&subway_code=&subway_station' \
          '_code=&district_code=&bizcircle_code=&clng=&clat=&suggestion_type=&suggestion_value=&keywords=&sort=' % page
    content = requests.get(url, headers=headers).json()
    rooms = content['data']['rooms']
    for room in rooms:
        id = room.get('id')
        time.sleep(2)
        roomurl = 'http://m.ziroom.com/v7/room/detail.json?city_code=110000&id=' + id
        print('start spider', roomurl)
        print(u'现在是第一页的数据')
        content = requests.get(roomurl, headers=headers).json()
        subdiarylist = content['data']['space']
        for subdiary in subdiarylist:
            icos = subdiary['config']
            for ico in icos:
                ico_url = ico['icon']
                if ico_url not in alreadsave:
                    alreadsave.append(ico_url)
                    img_content = requests.get(ico_url, headers=headers)
                    ima_name = ico_url.split('/')[-1]
                    with open(os.path.join(img_dir, ima_name), 'wb') as rf:
                        rf.write(img_content.content)
                    with open('ico.txt', 'a') as rf:
                        rf.write(str(ico))
                    print('已经写入', ima_name)
                    ico_model = Icon()
                    ico_model.iconid = str(uuid.uuid4())
                    ico_model.iconame = ico['name']
                    ico_model.iconurl = ico_url
                    session.add(ico_model)
                    session.commit()

if __name__ == '__main__':
    alreadsave = []
    for i in range(1, 20):
        get_icos(i)
        print('>>>>>>>>>>>>>>>>>>>>>>', len(alreadsave))
