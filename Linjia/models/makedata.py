# -*- coding: utf-8 -*-
import random
import uuid

from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash

from Linjia.commons import base_model as model
from Linjia.commons.base_model import Base
INFO_COUNT = 20
all_icos = {
    'ico1': '热水机',
    'ico2': '双开门衣柜',
    'ico3': '担任沙发',
    'ico4': '空调',
    'ico5': '路由器',
    'ico6': '华莱士'
}
citynum = ['hbs-shi2jia1zhuang1', 'hbs-huang2hua2', 'xjwwezzq-chang1ji2', 'xjwwezzq-kun1yu4']

def create_table():
    Base.metadata.create_all(model.mysql_engine)


def drop_table():
    model.Base.metadata.drop_all(model.mysql_engine)


class Dbcreater(object):

    def __init__(self):
        self.session = scoped_session(sessionmaker(autocommit=False, autoflush=False,  bind=model.mysql_engine))
        self.roomid = self.generic_uuid(INFO_COUNT * 5)
        self.houseid = self.generic_uuid()
        self.villigeid = self.generic_uuid()
        self.sn = [str(x) for x in range(100)]
        self.roomfeatureid = self.generic_uuid(INFO_COUNT * 5)
        self.roompriceid = self.generic_uuid(INFO_COUNT * 15)
        self.userid = self.generic_uuid(INFO_COUNT)

    def generic_uuid(self, info_count=INFO_COUNT):
        return [str(uuid.uuid4()) for _ in range(info_count)]

    def create_user(self):
        from Linjia.models import User
        for id in self.userid:
            user = User()
            user.USid = id
            user.USnickname = 'usernickname'
            user.USgender = random.choice([1, 0])
            user.USstar = random.choice(['大熊做', '小熊做', '金羊做', '白卖座'])
            user.USpassword = generate_password_hash('pass')
            self.session.add(user)
            self.session.commit()

    def create_room(self):
        from Linjia.models import Room
        self.alread_sent = []
        self.hezu = []
        self.zhengzu = []
        for index, id in enumerate(self.roomid):
            room = Room()
            room.ROid = id
            room.HOid = random.choice(self.houseid)
            room.ROname = '这是房源的名字' + str(id)
            room.ROarea = random.randint(20, 150)
            room.ROimage = 'http://www.thisisimage/fjdl' + str(random.randint(222222, 333333)) + '.png'
            room.ROface = random.randint(0, 8)
            room.ROdistance = '距离' + str(random.randint(3, 10)) + '号线' + str(random.randint(2, 10)) + '米'
            room.ROface = random.randint(0, 8)
            room.ROdistance = '这是距离描述还不错' + id[5]
            room.ROshowpricetype = 1  # 季
            room.ROrenttype = random.randint(0, 3)
            room.ROsubwayaround = random.choice([True, False])
            if room.ROrenttype == 0:
                room.ROnum = random.randint(1, 4)
            room.ROpersoncount = random.randint(1, 5)
            room.ROintro = '这是房源的描述非常好' + id
            room.ROstatus = random.choice([0, 5])
            if room.ROstatus == 5:
                self.alread_sent.append(room.ROid)
            room.ROcitynum = random.choice(citynum)
            if room.ROrenttype == 0:
                self.hezu.append(id)
            if room.ROrenttype == 1:
                self.zhengzu.append(id)
            self.session.add(room)
            self.session.commit()


    def create_house(self):
        from  Linjia.models  import House
        for id in self.houseid:
            house = House()
            house.HOid = id
            house.HOtotalfloor = random.randint(1, 40)
            house.HOfloor = random.randint(1, house.HOtotalfloor)
            house.HObedroomcount = random.randint(1, 5)
            house.HOparlorcount = random.randint(1, 3)
            house.VIid = random.choice(self.villigeid)
            self.session.add(house)
            self.session.commit()

    def creat_villege(self):
        from  Linjia.models  import Villege
        for id in self.villigeid:
            villege = Villege()
            villege.VIid = id
            Villege.VIyears = str(random.randint(1994, 2017))
            villege.VItype = '风格不错' + id[5]
            villege.VIdesc = '小区的介绍, 这是, 超级好'
            villege.VIgreen = random.random()
            villege.VIviolumetric = random.random()
            villege.VIcarrate = random.random()
            villege.VIisclose = random.choice([True, False])
            villege.VIcarpay = random.randint(1, 30) + random.random()
            villege.VIcompany = '这是物业公司' + id[5]
            villege.VIphone = str(random.randint(10000000000, 19999999999))
            villege.VILatitude = random.uniform(0, 45)
            villege.VIlongitude = random.uniform(70, 120)
            villege.VIlocationnum = str(random.randint(1, 100))
            self.session.add(villege)
            self.session.commit()

    def create_roomfeature(self):
        from  Linjia.models  import RoomFeature
        for id in self.roomfeatureid:
            roomfeature = RoomFeature()
            roomfeature.RFid = id
            roomfeature.ROid = random.choice(self.roomid)
            boolean_fiels = ['RFbalcony', 'RFfirstrent', 'RFtwotoilet', 'RFcanpet', 'RFlock', 'RFelevator', 'RFtimeservice', 'RFwifi', ]
            for fiel in boolean_fiels:
                setattr(roomfeature, fiel, random.choice([True, False]))
            roomfeature.RFhytingtype = random.randint(0, 3)
            roomfeature.RFmonthclean = random.randint(0, 3)
            roomfeature.RFstyle = random.choice(['2.0', '1.0'])
            self.session.add(roomfeature)
            self.session.commit()

    def create_roomprice(self):
        from Linjia.models import RoomPayPrice
        for index, id in enumerate(self.roompriceid):
            price = RoomPayPrice()
            price.RPPid = id
            price.ROid = self.roomid[index/3]
            price.RPPperiod = index % 3
            price.RPPdeposit = random.randint(200, 2000)
            price.RPPservice = random.randint(200, 3000)
            price.RPPprice = random.randint(1000, 50000)
            self.session.add(price)
            self.session.commit()

    def create_signinfo(self):
        from Linjia.models import RoomSignInfo
        for id in self.roomid:
            roomsigninfo = RoomSignInfo()
            roomsigninfo.RSIid = id
            roomsigninfo.ROid = id
            roomsigninfo.RSIshortest = random.randint(30, 90)
            roomsigninfo.RSIlongest = random.randint(90, 180)
            roomsigninfo.PSIsigntype = random.randint(0, 1)
            self.session.add(roomsigninfo)
            self.session.commit()

    def create_subdiry_info(self):
        from Linjia.models import HouseSubsidiaryInfo
        choice = ['起居室', '卫生间', '厨房', '户型', '恩行']
        subid = self.roomfeatureid
        for index, id in enumerate(subid):
            housesub = HouseSubsidiaryInfo()
            housesub.HSIid = id
            housesub.HOid = random.choice(self.houseid)
            housesub.HSIarea = random.randint(20, 80)
            housesub.HSIname = choice[index % 5]
            housesub.RSIface = random.randint(1, 8)
            housesub.HSIimage = 'http://www.thisisimage/fjdl' + str(random.randint(222222, 333333)) + 'png'
            housesub.HRIsort = index % 5
            self.session.add(housesub)
            self.session.commit()

    def create_equirment(self):
        from Linjia.models import HouseSubsidiaryEquirment

        ids = self.roompriceid
        for index, id in enumerate(ids):
            equrment = HouseSubsidiaryEquirment()
            equrment.HSEid = id
            equrment.HSIid = self.roomfeatureid[int(index/3)]
            equrment.HSEsn = random.choice(all_icos.keys())
            equrment.HSEname = all_icos.get(equrment.HSEsn)
            equrment.HSEsort = random.randint(1, 10)
            self.session.add(equrment)
            self.session.commit()

    def create_roomequiment(self):
        from Linjia.models import RoomEquirment
        len_roomid = len(self.roomid)
        for index, id in enumerate(self.roompriceid):
            rq = RoomEquirment()
            rq.REid = id
            rq.REsn = random.choice(all_icos.keys())
            rq.ROid = self.roomid[index % len_roomid]
            rq.REsort = random.randint(1, 10)
            rq.REname = all_icos.get(rq.REsn)
            self.session.add(rq)
            self.session.commit()


    def create_user_room(self):
        from Linjia.models import UserRoom
        for id in self.alread_sent:
            userroom = UserRoom()
            userroom.URid = id
            userroom.USid = random.choice(self.userid)
            userroom.ROid = id
            userroom.URstarttime = '201700000'
            userroom.URendtime = '20180000'
            self.session.add(userroom)
            self.session.commit()




    def create_cit(self):
        from Linjia.models import City as CityModel
        import json
        json_file = 'Linjia/models/cities.txt'
        import pinyin
        with open(json_file, 'r') as rf:
            content = json.load(rf)
        print(content)
        provinces = content.get('provinces')
        for province in provinces:
            citys = province.get('citys')
            for city in citys:
                provinceName = province.get('provinceName')
                cityName = city.get('citysName')
                c = CityModel()
                c.Cityid = str(uuid.uuid4())
                c.Cityprovincenum = pinyin.get(provinceName, format="numerical")
                c.Citynum = str(pinyin.get_initial(pinyin.get_initial(provinceName)).replace(' ', '') + '-' +  str(pinyin.get(cityName[: -1], format="numerical")))
                c.Cityname = cityName
                c.Cityprovincename = provinceName
                self.session.add(c)
                self.session.commit()



if __name__ == '__main__':
    # drop_table()
    # create_table()
    creater = Dbcreater()
    # creater.create_user()
    # creater.create_room()
    # creater.creat_villege()
    # creater.create_house()
    # creater.create_roomfeature()
    # creater.create_roomprice()
    # creater.create_signinfo()
    # creater.create_subdiry_info()
    # creater.create_equirment()
    # creater.create_user_room()
    creater.create_cit()

 
