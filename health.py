#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests, json
from bs4 import BeautifulSoup # 要求有lxml模块

class CDNU_HEALTH():
  """
  :Note: CDNU_HEAlTH
  :Author: @Suroy
  :Date: 2021.10.11
  :Update: 21.10.12
  :Version: V1.1
  """


  def __init__(self, cookie=False, payload=False):
    submitFlag, tmp = self.getForm(cookie)
    if submitFlag:
      self.submitForm(cookie, payload, submitFlag)
    elif not tmp:
      print('获取填报数据错误！')
      self.send_notification("Get Error!")
    else:
      print('获取Flag错误！')
      self.send_notification("Flag Error!")

  def getForm(self, cookie=False):
    url = "http://spcp.cdnu.zovecenter.com/Web/Report/Index"

    payload={}
    headers = {
      'Host': 'spcp.cdnu.zovecenter.com',
      'Cookie': 'ASP.NET_SessionId=123; CenterSoftWeb=123',
      'Upgrade-Insecure-Requests': '1',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/6.8.0(0x16080000) MacWechat/3.2(0x13020010) NetType/WIFI WindowsWechat',
      'Referer': 'http://spcp.cdnu.zovecenter.com/Web/Account/ChooseSys',
      'Accept-Language': 'zh-cn',
      'Accept-Encoding': 'gzip, deflate',
      'Connection': 'keep-alive'
    }

    if cookie :
      headers['Cookie'] = cookie # 替换Cookie


    response = requests.request("GET", url, headers=headers, data=payload)
    text = response.text

    if not text: # Null
      return False,False

    soup = BeautifulSoup(text, 'lxml')  # html 为下载的网页，lxml为解析器
    # page = soup.find_all('input', class_= 'd-none d-xl-flex')
    page = soup.find('input', attrs={'name': "ReSubmiteFlag"})

    if page and page['value']: # 提交标签
      submitFlag = page['value']
    else:
      submitFlag = False
    
    return submitFlag, text

  
  def submitForm(self, cookie = False, payload = False, submitFlag = False):
    """
    :Note: 提交表格
    """
    url = "http://spcp.cdnu.zovecenter.com/Web/Report/Index"

    # 不加submitFlag
    payload = "xxxx&ReSubmiteFlag="
    headers = {
      'Host': 'spcp.cdnu.zovecenter.com',
      'Connection': 'keep-alive',
      'Content-Length': '2617',
      'Cache-Control': 'max-age=0',
      'Upgrade-Insecure-Requests': '1',
      'Origin': 'http://spcp.cdnu.zovecenter.com',
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'Mozilla/5.0 (Linux; Android 11; meizu 17 Pro Build/QKQ1.200127.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/045811 Mobile Safari/537.36 MMWEBID/2561 MicroMessenger/8.0.15.2020(0x28000F35) Process/tools WeChat/arm64 Weixin NetType/5G Language/en ABI/arm64',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,image/wxpic,image/sharpp,image/apng,image/tpg,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'Referer': 'http://spcp.cdnu.zovecenter.com/Web/Report/Index',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'en-US,en;q=0.9',
      'Cookie': 'ASP.NET_SessionId=123; CenterSoftWeb=123; CenterSoftWeb=123'
    }

    # 个人信息参数
    if cookie:
      headers['cookie'] = cookie
    if payload:
      headers['payload'] = payload + submitFlag

    response = requests.request("POST", url, headers=headers, data=payload)

    text = response.text


    demo = """<!DOCTYPE html>
<html>

<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0,maximum-scale=1.0, minimum-scale=1.0">
  <title>成都师范学院信息提示页</title>
  <script src="/Web/Scripts/jquery-2.1.4.min.js"></script>
  <link href="/Web/Scripts/layer/mobile/need/layer.css" rel="stylesheet" />
  <script src="/Web/Scripts/layer/mobile/layer.js"></script>
</head>

<body>
  <script type="text/javascript">
    layer.open({shadeClose:false,content: '提交成功！', btn: '确定' , yes: function(index){window.location.href = '/Web/Account/ChooseSys'}});
  </script>
</body>

</html>"""

    state = False # 打卡状态
    if text.find('提交成功！') > 1:
      msg = '打卡完成 ✅'
      state = True
    elif text.find('请勿重复提交！') > 1:
      msg = '打卡失败 ❌'
    else:
      msg = '未知错误，也许是Cookies导致！ ⚠️'

    # 通知消息=
    self.send_notification(msg)
    print(msg)

    return state


  def work(self, cookie=False, payload=False):
    submitFlag, tmp = self.getForm(cookie)
    if submitFlag:
      self.submitForm(cookie, payload, submitFlag)
    else:
      print('获取Flag错误！')
      self.send_notification("Flag Error!")


  # pushpush
  def send_notification(self, content, token = '123', url_mode = 1):
    """
    :Param: content string, msg
    :Param: token
    :Param: Url_mode
    """
    url_host = ['http://www.pushplus.plus/send','http://pushplus.hxtrip.com/send']
    url = url_host[url_mode]
    data = {
        "token": token,
        "title":'⏰ CDNU打卡结果通知',
        "content": content,
        "template": "json"
    }
    body=json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type':'application/json'}
    txt = requests.post(url,data=body,headers=headers)
    return txt




if __name__ == '__main__':
  cookie = 'this is your cookie.';
  payload = 'this is payload.';
  suroy = CDNU_HEALTH(cookie=False, payload = False)
  # suroy.work()
