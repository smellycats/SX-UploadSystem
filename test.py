# -*- coding: utf-8 -*-
from iniconf import PlateIni
from upload import Users, Upload

def get_plate():
    p = PlateIni()
    s = p.get_plate('test.ini')
    print s
    del p

def create_table():
    #Users.create_table(True)
    Uploads.create_table(True)

def add_data():
    u = Upload.insert(timestamp=1433952012, uploadflag=False,
                      path=u'ImageFile\20150611\00\交警支队卡口\进城\0000126200200000000',
                      plateinfo='{"specialpiclocalpath": "ImageFile\\20150611\\00\\\u4ea4\u8b66\u652f\u961f\u5361\u53e3\\\u8fdb\u57ce\\0000126200200000000", "platecolor": "\u84dd\u724c", "roadname": "\u4ea4\u8b66\u652f\u961f\u5361\u53e3", "speedd": "60", "platecode": "\u7ca4LQZ388", "channelid": "2", "filename": "ImageFile\\20150611\\00\\\u4ea4\u8b66\u652f\u961f\u5361\u53e3\\\u8fdb\u57ce\\0000126200200000000", "datetime": "2015-06-11 00:00:12", "passdatetime": "2015-06-11 00:00:12", "flag": "1", "carspeed": "50", "deviceid": "", "directionid": "1", "cameraip": "192.168.188.55", "channelname": "2", "speed": "50", "roadid": "", "triggermode": "196", "speedx": "80"}')
    u.execute()

def get_test():
    u = Upload.select().order_by(Upload.id.desc()).limit(10)
    for i in u:
        print i

def get_test2():
    u = Upload.select().where(Upload.uploadflag == False).limit(5)
    print u
    for i in u:
        print i.path

def get_test3():
    u = Upload.select().order_by(Upload.uploadflag,Upload.timestamp).limit(10)
    print u
    for i in u:
        print i

def update_test():
    query = Upload.update(uploadflag=True).where(Upload.id == 100115)
    query.execute()

if __name__ == "__main__":
    get_plate()
    #create_table()
    #for i in range(90000):
        #add_data()
    #print 'done'
    #get_test3()
    #update_test()
    #get_test2()



