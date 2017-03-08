#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import datetime
import lxml.html
from bs4 import BeautifulSoup
from pprint import pprint


headers = {
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate',
              'Accept-Language': 'en-US,en;q=0.5',
              'Connection': 'keep-alive',
              'Host': 'graduate.hnust.cn',
              'Referer': 'http://graduate.hnust.cn/pyxx/login.aspx',
              'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0'
}

login_url = 'http://graduate.hnust.cn/pyxx/login.aspx'
img_url = 'http://graduate.hnust.cn/pyxx/PageTemplate/NsoftPage/yzm/createyzm.aspx?id={}'.format(datetime.datetime.now().strftime("%H:%M:%S"))
score_url = 'http://graduate.hnust.cn/pyxx/grgl/xskccjcx.aspx'
session = requests.Session()                               #使用seesion登录，可以在接下来的访问中保留登录信息


def get_captcha(data):                                     #手动输入验证码
    with open('captcha.png', 'wb') as fp:
        fp.write(data)
    return input('请输入验证码:')


#html = open('scores.html').read()
def get_score(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        for i in range(5, 20):
            for j in range(1, 5):
                print(soup.select('tr:nth-of-type({}) > td:nth-of-type({})'.format(i, j))[0].get_text(), end='\t')
            if i == 17:
                print('\n-----------------------------')
            print('\n')
    except Exception:
        print('您输入的信息不正确,无法查看成绩,请重新登陆')


def login(username, password, yzm):
    html =  session.get(login_url, headers=headers).text
    tree = lxml.html.fromstring(html)
    __VIEWSTATE = tree.cssselect('input#__VIEWSTATE')[0].get('value')
    __VIEWSTATEGENERATOR = tree.cssselect('input#__VIEWSTATEGENERATOR')[0].get('value')
    captcha_resp = session.get(img_url, headers=headers)

    data = {
        '__VIEWSTATE': __VIEWSTATE,
        '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
        'ctl00$txtusername': username,
        'ctl00$txtpassword': password,
        'ctl00$txtyzm': yzm(captcha_resp.content),
        'ctl00$ImageButton1.x': '0',
        'ctl00$ImageButton1.y': '0'
    }
    session.post(login_url, headers=headers, data=data)                    #提交表单数据
    s = session.get(score_url, headers=headers)                            #利用保存好的登陆信息访问登陆后的成绩页面
    return s.text


if __name__ == '__main__':
    username = input('你的学号：')
    password = input('你的密码: ')
    html = login(username=username, password=password,yzm=get_captcha)
    get_score(html)



















