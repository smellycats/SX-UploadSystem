import Queue
import json
import time
import datetime
import threading

from iniconf import PlateIni
from watch_file import WatchFile
import gl
from upload import app, db, Upload


basepath = 'C:\SpreadData\ImageFile'


class Uploader(threading.Thread):
    def __init__(self,t_name):
        threading.Thread.__init__(self)
        self.que = gl.CREATEDQUE
        self.ini = PlateIni()
        self.is_quit = False
        self.t_name = t_name

    def __del__(self):
        print '%s quit', t_name
        del self.ini

    def run(self):
        while 1:
            try:
                item = gl.CREATEDQUE.get(timeout=1)
                p = self.ini.get_plate(item['path'])
                if item['fresh']:
                    t = time.mktime(time.strptime(p['datetime'], '%Y-%m-%d %H:%M:%S'))
                    query = Upload.insert(timestamp=int(t), uploadflag=True,
                                          path=item['path'],
                                          plateinfo=json.dumps(p))
                    query.execute()
                else:
                    query = Upload.update(uploadflag=True).where(Upload.id == item['id'])
                    query.execute()
                print datetime.datetime.now(), self.t_name, item['path']
                time.sleep(1)
            except Queue.Empty:
                pass
            except Exception as e:
                print e
                time.sleep(1)
            finally:
                if self.is_quit:
                    break

def loop_histroy():
    while 1:
        if gl.CREATEDQUE.empty():
            query = Upload.select().where(Upload.uploadflag == False).limit(5)
            for i in query:
                gl.CREATEDQUE.put({'fresh': False, 'path': i.path, 'id': i.id})
        time.sleep(2)
            

if __name__ == "__main__":
    db.connect()
    w = WatchFile(path='.')
    for i in range(4):
        t = Uploader(str(i))
        t.setDaemon(True)
        t.start()
    #loop_histroy()
    while 1:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    del w
    db.close()




