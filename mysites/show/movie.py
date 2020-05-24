#coding=utf-8
import requests
import re
import lxml
from time import sleep
from bs4 import BeautifulSoup
from .models import DoubanTask
from .models import DoubanSubject
import time
import selenium
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



def getMovieMessage(url,subject,taskid):#其中flag 用来决定插入哪个数据表 movie或movie2 用来判断使用哪一个数据库插入函数
        print("豆瓣电影链接:{}".format(url))
        # header = dict()
        # #获取请求头的user-agent字典，应付反爬处理
        # header["user-agent"] = random.choice(headerlist)#通过random.choice随机抽取一个user-agent
        header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',}
        director = ''  # 导演
        writer = ''  # 编剧
        actors = ''  # 主演
        type = ''  # 类型
        date = ''  # 上映时间
        timelong = ''  # 时长
        IMDb = ''  # IMDb链接
        text = ''  # 简介
        video = ''  # 预告片
        name=''#片名
        score=''#评分
        try:
            #通过requests.get获取url链接
            r = requests.get(url, headers=header)
            r.raise_for_status()#网页状态码 200
            xml = lxml.etree.HTML(r.text)#将网页源码转为xml 用lxml库进行解析
            # 获取电影名
            n = xml.xpath("//div[@id='content']/h1/span")#通过xpath获取网页标签
            name = n[0].text + n[1].text
            print("片名:{}".format(name))
            div1 = xml.xpath("//div[@id='info']//span[@class='attrs']")
            for i in range(len(div1)):
                if i == 0:
                    #获取电影导演
                    x1 = div1[0].xpath("a")
                    for i in x1:
                        director += i.text + " "
                elif i == 1:
                    #获取电影编剧
                    x2 = div1[1].xpath("a")
                    for i in x2:
                        writer += i.text + " "
                elif i == 2:
                    #获取电影的前几个主演
                    x3 = div1[2].xpath("a")
                    for i in range(5):
                        if i >= len(x3): break
                        actors += x3[i].text + " "
            # 以上这么写原因：有些电影无编剧 无主演 健壮代码
            print("导演:{}".format(director))
            print("编剧:{}".format(writer))
            print("主演:{}".format(actors))
            # 获取电视;类型
            x4 = xml.xpath("//span[@property='v:genre']")
            for i in x4:
                type += i.text + " "
            print("类型:{}".format(type))
            # 获取电视上映日期
            x5 = xml.xpath("//span[@property='v:initialReleaseDate']")
            for i in x5:
                date += i.text + " "
            print("上映日期:{}".format(date))
            district=re.findall(r'制片国家/地区:</span>(.*)<',r.text)[0]
            print("制片国家/地区:{}".format(district))
            # 获取电影片长
            x6 = xml.xpath("//span[@property='v:runtime']")
            for i in x6:
                timelong += i.text + ' '
            print("片长:{}".format(timelong))
            #获取电影的IMDb链接
            div2 = xml.xpath("//div[@id='info']/a/@href")
            if len(div2)!=0:
                IMDb = div2[0]
            print("IMDb链接:{}".format(IMDb))
            #获取电影简介
            x7 = xml.xpath("//span[@property='v:summary']/text()")
            for i in range(len(x7)):
                text += "  " + x7[i].strip()
                if i < len(x7) - 1: text += '\n'
            print("简介:\n{}".format(text))
            score= xml.xpath("//strong[@property='v:average']")[0].text
            print("评分:{}".format(score))
            renshu = xml.xpath("//span[@property='v:votes']")[0].text
            print("人数:{}".format(renshu))
            star=xml.xpath("//div[@class='ratings-on-weight']//span[@class='rating_per']")
            star_five=star[0].text
            star_four=star[1].text
            star_three=star[2].text
            star_two=star[3].text
            star_one=star[4].text
            print(star_five)
            print(star_four)
            print(star_three)
            print(star_two)
            print(star_one)
            S = DoubanSubject(taskid=taskid,subject=subject,name=name,director=director,writer=writer,actors=actors,type=type,date=date,timelong=timelong,IMDb=IMDb,text=text,score=score,star_five=star_five,star_four=star_four,star_three=star_three,star_two=star_two,star_one=star_one,peoplenum=renshu,district=district)
            time.sleep(5)
            S.save()
        except:
            print("无法访问电影详细信息")
            return 0
def doubanTopMovie(Taskid):
    movielist=[]
    header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',}
    for i in range(10):
        website='https://movie.douban.com/top250?start='+str(i*25)+'&filter='
        
        s=requests.get(website,headers=header)
        
        soup = BeautifulSoup(s.text,'html.parser')
        tags = soup.find_all(attrs={"class":"hd"})
        for tag in tags:
            # print(tag)
            movielist.append(tag.a['href'])
            subject = re.findall(r'https://movie.douban.com/subject/(.*)/',tag.a['href'])
        time.sleep(5)
        # print(movelist)
        
    for website in movielist:
        subject = re.findall(r'https://movie.douban.com/subject/(.*)/',website)[0]
        getMovieMessage(website,subject,Taskid)
    
       
        
def searchNewMovie(Taskid):
    import requests
    
    header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',}
    s=requests.session()
    s.get('https://movie.douban.com',headers=header)
    r=s.get('https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%9C%80%E6%96%B0&page_limit=50&page_start=0',headers=header)
    id=[]
    change=r.json()
    new_r=json.dumps(change,ensure_ascii=False)
    n=json.loads(new_r)["subjects"]
    websites=[]
    for i in n:
        websites.append(i['url'])
        id.append(i['id'])
    for i in range(50):
        getMovieMessage(websites[i],id[i],Taskid)
def searchHotMovie(Taskid):
    header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',}
    s=requests.session()
    s.get('https://movie.douban.com',headers=header)
    r=s.get('https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0',headers=header)
    id=[]
    change=r.json()
    new_r=json.dumps(change,ensure_ascii=False)
    n=json.loads(new_r)["subjects"]
    websites=[]
    for i in n:
        websites.append(i['url'])
        id.append(i['id'])
    for i in range(50):
        getMovieMessage(websites[i],id[i],Taskid)
def searchMoviewithkey(Taskid,key,pagenum):
    browser = webdriver.Chrome()
    url = 'https://movie.douban.com/'
    browser.get(url)
    browser.find_element_by_id("inp-query").send_keys(key)
    browser.find_element_by_id('inp-query').send_keys(Keys.ENTER)
    websites=[]
    try:
        for i in range(int(pagenum)-1):
            page = browser.page_source
            soup = BeautifulSoup(page,'html.parser')
            tags = soup.find_all(attrs={"class":"item-root"})
            for tag in tags:
                # print(tag)
                websites.append(tag.a['href'])
            time.sleep(5)
            browser.find_element_by_class_name("next").click() 
    except selenium.common.exceptions.ElementClickInterceptedException:
        pass
    browser.close()
    for website in websites:
        subject = re.findall(r'https://movie.douban.com/subject/(.*)/',website)[0]
        getMovieMessage(website,subject,Taskid)

        