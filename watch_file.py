from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import gl

class MyHandler(FileSystemEventHandler):
    def on_created(self,event):
        if event.src_path[-4:] == '.ini':
            gl.CREATEDQUE.put({'fresh': True, 'path': event.src_path, 'id': 0})
    
    def on_deleted(self,event):
        pass

    def on_modified(self,event):
        pass

    def on_moved(self,event):
        pass

class WatchFile:
    def __init__(self, path):
        event_handler = MyHandler()
        self.observer = Observer()
        self.observer.schedule(event_handler, path=path, recursive=True)
        self.observer.start()
            
    def __del__(self):
        self.observer.stop()
        self.observer.join()
        del self.observer
        print 'watch quite'
    
