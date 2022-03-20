#!/usr/bin/python
from cProfile import run
from email import header
import requests,re,json,sys, getopt
import argparse
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from rich.console import Console
from pyfiglet import Figlet
console = Console() #输出带颜色的内容
ret=""
Cookies=json.load(open('config.json','r'))
IP138_Cookie=Cookies["IP138_Cookie"]
baidu_Cookie=Cookies["baidu_Cookie"]
header={
    "Connection": "close",
    "sec-ch-ua": "' Not A;Brand';v='99', 'Chromium';v='99', 'Microsoft Edge';v='99'",
    "Accept": "text/plain, */*; q=0.01" ,
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39",
    "sec-ch-ua-platform": "'macOS'",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cookie": IP138_Cookie
    }
header2={
    "ccept":"*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Referer": "https://baike.baidu.com/item/%E6%B2%A7%E5%B7%9E%E5%B8%82%E5%A4%A9%E6%88%90%E6%88%BF%E5%9C%B0%E4%BA%A7%E5%BC%80%E5%8F%91%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8",
    "sec-ch-ua": "' Not A;Brand';v='99', 'Chromium';v='99', 'Microsoft Edge';v='99'",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "'macOS'",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": baidu_Cookie
    }
def Address(url):
    #该IP的归属地址
    url="https://site.ip138.com/"+url+"/"
    res=requests.get(url=url,headers=header,verify=False)
    bs_xml = BeautifulSoup(res.text, "html.parser")
    div =str(bs_xml.findAll('div',{'class':'result result2'}))
    ret_greed= re.findall(r'<h3>(.*)</h3>',div)
    return ret_greed[0]
    
def AddDomain(url):
    #该域名的归属IP为
    ret=""
    url="https://site.ip138.com/"+url+"/"
    res=requests.get(url=url,headers=header,verify=False)
    bs_xml = BeautifulSoup(res.text, "html.parser")
    div =str(bs_xml.findAll('div',{'id':'J_ip_history'}))
    try:
        ret_greed1= re.findall(r'<span class="date">(.*)</span>',div)
        ret_greed2= re.findall(r'target="_blank">(.*)</a>',div)
        seeis=len(ret_greed1)
        for i in range(seeis):
            ret=str(ret)+"\n         绑定时间-->"+ret_greed1[i]+"\n         绑定IP-->"+ret_greed2[i]+"\n         ---------------------------------------"
        if(ret!=""):
            return ret
        else:
            return "非常抱歉暂时没有找到该归属域名"
    except:
        return "非常抱歉暂时没有找到该归属域名"


def Domain(url):
    #该IP的归属域名
    ret=""
    url="https://site.ip138.com/"+url+"/"
    res=requests.get(url=url,headers=header,verify=False)
    div = str(BeautifulSoup(res.text, "html.parser"))
    #print(div)
    try:
        ret_greed= re.findall(r'<li><span class="date">(.*)</a></li>',div)
        for i in ret_greed:
            ret_greed1= re.findall(r'(.*)</span><a',i)
            ret_greed2= re.findall(r'target="_blank">(.*)',i)
            ret=ret+"\n         绑定时间-->"+ret_greed1[0]+"\n         绑定域名-->"+ret_greed2[0]+FFRecord(ret_greed2[0])+"\n         ---------------------------------------"
        if(ret!=""):
            return ret
        else:
            return "非常抱歉暂时没有找到该归属域名"
    except:
        return "非常抱歉暂时没有找到该归属域名"


def subdomain(url):
    #该域名的归属子域名
    ret=""
    url="https://site.ip138.com/"+url+"/domain.htm"
    res=requests.get(url=url,headers=header,verify=False)
    div = BeautifulSoup(res.text, "html.parser")
    div =str(div.findAll('div',{'class':'panel'}))
    # print(div)
    try:
        ret_greed= re.findall(r'target="_blank">(.*)</a></p>',div)
        for i in ret_greed:
            if(i!="更多子域名"):
                ret=ret+"\n         子域名地址-->"+i+"\n         ---------------------------------------"
        if(ret!=""):
            return ret
        else:
            return "非常抱歉暂时没有找到该归属子域名"
    except:
        return "非常抱歉暂时没有找到该归属子域名"

def FFRecord(url):
    #该域名的归属公司为
    ret=""
    url="https://site.ip138.com/"+url+"/beian.htm"
    res=requests.get(url=url,headers=header,verify=False)
    div = BeautifulSoup(res.text, "html.parser")
    div =str(div.findAll('div',{'class':'panel'}))
    #print(div)
    try:
        ret_greed= re.findall(r'rel="nofollow" target="_blank">(.*)</a>\n</p>',div)
        return "\n         备案号为-->"+ret_greed[0]+Company(Record(ret_greed[0]))
    except:
        return "非常抱歉暂时没有找到该归属公司"


def Record(url):
    ret=""
    url="https://icplishi.com/"+url
    res=requests.get(url=url,headers=header,verify=False)
    div = BeautifulSoup(res.text, "html.parser")
    div =str(div.findAll('div',{'class':'c-bd'}))
    #print(div)
    try:
        ret_greed= re.findall(r'target="_blank">(.*)</a></span></td>',div)
        return ret_greed[0]
    except:
         return "非常抱歉暂时没有找到该归属备案号"
        
def Company(url):
    ret=""
    url="https://baike.baidu.com/wikiui/api/getcertifyinfo?lemmaTitle="+url
    res=requests.get(url=url,headers=header2,verify=False)
    div = BeautifulSoup(res.text, "html.parser")
    #div =str(div.findAll('div',{'class':'panel'}))
    div1=json.loads(div.decode('unicode_escape'))
    ret=ret+"\n         公司名称-->"+div1['data']['lemmaTitle']+"\n         公司地址-->"+div1['data']['location']+"\n         公司税号-->"+div1['data']['creditNo']+"\n         资产金额-->"+div1['data']['regCapital']
    return ret

def main(argv):
    try:
        getopt.getopt(argv,"hu:d",["url=","domain="])
    except getopt.GetoptError:
        console.print("查询IP归属与归属地址-->IpconFig.py -u 127.0.0.1", style='bold green')
        console.print("查询域名及公司归属地-->IpconFig.py -d www.baidu.com", style='bold green')
        sys.exit(2)
    if(argv[0]=="-d"):
        console.print("该域名的归属IP为："+AddDomain(argv[1]), style='bold green')
        console.print("该域名的归属子域名："+subdomain(argv[1]), style='bold green')
        console.print("该域名的归属公司为："+FFRecord(argv[1]), style='bold green')
    elif(argv[0]=="-u"):
        console.print("该IP的归属地址："+Address(argv[1]), style='bold green')
        console.print("该IP的归属域名："+Domain(argv[1]), style='bold green')  
    elif(argv[0]=="-h"): 
        console.print("查询IP归属与归属地址-->IpconFig.py -u 127.0.0.1", style='bold green')
        console.print("查询域名及公司归属地-->IpconFig.py -d www.baidu.com", style='bold green')



if __name__=="__main__":
    console.print(Figlet(font='slant').renderText('IP Address'), style='bold blue')
    console.print('         Author: Summ1e233 - V2.0    \n', style='bold blue')
    console.print('           输入-h查看说明    \n', style='bold blue')
    console.print('---------------------------------------------------\n', style='bold blue')
    try:
        main(sys.argv[1:])
    except:
        console.print("查询IP归属与归属地址-->IpconFig.py -u 127.0.0.1", style='bold green')
        console.print("查询域名及公司归属地-->IpconFig.py -d www.baidu.com", style='bold green')