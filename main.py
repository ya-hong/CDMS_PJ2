from bookstore import serve
import threading
import os
import json
from urllib.parse import urljoin
import requests
import time
import pprint


if __name__ == '__main__':
   thread = threading.Thread(target = serve.run_server)
   thread.start()
   time.sleep(0.5)
   while True:
      cmd = input('输入测试指令 (将需要测试的指令写在test_commands文件夹下，再在此输入文件名) \n')
      if cmd == 'end':
         break
      with open(os.path.join('test_commands', cmd + '.json'), 'r') as f:
         dic = json.load(f)
         print(dic)
      url = urljoin('http://127.0.0.1:5000/', dic['url'])
      print(url)
      
      # headers = {"token": self.token}
      r = requests.post(url, json=dic)
      print(r)
