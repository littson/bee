# coding=utf-8
import sys
import requests
import re

def v2ex(cfg):
    return run(cfg)

if __name__ == '__main__':
    #TODO pass in cfg
    run()

def run(cfg):
    s = requests.Session()
    s.headers.update({'User-Agent': 'My Agent'})
    # get signin form
    r = s.get('http://v2ex.com/signin')
    match = re.search('<input type="hidden" value="(\w*)" name="once" />',r.text)
    if(not match):
        return 'can not signin!'

    once = match.group(1)
    payload = {'u':cfg['username'], 'p':cfg['password'], 'once':once.encode('ascii','ignore'), 'next':'/'}
    s.headers.update({'Referer': 'http://v2ex.com/signin'})
    # post signin form
    r1 = s.post('http://v2ex.com/signin', data=payload)

    # get daily mission form
    r2 = s.get('http://v2ex.com/mission/daily')
    match = re.search('/mission/daily/redeem\?once=(\d+)', r2.text)
    if(not match):
        return get_login_days(r2.text)

    once = match.group(1)
    # post daily misson
    r3 = s.get('http://v2ex.com/mission/daily/redeem?once=%s' % once)
    return get_login_days(r3.text)

def get_login_days(text):
    # print u'已连续登录 n 天'
    match = re.search(u'\u5df2\u8fde\u7eed\u767b\u5f55 (\d+) \u5929', text)
    if(not match):
        return 'can not get login days!'
    return (match.group(0), match.group(1))

