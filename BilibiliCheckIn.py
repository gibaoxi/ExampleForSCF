# -*- coding: utf8 -*-
import requests 
import json
import time
import re
from bs4 import BeautifulSoup
from json.decoder import JSONDecodeError

cookie = 'innersign=0;buvid3=2D2DDCA0-A21A-A94A-3893-6E0BF6F2757699825infoc;b_nut=1698807799;i-wanna-go-back=-1;b_ut=7;_uuid=1039214EA-8BF6-10DEA-BA99-6E3EAE65F61E01173infoc;enable_web_push=DISABLE;header_theme_version=undefined;home_feed_column=4;buvid4=35B124BF-B304-E6E1-018F-959A69F1EC3902418-023110111-SK3hbof5R8la8CT0PkJUgBxsHnO12KsjNrfPGXWknS6WNc%2B50jo5DQ%3D%3D;buvid_fp=06a7be2320d24966e34bef4edb01144a;SESSDATA=6cb21d23%2C1714359826%2Cb060b%2Ab2CjAdTORdDUZt7Cq-ElsbKPaEU9ILfoxJ2aI21s_ojlJ2FRDKSACVK0tuzeUxMLUHqfkSVk9JVFBqZzRZU2R1cnEybFE1ZWZYckVaWmxqemNMc21Vd2c0cVMwZFY5RFZGSTB5YzZDRlhVUGI2bThDSzhBZlIxbnlSOGJ2aWRzY1VIQmFjVkw4NHpRIIEC;bili_jct=584f29168fbe3544c450c485ccd28473;DedeUserID=318842163;DedeUserID__ckMd5=2581eaa3d06653e7;sid=nin7p3pn;browser_resolution=1141-1931;bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTkwNzgzNzgsImlhdCI6MTY5ODgxOTExOCwicGx0IjotMX0.DZdETpvp2GLbFuyxgJf5C0Er5w54h0MmDcdQJ4rhHfA;bili_ticket_expires=1699078318;b_lsid=F8C38D42_18B90FF233D;bsource=search_google'  # 配置你的cookie
sckey = '' # 配置你的server酱SCKEY
bid = 'BV1mD4y1U7z9'  # 配置需观看的视频BV号

uid=re.match('(?<=DedeUserID=).*?(?=;)',cookie)
sid=re.match('(?<=sid=).*?(?=;)',cookie)
csrf=re.match('(?<=bili_jct=).*',cookie)


# bv转av
def bv_to_av(bv):
    headers={   
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    }
    r = requests.get('https://api.bilibili.com/x/web-interface/view', {'bvid': bv}, headers=headers)
    response = decode_json(r)
    try:
        return str(response['data']['aid'])
    except (KeyError, TypeError):
        return '883409884'

# json解析
def decode_json(r):
    try:
        response = r.json()
    except JSONDecodeError:
        # 虽然用的是requests的json方法，但要捕获的这个异常来自json模块
        return -1
    else:
        return response


# server酱
def pushinfo(info,specific):
    headers={   
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'ContentType': 'text/html'
    }
    requests.session().get("https://sc.ftqq.com/"+sckey+".send?text=" + info + "&desp=" + specific,headers=headers)

# 登录
def login():
    headers={   
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    'Cookie':cookie
    }
    response = requests.session().get('http://api.bilibili.com/x/space/myinfo',headers=headers)
    rejson = json.loads(response.text)
    code = rejson['code']
    msg = rejson['message']
    if code == 0:
        print('登录成功')
        return True
    else:
        print('登录失败：'+msg)
        return False

# 获取用户信息
def get_user_info():
    headers = {
        'Cookie':cookie
    }
    response = requests.session().get('http://api.bilibili.com/x/space/myinfo?jsonp=jsonp',headers=headers)
    rejson = json.loads(response.text)
    code = rejson['code']
    msg = rejson['message']
    if code == 0:
        userInfo=['账号：'+str(rejson['data']['silence']),
        '硬币：'+str(rejson['data']['coins']),
        '经验：'+str(rejson['data']['level_exp']['current_exp'])+"/"+str(rejson['data']['level_exp']['next_exp']),
        '等级：'+str(rejson['data']['level']),
        '昵称：'+str(rejson['data']['name'])
        ]
        print(userInfo[0]) 
        print (userInfo[1])
        print(userInfo[2])
        #response['data']['face'] #头像
        print(userInfo[3])
        print(userInfo[4])
        return userInfo
    else:
        print("用户信息获取失败："+msg)
        return "用户信息获取失败："+msg

# 直播签到
def do_sign():
    headers = {
        'Cookie':cookie
    }
    response = requests.session().get('https://api.live.bilibili.com/sign/doSign',headers=headers)
    rejson = json.loads(response.text)
    code = rejson['code']
    msg = rejson['message']

    if code == 0:
        print('直播签到成功！') 
        return True
    else:
        print("直播签到失败："+msg)
        return False

# 看视频
def watch():
        aid=bv_to_av(bid)
        headers = {
            'Cookie':cookie
        }
        response = requests.session().get('http://api.bilibili.com/x/web-interface/view?aid='+str(aid),headers=headers)
        rejson = json.loads(response.text)
        code = rejson['code']
        #print(response.text)
        if code == 0:
            cid = rejson['data']['cid']
            duration = rejson['data']['duration']
        else:
            print('视频信息解析失败')
            return False
        payload = {
            'aid': aid,
            'cid': cid,
            'jsonp': "jsonp",
            'mid': uid,
            'csrf': csrf,
            'played_time': 0,
            'pause': False,
            'realtime': duration,
            'dt': 7,
            'play_type': 1,
            'start_ts': int(time.time()),
        }
        response = requests.session().post('http://api.bilibili.com/x/report/web/heartbeat',data=payload,headers=headers)
        rejson = json.loads(response.text)
        code = rejson['code']
        if code == 0:
            time.sleep(5)
            payload['played_time'] = duration - 1
            payload['play_type'] = 0
            payload['start_ts'] = int(time.time())
            response = requests.session().post('http://api.bilibili.com/x/report/web/heartbeat',data=payload,headers=headers)
            rejson = json.loads(response.text)
            code = rejson['code']
            if code == 0:
                print(f"av{aid}观看成功")
                return True
        print(f"av{aid}观看失败 {response}")
        return False



def main(*args):
    if login():
        ui = get_user_info()
        desp='直播签到：'+str(do_sign())+'\n\n'+'观看视频：'+str(watch())+'\n\n'+ui[0]+'\n\n'+ui[1]+'\n\n'+ui[2]+'\n\n'+ui[3]+'\n\n'+ui[4]+'\n\n'
        pushinfo('哔哩哔哩签到成功',desp)
    else:
        pushinfo('哔哩哔哩签到失败','')

    

if __name__ == '__main__':
    main()
