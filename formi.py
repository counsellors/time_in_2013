# -*- coding: utf-8 -*-
import urllib2, cookielib
import re
import urllib

cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())

opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

content = urllib2.urlopen('https://account.xiaomi.com/pass/serviceLogin').read()

#print content

passToken = ''
#填写小米账号
user = ''
#密码
pwd = ''
callback = 'https://account.xiaomi.com'
sid = 'passport'
qs = '%3Fsid%3Dpassport'
hidden = ''
_sign = ''

#match = re.search(r'"sid" value="(\w+)"',content)
#if match :
#    print match.group(1)
#    sid = match.group(1)

match = re.search(r'"_sign" value="(.+)"',content)
if match :
    print match.group(1)
    _sign = match.group(1)


headers = {
    'User-Agent':' Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'}

postdata=urllib.urlencode({
    'passToken':passToken,
    'user':user,
    'pwd':pwd,
    'callback':callback,
    'sid':sid,
    'qs':qs,
    'hidden':hidden,
    '_sign':_sign})

miurl = 'https://account.xiaomi.com/pass/serviceLoginAuth2'
#print postdata
req = urllib2.Request(
    url = 'https://account.xiaomi.com/pass/serviceLoginAuth2 ',
    data = postdata,
headers = headers)
#result = urllib2.urlopen(req).read()
#print result

cookieJar = cookielib.CookieJar()
cookieProcessor = urllib2.HTTPCookieProcessor(cookieJar) 
opener = urllib2.build_opener(cookieProcessor) 
#params = postdata

#request = urllib2.Request("http://www.somesite.com/Login.do") 
httpf = opener.open(req, postdata) 
#print httpf.read() 
cookieJar.extract_cookies(httpf, req)

cookie_handler= urllib2.HTTPCookieProcessor(cookieJar)
redirect_handler= urllib2.HTTPRedirectHandler()
print cookie_handler
opener = urllib2.build_opener(redirect_handler, cookie_handler)
openurl = 'http://p.www.xiaomi.com/open/index.html'
request = urllib2.Request(openurl,headers = headers) 
resp = opener.open(request)
print resp.read()
#重定向有些问题，目前还无法用于抢购小米手机当然由于小米是json的东西，跳转机制还不明白


