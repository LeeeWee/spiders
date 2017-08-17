from urllib import request
from bs4 import BeautifulSoup
import urllib
import http.cookiejar
import hashlib
import datetime
import re

#验证码地址
captchaUrl = 'http://210.42.121.132/servlet/GenImg'
#登录的主页面
hosturl = 'http://210.42.121.132'
#post数据接收和处理的页面
posturl = 'http://210.42.121.132/servlet/Login'
#成绩jsp地址
scoreUrl = 'http://210.42.121.132/stu/stu_score_parent.jsp'


stuId = input('请输入用户名： ')
pwd = input('请输入密码： ')
m = hashlib.md5()
m.update(pwd.encode(encoding='utf-8'))
pwd = m.hexdigest()


#设置一个cookie处理器，负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
cj = http.cookiejar.CookieJar()
opener = request.build_opener(request.HTTPCookieProcessor(cj))


#用openr访问验证码地址,获取cookie
picture = opener.open(captchaUrl).read()
#保存验证码到本地
local = open(r'D:\Desktop\captcha.jpg', 'wb')
local.write(picture)
local.close()
#打开保存的验证码图片 输入
CaptchaCode = input('请输入验证码： ')



#构造header，一般header至少要包含以下两项，这两项是从抓到的包里分析得出的
headers = {'Host': '210.42.121.132',
           'Origin': 'http://210.42.121.132',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
           'Referer': 'http://210.42.121.132/'}
#构造Post数据，也是从抓到的包里分析得出
postData = urllib.parse.urlencode({'id': stuId,
                                   'pwd': pwd,
                                   'xdvfb': CaptchaCode}).encode('utf-8')
req = urllib.request.Request(posturl, postData, headers)
#print(request.urlopen(req).read().decode('utf-8'))

response = opener.open(req)            # 访问登录页面
#r = response.read()
response2 = opener.open(scoreUrl)         #访问成绩页面，获得成绩的数据
r = response2.read().decode('gbk')
#print(r)

patten = re.compile('/servlet/Svlt_QueryStuScore\?csrftoken=(.*)&year=0&term=&learnType=&scoreFlag=0&t=')
s = re.search(patten, r)
GMT_FORMAT = '%a%%20%b%%20%d%%20%Y%%20%H:%M:%S%%20GMT+0800%%20(China%%20Standard%%20Time)'
#Fri%20Mar%2003%202017%2001:39:28%20GMT+0800%20(China%20Standard%20Time)
t = datetime.datetime.now().strftime(GMT_FORMAT)
url = 'http://210.42.121.132' + s.group() + t
print(url)

response3 = opener.open(url)
result = response3.read()
print(result.decode('gbk'))


save_path = r"D:\Desktop\snatch2.txt"
# save_path 's file unnecessary to be exist
f_obj = open(save_path, 'wb')
f_obj.write(result)
print("snatch successfully.")

patten2 = re.compile(r'<tr (.*)>(.*)<td>(\d{11})</td>(.*)<td>(.*)</td>(.*)<td>(.*)</td>(.*)<td>(.*)</td>(.*)<td>(.*)</td>(.*)<td>(.*)</td>(.*)<td>(.*)</td>(.*)<td>(.*)</td>(.*)<td>(.*)</td>(.*)<td>(.*)</td>(.*)<td>(.*)</td>(.*)</tr>', re.S)
scores = re.search(patten2, result.decode('gbk'))
print(scores.group(3), scores.group(5), scores.group(7), scores.group(9), scores.group(11), scores.group(13), scores.group(15), scores.group(17), scores.group(19), scores.group(21))
