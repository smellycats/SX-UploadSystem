import os
import glob
import json
import Queue
import threading

import arrow

from iniconf import PlateIni, MyIni
from app import app, db
from models import Upload


class Uploader(threading.Thread):
    def __init__(self,t_name):
        threading.Thread.__init__(self)

        self.ini = PlateIni()
        self.is_quit = False
        self.t_name = t_name

    def __del__(self):
        print '%s quit', t_name
        del self.ini

    def run(self):
        while 1:
            try:
                item = app.config['CREATEDQUE'].get(timeout=1)
                p = self.ini.get_plate(item['path'])
                if item['fresh']:
                    #t = time.mktime(time.strptime(p['datetime'], '%Y-%m-%d %H:%M:%S'))
                    t = arrow.get(p['datetime']).replace(hours=8)
                    query = Upload.insert(timestamp=t.timestamp,
                                          uploadflag=True,
                                          path=item['path'],
                                          plateinfo=json.dumps(p))
                    query.execute()
                else:
                    query = Upload.update(uploadflag=True).where(Upload.id == item['id'])
                    query.execute()
                print arrow.now(), self.t_name, item['path']
                time.sleep(1)
            except Queue.Empty:
                pass
            except Exception as e:
                print e
                time.sleep(1)
            finally:
                if self.is_quit:
                    break


class Digger(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.is_quit = False

    def __del__(self):
        pass

    def run(self):
        while 1:
            if self.is_quit:
                break
            if app.config['CREATEDQUE'].empty():
                query = Upload.select().where(Upload.uploadflag == False).limit(5)
                for i in query:
                    app.config['CREATEDQUE'].put({'fresh': False,'path': i.path,
                                                  'id': i.id})
            time.sleep(1)


class History(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.mini = MyIni()
        self.pini = PlateIni()
        self.timeflag = arrow.get(self.mini.get_sys()['timeflag']).replace(hours=-1)
        self.now = arrow.now('PRC')
        self.is_quit = False
        print 'History'

    def __del__(self):
        print 'history quit'
        del self.mini
        del self.pini

    def run(self):
        while 1:
            if self.is_quit:
                break
            if self.timeflag <= self.now.replace(hours=1):
                print self.timeflag
                h_files = self.get_files_from_db(self.timeflag)
                n_files = self.get_files_by_datetime(self.timeflag)
                c = set(n_files) - set(h_files)
                if c != set([]):
                    self.insert_db(c)
                self.timeflag = self.timeflag.replace(hours=1)
                if self.timeflag < self.now:
                    self.ini.set_sys(self.timeflag)
            else:
                break
            time.sleep(1)

    def insert_db(self, f):
        data_source = []
        for i in f:
            p = self.ini.get_plate(i)
            #t = time.mktime(time.strptime(p['datetime'], '%Y-%m-%d %H:%M:%S'))
            t = arrow.get(p['datetime']).replace(hours=8)
            info = {'timestamp': t.timestamp, 'uploadflag':False, 'path': i,
                    plateinfo=json.dumps(p)}
            data_source.append(info)
        with db.atomic():
            Upload.insert_many(data_source).execute()

    def get_files_from_db(self, t):
        f = Upload.select().where(Upload.timestamp >= t.timestamp,
                                  Upload.timestamp < t.replace(hours=+1).timestamp)
        r = []
        for i in f:
            r.append(i.path)
        return r

    def get_files_by_datetime(self, t):
        p = os.path.join(app.config['BASEPATH'], t.format('YYYYMMDD\HH'),
                         '*\*\*.ini')
        r = []
        for i in glob.glob(p):
            r.append(i[:-4].decode('gbk'))
        return r


if __name__ == "__main__":
    h = History()
    h.start()
    print 'end'
##    db.connect()
##    w = WatchFile(path='.')
##    for i in range(4):
##        t = Uploader(str(i))
##        t.setDaemon(True)
##        t.start()
##    #loop_histroy()
##    while 1:
##        try:
##            time.sleep(1)
##        except KeyboardInterrupt:
##            break
##    del w
##    db.close()




