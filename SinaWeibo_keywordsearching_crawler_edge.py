# SinaWeibo_keywordsearching_crawler_edge.py
# 新浪微博关键字检索推文爬虫
# beta version
# Copyright (C) 2023-  Chi Xianzheng.
# email: 2489798267@qq.com  or 13789955221@139.com
# github：https://github.com/Chase9527/myCrawler.git
# This software is provided 'as-is', without any express or implied warranty.
# In no event will the author be held liable for any damages arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,including commercial applications,
# and to alter it and redistribute it freely, subject to the following restrictions:
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

#使用说明：
# 运行代码后，Edge浏览器窗口打开后需要登录。
# 本代码为第一部分——关键字检索/话题检索评论爬取，适用于微博关键字检索和某个话题下的发文内容爬取
# 针对推文内容，在所有回答爬完或下拉循环次数达到后，会将爬取到的评论存放到keywordsearch.xlsx文件中
# http变量为需要爬取的推文的网址
# for i in range(1,25):其中25为循环下拉的次数，请根据爬取需要设置爬取页数
# searchmode=topicsearch#此处设置爬取模式，keywordsearch为关键字检索爬取，topicsearch为话题内容爬取


# 如需使用chrome浏览器进行爬取，调整以下导入语句中的edge为chrome即可：
# from selenium.webdriver.edge.webdriver import WebDriver
# from selenium.webdriver.edge.options import Options

from selenium.webdriver.edge.webdriver import WebDriver # 导入 webdriver
from selenium.webdriver.common.action_chains import ActionChains #ActionChains是模拟鼠标的一些操作
from lxml import etree #通过xpath解析DOM树的时候会使用lxml的etree，可以很方便的从html源码中得到自己想要的内容
from selenium.webdriver.edge.options import Options #使用 Options 对象可以设置浏览器的一些配置选项，
import time
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta

options=Options()
options.add_argument('--start-maximized')#将浏览器窗口最大化，以便在爬取时能够更清晰地获取网页内容。
options.add_argument('--hide-scrollbars')

browser = WebDriver(options=options)
action = ActionChains(driver=browser)

content = []  #微博发文内容
User = []  #微博发文用户
Date = []  #微博发文日期
commentslink = [] #微博发文的评论的链接网址
praisenumber = [] #微博发文获赞数量
commentnum = []  #微博发文下评论数量
forwardnum = []  #微博发文被转发数量


keywordsearch="2"
topicsearch="4"
searchmode=topicsearch#爬取模式

http="https://weibo.com/"
browser.get(http)
time.sleep(15)  # 此等待过程中请自行登录

for i in range(1,25):#此处设置需要爬取的页面数
    print(i)
    #调整，先进入网页进行登录
    # http="https://s.weibo.com/weibo?q=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90"+"&page="+str(i)
    http="https://s.weibo.com/weibo?q=%23%E5%B8%B8%E6%B8%A9%E8%B6%85%E5%AF%BC%23"+"&page="+str(i)
    browser.get(http)
    time.sleep(2)

    #每页下拉到底后再进行统一爬取
    for i in range(15):
        action.scroll_by_amount(0,1000)#将页面向下滚动1000像素
        action.perform()#执行
        pass
    time.sleep(2)

    root=etree.HTML(browser.page_source)#使用XPath表达式提取出页面中所有的回答内容
    page_answers = root.xpath(r'// *[ @ id = "pl_feedlist_index"]/div['+searchmode+']/div[*]/div/div[1]/div[2]')

    # "评论"点击
    try:
        Click_check_total = WebDriverWait(browser, 5).until(
            lambda x: x.find_element(By.XPATH, r'//*[@id="pl_feedlist_index"]/div['+searchmode+']/div[*]/div/div[2]/ul/li[2]/a'))
        action.click(Click_check_total)
        action.perform()
    except:
        pass

    num=0
    for i in page_answers:
        num+=1

        content_i_l = i.xpath(r'./p[2]//text()')
        content_i_text = "".join(content_i_l)
        if content_i_text=="":
            content_i_l = i.xpath(r'./p//text()')
            content_i_text = "".join(content_i_l)
        content.append(content_i_text)

        user_i_l = i.xpath(r'./div[1] / div[2] / a//text()')
        user_i_text = "".join(user_i_l)
        User.append(user_i_text)

        date_i_l = i.xpath(r'./div[2]/a[1]//text()')
        date_i_text="".join(date_i_l)
        Date.append(date_i_text)

        praisenumber_i_l = i.xpath(r'//*[ @ id = "pl_feedlist_index"]/div['+searchmode+']/div['+str(num)+']/div/div[2]/ul/li[3]/a/button/span[2]//text()')
        praisenumber_i_text="".join(praisenumber_i_l)
        praisenumber.append(praisenumber_i_text)

        commentnum_i_l=i.xpath(r'//*[@id="pl_feedlist_index"]/div['+searchmode+']/div['+str(num)+']/div/div[2]/ul/li[2]/a/text()')
        commentnum_i_text="".join(commentnum_i_l)
        commentnum.append(commentnum_i_text)

        #关键字检索下的微博推文下的评论链接获取
        if(commentnum_i_text!='' and commentnum_i_text!=' 评论' and int(commentnum_i_text)>=10):#此处可筛选评论数量
            elem = browser.find_elements(By.XPATH,"//*[@id='pl_feedlist_index']/div["+searchmode+"]/div["+str(num)+"]/div/div[1]/div[2]/div[2]/a")
            print(elem)
            name = elem[0]
            url = elem[0].get_attribute('href')
            print(name, url)
            commentslink.append(url)
        else:
            commentslink_i_text = ""
            commentslink.append(commentslink_i_text)

        forwardnum_i_l=i.xpath(r'// *[ @ id = "pl_feedlist_index"] / div['+searchmode+'] /div['+str(num)+']/div / div[2] / ul / li[1] / a / text()')
        forwardnum_i_text="".join(forwardnum_i_l)
        forwardnum.append(forwardnum_i_text)


def convert_time(time_str):
    """以下函数用于对微博发文时间格式进行初步调整"""
    now = datetime.now()
    try:
        if "分钟前" in time_str:
            minutes = int(time_str.split('分钟前')[0])
            past_time = now - timedelta(minutes=minutes)
            return past_time.strftime("%d-%m-%y %H:%M")

        elif "小时前" in time_str:
            hours = int(time_str.split('小时前')[0])
            past_time = now - timedelta(hours=hours)
            return past_time.strftime("%d-%m-%y %H:%M")

        elif "今天" in time_str:
            time_only = time_str.split('今天')[1].strip()
            time_str = now.strftime("%d-%m-%y") + " " + time_only
            return datetime.strptime(time_str, "%d-%m-%y %H:%M").strftime("%d-%m-%y %H:%M")

        elif "昨天" in time_str:
            time_only = time_str.split('昨天')[1].strip()
            past_time = now - timedelta(days=1)
            time_str = past_time.strftime("%d-%m-%y") + " " + time_only
            return datetime.strptime(time_str, "%d-%m-%y %H:%M").strftime("%d-%m-%y %H:%M")
        else:
            return time_str
    except:
        return time_str

df = pd.DataFrame()
df['User'] =User
df["Content"]=content
df["Date"]=[convert_time(i) for i in Date]
df["praisenumber"]=praisenumber
df["commentnum"]=commentnum
df["forwardnum"]=forwardnum
df["commentslink"]=commentslink
df.to_excel("keywordsearch.xlsx")


