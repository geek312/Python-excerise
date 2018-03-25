# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import http.cookiejar
#import urllib
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time


'''
#爬取ip值，供后面爬虫使用
def get_ip_list(url, headers):
    req = urllib.request.Request(url, headers=headers)  
    web_data = urllib.request.urlopen(req)
    soup = BeautifulSoup(web_data.read(), 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies
    
proxy = get_random_ip(ip_list)
proxy_support = urllib.request.ProxyHandler(proxy)
#创建Opener
opener = urllib.request.build_opener(proxy_support)
#添加User Angent
opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
#使用自己安装好的Opener
response = opener.open(url)
#读取相应信息并解码
content = response.read()

url_ = 'http://www.xicidaili.com/nn/'
ip_list = get_ip_list(url_, headers=headers)

单次登录
loginUrl = 'http://accounts.douban.com/login'
s = requests.Session()
formdata = {
            'redir': url,
            'form_email': '13715430738',
            'form_password': 'zhangyuqun0214-',
            'login': '登陆'
                }
content = s.post(loginUrl, data = formdata, headers = headers).text
'''

##
url_base = "https://movie.douban.com/subject/26727273/comments"
url_after = "?sort=new_score&status=P"
comm_user = []
comm_time = []
comm_rate_star = []
comm_rate_level = []
comm_vote = []
comm_cont = []
comm_watched = []
i = 1

#利用记住账号后的cookie登录豆瓣
cookies = {'cookie':'gr_user_id=e343af5e-44fc-4e54-8296-fb047693cb4d; bid=vp_8F7X6Wlw; ll="118281"; __guid=223695111.4263013287088453600.1505008477891.9285; ps=y; __yadk_uid=Se6NV6rSO4GEgNdwXVdsnidse7KYc53V; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1505026571%2C%22https%3A%2F%2Fwww.douban.com%2Fabout%22%5D; dbcl2="166542206:Yl+xL1znqxg"; ck=DrVY; monitor_count=14; _pk_id.100001.4cf6=2e865f9a914a3b3d.1465979086.13.1505027501.1505021564.; _pk_ses.100001.4cf6=*; __utma=30149280.167597013.1458911625.1505021556.1505026425.65; __utmb=30149280.9.6.1505026425; __utmc=30149280; __utmz=30149280.1505026425.65.64.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.16654; __utma=223695111.667028018.1465979086.1505012626.1505026571.13; __utmb=223695111.0.10.1505026571; __utmc=223695111; __utmz=223695111.1505026571.13.13.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/about; ap=1; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=04B3CBA87ACF09BB440B7FB40850C5B8|ee46fcf66da4244da69780629efa8fc3'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

while url_after:
    
    time.sleep(2)
    url = url_base + url_after   
    

    content = requests.get(url, cookies = cookies, headers = headers).text

    soup = BeautifulSoup(content, "html.parser")

    url_after = soup.find_all("a", class_ = "next")[0]["href"]

    for vote in soup.find_all(class_ = "votes"):
        comm_vote.append(int(vote.text))
    
    for info in soup.find_all(class_ = "comment-info"):
        user = re.findall("(<a.*>)(.*?)(</a>)", str(info))[0][1]
        comm_user.append(user)
       
        watched = re.findall("(<span>)(.*?)(</span>)", str(info))[0][1]
        comm_watched.append(watched)
       
        all_ = re.findall("(<span class=)(.*?)( title=)(.*?)(>)", str(info))
        
        if len(all_) == 2:
            rate_star = all_[0][1]
            rate_star = int(re.findall("(allstar)(.*)(0 rating)",rate_star)[0][1])
            rate_level = all_[0][3].replace('"', '')
            comm_rate_star.append(rate_star)
            comm_rate_level.append(rate_level)
       
            time_ = all_[1][3].replace('"', '')
            comm_time.append(time_)
        else:
            comm_rate_star.append('Null')
            comm_rate_level.append('Null')
       
            time_ = all_[0][3].replace('"', '')
            comm_time.append(time_)
        
       
    for comms in soup.find_all(class_ = "comment"):
        comm = re.findall('(<p class="">)(.*)', str(comms))[0][1].replace(' ', '').replace('\r','')
        comm_cont.append(comm)
    
    if i % 100 == 0:
        print('The page%d completed successfully!' % i)
    
    if i == 2600:
        break
    
    i = i + 1
    
print("Spider Finshed Successfully!Totally Get %d data!" % len(comm_user))       
data = pd.DataFrame({"User" : comm_user, "Time" : comm_time, "Rate_Star" : comm_rate_star,
                    "Rate_Level" : comm_rate_level, "Vote" : comm_vote, "Watched" : comm_watched,
                    "Content" : comm_cont})



def f(y):
    if y == 'Null':
        z = 'Null'
    else:
        x = int(y)
        if x < 3:
            z = -1
        elif x > 3:
            z = 1
        else:
            z = 0
    return z

data["Liked"] = data["Rate_Star"].map(f)

data.to_csv("/Users/laihongji/个人文件夹/爬虫+贝叶斯/renmin_analysismm.csv", encoding = 'utf_8_sig')

