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




