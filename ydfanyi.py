from requests_html import HTMLSession
import time
import random
import execjs
import os

session = HTMLSession()

# yd加密js
ctx = execjs.compile(open('mdz.js', 'r').read())
lts = round(time.time() * 1000)
salt = int(str(lts) + str(random.randint(0, 9)))

url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
index_url = 'https://fanyi.youdao.com/'

# 设置ua
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 ' \
            'Safari/537.36 '

headers_get = {
    'User-Agent': useragent
}

# 设置cookie重置时间 单位 秒
cookie_reset_time = float(900)

# 获取cookie并防止多次请求cookie
try:
    cookies = open('ydcookies.txt', 'r').read()
    if cookies == '' or (time.time() - os.path.getmtime('ydcookies.txt')) > cookie_reset_time:
        f = open('ydcookies.txt', 'w')
        youdao_index = session.get(url=index_url, headers=headers_get)
        cookies = youdao_index.html.render(script='''
            () => {
                var result = document.cookie
                return result;
            }
        ''')
        f.write(cookies)
        f.close()
except FileNotFoundError:
    f = open('ydcookies.txt', 'w')
    youdao_index = session.get(url=index_url, headers=headers_get)
    cookies = youdao_index.html.render(script='''
                () => {
                    var result = document.cookie
                    return result;
                }
            ''')
    f.write(cookies)
    f.close()

# 翻译目标
word = 'test'

headers_post = {
    'User-Agent': useragent,
    'Cookie': cookies,
    'Host': 'fanyi.youdao.com',
    'Origin': 'https://fanyi.youdao.com',
    'Referer': 'https://fanyi.youdao.com/'

}

data = {
    'i': word,

    'from': 'AUTO',
    'to': 'AUTO',

    'smartresult': 'dict',
    'client': 'fanyideskweb',
    'salt': salt,
    'sign': ctx.call('md5', ("fanyideskweb" + word + str(salt) + "Ygy_4c=r#e#4EX^NUGUc5")),
    'lts': str(lts),
    'bv': ctx.call('md5', useragent),
    'doctype': 'json',
    'version': '2.1',
    'keyfrom': 'fanyi.web',
    'action': 'FY_BY_REALTlME'
}

# 获取结果
result = eval(session.post(url=url, data=data, headers=headers_post).text)

# 翻译源
src = result['translateResult'][0][0]['src']
# 翻译结果
tgt = result['translateResult'][0][0]['tgt']

print(src, tgt)
