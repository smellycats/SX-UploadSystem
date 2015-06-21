#-*- encoding: utf-8 -*-
import ConfigParser


class PlateIni:
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()

    def __del__(self):
        del self.cf

    def get_plate(self, path):
        self.cf.read(path)
        info = {}
        for i in self.cf.items('PLATEINFO'):
            info[i[0]] = i[1].decode(encoding='gbk', errors='ignore')

        return info


class MyIni:

    def __init__(self, confpath='upload.conf'):
        self.confpath = confpath
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.confpath)

    def __del__(self):
        del self.cf

    def get_sys(self):
        """获取系统配置参数"""
        conf = {}
        conf['path'] = self.cf.get('SYSSET', 'path')
        conf['port'] = self.cf.getint('SYSSET', 'port')
        conf['timeflag'] = self.cf.get('SYSSET', 'timeflag')

        return conf

    def set_sys(self, timeflag):
        self.cf.set('SYSSET', 'timeflag', timeflag)
        self.cf.write(open(self.confpath, 'w'))




