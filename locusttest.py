from locust import task,HttpLocust,TaskSet
from queue import Queue
import os
import json
import re
class RedRain(TaskSet):
    def login(self):
        login_name_data = self.locust.login_name_data.get()
        self.login_name = login_name_data['UserName'].strip('\n')
        self.res = self.client.get("/api/GetValidateTokenKey").json()
        self.token = self.res['Data']['Value']
        self.header = {'ValidateToken': self.token}
        data = self.locust.common_data
        param_data = json.loads(data["param"])
        param_data.update({"username":self.login_name})
        data.update({'param': json.dumps(param_data)})
        res = self.client.post("/api/Login",headers=self.header,data=data)
        self.lg = res.headers['Set-Cookie']

    def on_start(self):
        self.login()

    @task
    def rain(self):
        logsessionid = re.search('LoginSessionID=(.*); path=/', self.lg).group(1)
        head = {"ValidateToken": self.token, "LoginSessionID": logsessionid}
        data = {"param":'{"SingTime":13}'}
        res = self.client.get('/api/GetRedPacket',headers=head,data=data)
        print(res.text)


class WebsitUser(HttpLocust):
    with open('account.txt', 'r') as f:
        account_list = f.readlines()

    # 公共登录参数
    common_data = {
        "param": '{"OnlyFlag":"5d9a4672fb5e36f1f8cd4e45ef28cb59","ClientFlag":"Android","Password":"8196658ecaeceb870d0ad3053dd579d2","ValidateCode":""}'
    }

    login_name_data = Queue()   # 存储用户login_name
    for account in account_list:
        data = {
            "UserName": account
        }
        login_name_data.put_nowait(data)
    task_set = RedRain
    min_wait = 300
    max_wait = 600


if __name__ == '__main__':
    os.system("locust -f locusttest.py --host=http://csdqthcapi.lx901.com")
