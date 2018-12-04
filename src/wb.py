#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import re
import json
import base64
import binascii
import getpass
import os
import pickle
import rsa
import requests
import signal
import sys

from sender import WeiboSender

WBCLIENT = 'ssologin.js(v1.4.18)'

session = requests.session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) '

login_data_path = os.path.join(os.path.expanduser('~'), 'wblogin.data')


def encrypt_passwd(passwd, pubkey, servertime, nonce):
    key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(passwd)
    passwd = rsa.encrypt(message.encode('utf-8'), key)
    return binascii.b2a_hex(passwd)


def login_from_passwd():
    username = input('Username> ')
    password = getpass.getpass('Password> ')
    resp = session.get(
        'http://login.sina.com.cn/sso/prelogin.php?'
        'entry=weibo&callback=sinaSSOController.preloginCallBack&'
        'su=%s&rsakt=mod&checkpin=1&client=%s' %
        (base64.b64encode(username.encode('utf-8')), WBCLIENT)
    )

    pre_login_str = re.match(r'[^{]+({.+?})', resp.text).group(1)
    pre_login = json.loads(pre_login_str)
    data = {
        'entry': 'weibo',
        'gateway': 1,
        'from': '',
        'savestate': 7,
        'userticket': 1,
        'ssosimplelogin': 1,
        'su': base64.b64encode(requests.utils.quote(username).encode('utf-8')),
        'service': 'miniblog',
        'servertime': pre_login['servertime'],
        'nonce': pre_login['nonce'],
        'vsnf': 1,
        'vsnval': '',
        'pwencode': 'rsa2',
        'sp': encrypt_passwd(password, pre_login['pubkey'],
                             pre_login['servertime'], pre_login['nonce']),
        'rsakv': pre_login['rsakv'],
        'encoding': 'UTF-8',
        'prelt': '53',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.si'
        'naSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }
    return data


def login_from_file():
    with open(login_data_path, 'rb') as f:
        return pickle.load(f)


def save_login_data(session, uniqueid):
    with open(login_data_path, 'wb') as f:
        pickle.dump((session, uniqueid), f)
        print('（已保存登录信息至 %s）' % login_data_path)


def wblogin(new_login=False):
    if new_login:
        data = login_from_passwd()
    else:
        return login_from_file()

    login_url_list = 'http://login.sina.com.cn/sso/login.php?client=%s' % WBCLIENT

    resp = session.post(login_url_list, data=data)
    match_obj = re.search('replace\\(\'([^\']+)\'\\)', resp.text)
    while match_obj is None:
        print('登录失败，请尝试重新输入账号密码...')
        data = login_from_passwd()
        resp = session.post(login_url_list, data=data)
        match_obj = re.search('replace\\(\'([^\']+)\'\\)', resp.text)

    login_url = match_obj.group(1)
    resp = session.get(login_url)
    login_str = re.search(r'\((\{.*\})\)', resp.text).group(1)
    login_info = json.loads(login_str)
    uniqueid = login_info["userinfo"]["uniqueid"]

    print("登陆成功！")

    save_login_data(session, uniqueid)
    return (session, uniqueid)


def SIGINT_handler(signal, frame):
    print('\n Bye.')
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, SIGINT_handler)

    # wb
    if len(sys.argv) == 1:
        if not os.path.isfile(login_data_path):
            print('之前未登录过，请先登录（wb -l）...')
            exit(-1)
        else:
            (session, uid) = wblogin()
            text = input()
            sender = WeiboSender(session, uid)
            sender.send_weibo(text)

    # wb -l
    elif len(sys.argv) == 2 and sys.argv[1] == '-l':
        (session, uid) = wblogin(new_login=True)
        exit(0)

    # wb -i
    elif len(sys.argv) == 2 and sys.argv[1] == '-i':
        while 1:
            text = input('发微博（Ctrl-C 退出）> ')
            sender = WeiboSender(session, uid)
            sender.send_weibo(text)

    # wb --help
    else:
        print('wbpy - 命令行交互式新浪微博客户端\n')
        print('%-10s %-20s %s' % ('Usage:', 'wb', '使用上一次登录信息'))
        print('%-10s %-20s %s' % ('', 'wb -l', '第一次登录（强制重新登录）'))
        print('%-10s %-20s %s' % ('', 'echo haha | wb', '管道'))
        print('%-10s %-20s %s' % ('', 'wb < data.txt', '文件重定向'))
        exit(0)
