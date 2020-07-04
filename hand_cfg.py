import os
from configparser import ConfigParser
path = os.path.abspath(os.path.dirname(__file__)) +'\\ser.ini'
class Hand_cfg():
    def get_config(self,server,key):
        cf = ConfigParser()
        cf.read(path,encoding="utf-8")
        cf.sections()
        data = cf.get(server,key)
        return data

