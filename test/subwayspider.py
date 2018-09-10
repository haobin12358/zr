# -*- coding: utf-8 -*-
import json
import re
import time
import uuid

import requests
from sqlalchemy.orm import scoped_session, sessionmaker
from Linjia.commons import base_model as model
from Linjia.models import City, SubwayLine, SubwayPosition
session = scoped_session(sessionmaker(autocommit=False, autoflush=False,  bind=model.mysql_engine))


with open('Linjia/configs/subway_city_code.json', 'r') as rf:
    content = json.load(rf)
    print(content)
    subways_city = content.get('subways_city').get('cities')
    for city in subways_city:
        code = city.get('code')
        cename = city.get('cename')
        name = city.get('cn_name')
        chinacity = session.query(City).filter(City.name==name).first()
        if chinacity:
            print(u'current city is {}'.format(name))
            url = 'https://map.baidu.com/?qt=subways&c={}&format=json'.format(code)
            respjson = requests.get(url).json()
            subways = respjson.get('subways').get('l')
            line_list = []
            for subway in subways:
                postions = subway.get('p')
                lines = subway.get('l_xmlattr')
                line_name = lines.get('lb')
                subwayline = SubwayLine()
                s_id = str(uuid.uuid4())
                subwayline.subwaylineid = s_id
                subwayline.city_id = chinacity.city_id
                subwayline.linename = line_name
                session.add(subwayline)
                session.commit()
                for potion in postions:
                    potion = potion.get('p_xmlattr')
                    positionnane = potion.get('sid')
                    line_name = potion.get('ln')
                    subwayposionmodel = SubwayPosition()
                    subwayposionmodel.subwayposionid = str(uuid.uuid4())
                    subwayposionmodel.subwaylineid = s_id
                    subwayposionmodel.position = positionnane
                    session.add(subwayposionmodel)
                    session.commit()

            time.sleep(3)




"""
url = 'https://map.baidu.com/?qt=subways&c=179&format=json&t=1536588015866&callback=jsonp67097049'
resp = requests.get(url)
resp_resource = str(resp.text)
print(resp_resource)
resp_dict = re.findall(r'json.*?\((.*?)\)', resp_resource, re.S)[0]
resp_json = json.loads(resp_dict)
result = resp_json.get('result')
if result.get('error') != 0:
    print('an error occured')
subways = resp_json.get('subways').get('l')
for subway in subways:


"""
