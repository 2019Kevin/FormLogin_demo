#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import lxml.html
import time


URL = 'https://www.zhihu.com'
LOGIN_URL = 'https://www.zhihu.com/#signin'
YZM_URL = 'https://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000)  #验证码的URL
session = requests.Session()
headers = {'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
           }

#获取验证码，其实现在知乎不需要输入验证码了。
def get_captcha(data):
    with open('captcha.gif','wb') as fp:
        fp.write(data)
    return input('输入验证码：')


def login(username,password, getcaptcha):
    html = session.get(LOGIN_URL, headers=headers).text
    tree = lxml.html.fromstring(html)
    for tag in tree.cssselect('input'):
        if tag.get('name') == '_xsrf':
            _xsrf = tag.get('value')         #从登陆表单中抽取_xsrf的值
            break
    captcha_content = session.get(YZM_URL, headers=headers).content    #是字节数据
    data = {                                                #构建提交的表单数据
        "_xsrf":_xsrf,
        "email":username,
        "password":password,
        "remember_me":True,
        "captcha": getcaptcha(captcha_content),
    }
    wb_data = session.post('https://www.zhihu.com/login/email',data,headers=headers)   #提交表单数据
    '''
    第一种验证登陆成功的方式
    try:
        assert r'\u767b\u5f55\u6210\u529f' in wb_data.text      #若成功登陆,那么返回的内容中包括其信息
    except:
        print('您的邮箱账号或密码错误,请重新登陆')
    else:
        print('您已经成功登陆!')
    '''
    Text = session.get(URL, headers=headers).text
    tree = lxml.html.fromstring(Text)
    try:
        if tree.cssselect('span.name')[0].text == 'Denver2014':        #第二种是验证首页是否包含用户名
            print('登陆成功')
        else:
            print('登陆失败')
    except:
        print('您的邮箱账号或者密码错误,请重新登陆')
    return session          #若成功登陆,返回这个session对象,这个保存了cookie信息


def getHtml():
    wb_data = session.get(LOGIN_URL, headers=headers)
    with open('zhihu_shouye.html', 'w') as f:
        f.write(wb_data.text)


if __name__ == "__main__":
    Name = input('您的邮箱: ')
    Pwd = input('您的密码: ')
    session = login(username=Name, password=Pwd, getcaptcha=get_captcha)
    getHtml()
