# -*- coding: utf-8 -*-

import time
import re
import json


class WeiboSender(object):

    def __init__(self, session, uid):
        super(WeiboSender, self).__init__()
        self.session = session
        self.uid = str(uid)
        self.Referer = "http://www.weibo.com/u/%s/home?wvr=5" % self.uid

    def send_weibo(self, weibo):
        self.session.headers["Referer"] = self.Referer
        data = self.get_send_data(weibo)
        try:
            self.session.post("https://www.weibo.com/aj/mblog/add?ajwvr=6&__rnd=%d"
                              % int(time.time() * 1000),
                              data=data)
            print('微博发送成功')
        except Exception as e:
            print('微博发送失败')

    def get_send_data(self, text, pids=''):
        data = {
            "location": "v6_content_home",
            "appkey": "",
            "style_type": "1",
            "pic_id": pids,
            "text": text,
            "pdetail": "",
            "rank": "0",
            "rankid": "",
            "module": "stissue",
            "pub_type": "dialog",
            "_t": "0",
        }
        return data
