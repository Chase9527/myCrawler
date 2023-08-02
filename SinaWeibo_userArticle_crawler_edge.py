# SinaWeibo_userArticle_crawler_edge.py
# 新浪微博博主主页推文爬虫
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
# 本代码为第二部分——用户发文爬取，适用于微博博主主页下的发文内容爬取
# 针对推文内容，在所有回答爬完或下拉循环次数达到后，会将爬取到的评论存放到resultUserArticle.xlsx文件中
# http变量为需要爬取的推文的网址
# for j in range(600)，其中600为循环下拉的次数，请根据需要爬取的推文数量设置下拉次数
# action.scroll_by_amount(0,500)#将页面向下滚动500像素，此处可设置每次下拉的页面距离，不建议设置过大，否则会导致评论漏爬
# 其他：微博评论的元素Xpath位置具有重复循环特性，故需要少量多次爬取，之后去重处理
# 如需使用chrome浏览器进行爬取，调整以下导入语句中的edge为chrome即可：
# from selenium.webdriver.edge.webdriver import WebDriver
# from selenium.webdriver.edge.options import Options

from selenium.webdriver.edge.webdriver import WebDriver  # 导入 webdriver
from selenium.webdriver.common.action_chains import ActionChains  # ActionChains是模拟鼠标的一些操作
from lxml import etree  # 通过xpath解析DOM树的时候会使用lxml的etree，可以很方便的从html源码中得到自己想要的内容
from selenium.webdriver.edge.options import Options  # 使用 Options 对象可以设置浏览器的一些配置选项，
import time
import pandas as pd
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--start-maximized')  # 将浏览器窗口最大化，以便在爬取时能够更清晰地获取网页内容。
options.add_argument('--hide-scrollbars')

browser = WebDriver(options=options)
action = ActionChains(driver=browser)

http = "https://weibo.com/"
browser.get(http)
time.sleep(15)  # 此等待过程中请自行登录

# 调整，先进入网页进行登录
http = "https://weibo.com/u/1644948230" #此处放置需要爬取的微博博主主页链接
browser.get(http)
time.sleep(2)

user=[]#用户名
Article_content = [] #推文内容
Article_date = [] #推文日期
Article_praise_number = [] #点赞数
Article_comment_number = [] #评论数
Article_forwardnum = [] #转发数
commentslink = [] #推文评论链接

flag=1
for j in range(600):
    root = etree.HTML(browser.page_source)
    # 使用XPath表达式提取出页面中所有的回答内容
    page_answers = root.xpath(r'// *[ @ id = "scroller"] / div[1] / div[*] / div / article')

    # 循环遍历page_answers列表中的每一个回答框，然后提取其中的回答内容。
    num = 0
    for i in page_answers:
        num +=1
        Article_content_i_l = i.xpath(r'./div / div / div[1] / div//text()')
        Article_content_i_text = "".join(Article_content_i_l)
        Article_content.append(Article_content_i_text)

        user_i_l=i.xpath(r'//*[@id="app"]/div[2]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div//text()')
        user_i_text="".join(user_i_l)
        user.append(user_i_text)


        Article_praise_number_i_l=i.xpath(r'./footer / div / div / div / div[3] / div / button / span[2]//text()')
        Article_praise_number_i_text="".join(Article_praise_number_i_l)
        Article_praise_number.append(Article_praise_number_i_text)


        try:
            elem = browser.find_elements(By.XPATH, "//*[@id='scroller']/div[1]/div[" + str(
                num) + "]/div/article/div/header/div[1]/div/div[2]/a")
            print(elem)
            Article_date_i_text = elem[0].get_attribute('title')
            print(Article_date_i_text)
            Article_date.append(Article_date_i_text)
        except:
            Article_date_i_text = ""
            Article_date.append(Article_date_i_text)



        Article_comment_number_i_l=i.xpath(r'./footer / div / div / div / div[2] / div / span//text()')
        Article_comment_number_i_text="".join(Article_comment_number_i_l)
        Article_comment_number.append(Article_comment_number_i_text)

        Article_forwardnum_i_l=i.xpath(r'./ footer / div / div / div / div[1] / div / div / span / div / span// text()')
        Article_forwardnum_i_text="".join(Article_forwardnum_i_l)
        Article_forwardnum.append(Article_forwardnum_i_text)

        if (Article_comment_number_i_text != '' and Article_comment_number_i_text != ' 评论 ' and int(Article_comment_number_i_text) >= 10):
            try:
                elem = browser.find_elements(By.XPATH, "//*[@id='scroller']/div[1]/div[" + str(
                    num) + "]/div/article/div/header/div[1]/div/div[2]/a")

                print(elem)
                name = elem[0]
                url = elem[0].get_attribute('href')
                print(name, url)
                commentslink.append(url)
            except:
                commentslink_i_text = ""
                commentslink.append(commentslink_i_text)
        else:
            commentslink_i_text = ""
            commentslink.append(commentslink_i_text)


        flag+=1
    print("flag:",flag)
    action.scroll_by_amount(0,500)#将页面向下滚动500像素
    action.perform()#执行
    pass

df = pd.DataFrame()

df["user"]=user
df["Article_content"] = Article_content
df["Article_praise_number"] = Article_praise_number
df["Article_date"]=Article_date
df["Article_comment_number"]=Article_comment_number
df["Article_forwardnum"]=Article_forwardnum
df["commentlinks"]=commentslink

df.dropna(subset=['Article_content'], inplace=True)
df.drop_duplicates(subset=['Article_content'], inplace=True)
df.to_excel('resultUserArticle.xlsx')
