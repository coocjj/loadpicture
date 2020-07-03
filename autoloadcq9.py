import requests
import base64
import ddt,os
import unittest
from LoadCq9Photo.hand_cfg import Hand_cfg
from LoadCq9Photo.hand_json import HandJson
from LoadCq9Photo.func import fc
from multiprocessing import Pool
@ddt.ddt()
class LoadCq9(unittest.TestCase):
    @ddt.data(*fc.get_ddtdata())
    def test_loadcq9(self,data):
        file = os.getcwd() + '\\CQ9160' + '\\' + '{}'.format(data[1]) + '.png'
        with open(file, 'rb') as f:
            data2 = f.read()
        byttr = base64.b64encode(data2)
        hg = Hand_cfg()
        url = hg.get_config("data", "url") + r'CCGameManager/UpdateGameManagementInfo'
        skin = hg.get_config("data", "skin")
        js = HandJson()
        data1 = js.get_value('UpdateGameManagementInfo')
        data1["GameSorts[0][GameId]"] = data[0]
        data1["GameSorts[0][GameIconUrl]"] = byttr
        data1["HomeView"] = skin
        cookie = fc.get_cookie()
        res = requests.post(url=url,data=data1,cookies=cookie)
        code = res.json()["Code"]
        self.assertEqual(code,1)



if __name__ == '__main__':
    unittest.main()


