# SinaWeibo_comments_crawler_edge.py
# 新浪微博推文评论爬虫
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
# 本代码为第四部分——推文评论爬取，适用于微博发文下的评论文本爬取
# 针对推文下的评论，在所有回答爬完或下拉循环次数达到后，会将爬取到的评论存放到commentsresult.xlsx文件中
# http变量为需要爬取的推文评论的网址，同样适用于微博爬虫第一二三部分爬虫结果中所获取的推文评论网址
# for j in range(500)，其中500为循环下拉的次数，请根据评论数量设置下拉次数
# action.scroll_by_amount(0,120)#将页面向下滚动120像素，此处可设置每次下拉的页面距离，不建议设置过大，否则会导致评论漏爬
# 其他：微博评论的元素Xpath位置具有重复循环特性，故需要少量多次爬取，之后去重处理
# 如需使用chrome浏览器进行爬取，调整以下导入语句中的edge为chrome即可：
# from selenium.webdriver.edge.webdriver import WebDriver
# from selenium.webdriver.edge.options import Options

from selenium.webdriver.edge.webdriver import WebDriver # 导入 webdriver
from selenium.webdriver.common.action_chains import ActionChains #ActionChains是模拟鼠标的一些操作
from lxml import etree #通过xpath解析DOM树的时候会使用lxml的etree，可以很方便的从html源码中得到自己想要的内容
from selenium.webdriver.edge.options import Options #使用 Options 对象可以设置浏览器的一些配置选项，
import time
import pandas as pd

#将浏览器窗口最大化，以便在爬取时能够更清晰地获取网页内容。
options=Options()
options.add_argument('--start-maximized')
options.add_argument('--hide-scrollbars') #隐藏浏览器的滚动条，以避免在爬取过程中出现滚动条相关的问题。

browser = WebDriver(options=options)
action = ActionChains(driver=browser)

#调整，先进入网页进行登录
http="https://weibo.com/1910633462/N8j9QDv1x"
browser.get(http)
time.sleep(15)#此等待过程中请自行登录

user=[] #评论用户
answer_content = [] #评论文本内容
answer_date = []  #评论日期
answer_praise_number = []  #评论获赞数量
answer_comment_number = [] #评论下的评论数量

time.sleep(2)

for j in range(600):
    root = etree.HTML(browser.page_source)
    # 使用XPath表达式提取出页面中所有的回答内容
    page_answers = root.xpath(r'////*[@id="scroller"]/div[1]/div[*]/div/div/div')

    # 循环遍历page_answers列表中的每一个回答框，然后提取其中的回答内容。
    for i in page_answers:
        answer_content_i_l = i.xpath(r'./div[1]/div[2]/div[1]/span//text()')
        answer_content_i_text = "".join(answer_content_i_l)
        answer_content.append(answer_content_i_text)

        user_i_l=i.xpath(r'./div[1]/div[2]/div[1]/a[1]//text()')
        user_i_text="".join(user_i_l)
        user.append(user_i_text)

        answer_praise_number_i_l=i.xpath(r'./div[1]/div[2]/div[2]/div[2]/div[4]/button/span[2]//text()')
        answer_praise_number_i_text="".join(answer_praise_number_i_l)
        answer_praise_number.append(answer_praise_number_i_text)

        answer_date_i_l=i.xpath(r'./div[1]/div[2]/div[2]/div[1]//text()')
        answer_date_i_text="".join(answer_date_i_l)
        answer_date.append(answer_date_i_text)

        answer_comment_number_i_l=i.xpath(r'./div[2]/div/div/div/span//text()')
        answer_comment_number_i_text="".join(answer_comment_number_i_l)
        answer_comment_number.append(answer_comment_number_i_text)

    """说明：微博评论的元素Xpath位置具有重复循环特性，故需要少量多次爬取，之后去重处理"""
    action.scroll_by_amount(0,120)#将页面向下滚动120像素
    time.sleep(0.05)
    action.perform()#执行
    pass

df = pd.DataFrame()
df["user"]=user
df["answer_content"] = answer_content
df["answer_praise_number"] = answer_praise_number
df["answer_date"]=answer_date
df["answer_comment_number"]=answer_comment_number

df.dropna(subset=['answer_content'], inplace=True)#去重操作
df.drop_duplicates(subset=['answer_content']and["user"], inplace=True)

df.to_excel('commentsresult.xlsx')






