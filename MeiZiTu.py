from multiprocessing import Process
import requests
from urllib import request
from bs4 import BeautifulSoup
import re
import os
import time

def run(name):
    print(">>>启动子进程：" + str(os.getpid()))
    count = 1
    headers = {'User-Agent': 'Mozilla/5.0', "referer": "https://www.mzitu.com/"}
    surl = "https://www.mzitu.com/"+name
    r = requests.get(surl, headers=headers)
    sum_init = re.findall(r'https://www.mzitu.com/'+str(name)+'/page/(.*?)/', r.text)
    sum = int(sum_init[3])
    for n in range(1,int(sum)+1):
        print(name+"正在运行！")
        url_1 = "https://www.mzitu.com/"+name+"/page/"+str(n)
        #获取主页面HTML
        html_1 = requests.get(url_1,headers = headers)
        #得到每组图片的url_2页面
        url_2 = re.findall(r'''href="(.*?)" target="_blank"><img class='lazy''',html_1.text)
        for i in range(len(url_2)):
            #获取每组图片的总html,html_2
            html_2 = requests.get(url_2[i],headers = headers)
            #获取每组图片的各自的总数量number
            number = re.findall(r''+str(url_2[i])+'/(\d\d)',html_2.text)

            for j in range(1,int(number[0])+1):
                #构造每张图片所在网址的url,url_3
                url_3 = url_2[i]+"/"+str(j)
                #得到每张图片的所在的html,html_3
                html_3 = requests.get(url_3,headers = headers)
                #获取每张图片的url,p_url
                p_url = re.findall(r'''img src="(.*?)"''',html_3.text)
                print(p_url)
                print(name+"第"+str(i+1)+"组:"+p_url[0])
                picture = requests.get(p_url[0], headers=headers)
                path = "E:/MeiZiTu/"+name+"_"+str(n)+"_"+str(i+1)+"_"+str(j)+"_"+str(count)+".jpg"
                with open(path, 'wb') as f:
                    f.write(picture.content)
                    count = count + 1


if __name__ == '__main__':
    print(">>>启动主进程：" + str(os.getpid()))
    arry = ["xinggan","japan","taiwan","mm"]
    for i in range(0,1):#可以修改成（0,4）启动四个线程
        p = Process(target=run, args=(arry[i],))
        p.start()
    p.join()
    print("主进程结束")

