# 站酷Zcool_图片爬虫_edge.py
# beta version
# Copyright (C) 2023-  Chi Xianzheng.
# email: 2489798267@qq.com  or 13789955221@139.com
#
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
# 本代码有 按照图片大类目录爬取 和  按照关键字检索爬取 两种方式，请根据需要使用其中一种，并注释掉另一种代码
# 针对每个问题，在所有回答爬完后，会爬取的图片会保存到文件夹中。
#getPic（）方法中的，通过设置range(*)中的数值和action.scroll_by_amount(0, *)来调整具体图文页面的下拉次数和下拉长度
#while 循环中通过设置range(*)中的数值和action.scroll_by_amount(0, *)来调整全局图文页面的下拉次数和下拉长度

import os
import shutil
import time
import re
from urllib.request import urlretrieve
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.edge.options import Options #使用 Options 对象可以设置浏览器的一些配置选项，
from selenium.webdriver.common.action_chains import ActionChains #ActionChains是模拟鼠标的一些操作
from selenium.webdriver.common.by import By #导入By包进行元素定位
# 下载图片
def loadPicture(pic_url, pic_path,num):
    pic_name = str(100000+num) + ".jpg"
    print(pic_path + pic_name)
    try:
        urlretrieve(pic_url, pic_path+pic_name)
    except:
        pass

# 爬取图片
def getPic(name, url):
    invalid_chars = '[\\\/:*?"<>|]'
    replace_char = '-'
    name=re.sub(invalid_chars,replace_char,name)#设置每个图文栏目文件夹的命名
    path = "D:\\pic_02\\" +name + "\\"#设置图片保存到位置
    if os.path.isfile(path):    # Delete file
        os.remove(path)
    elif os.path.isdir(path):   # Delete dir
        shutil.rmtree(path, True)
    os.makedirs(path)           # create the file directory

    driver.get(url)
    #以下根据页面具体的图文长度进行微调
    for i in range(20):
      action.scroll_by_amount(0, 1500)  # 将页面向下滚动1500像素
      action.perform()  # 执行
      time.sleep(0.1)

    elems = driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section/div[1]/div/section[2]/section/section/section/div/div[1]/img')
    i = 0
    num=1  #将每个图文栏目的图片按照顺序以数字命名
    for elem in elems:
        url = elem.get_attribute('src')
        print(url)
        loadPicture(url,path,num)
        num+=1


driver=WebDriver()
action = ActionChains(driver)
#站酷登录页面
url0="https://passport.zcool.com.cn/loginApp.do?appId=1006&cback=https%3A%2F%2Fwww.zcool.com.cn%2Fu%2F26590055"
driver.get(url0)
time.sleep(10)#此处根据登录需要调整等待时间

#-------------------part1：按照图片分类爬取----------------------

url = 'https://www.zcool.com.cn/discover?cate=1&subCate=292&page=1'
#想要爬取的图片类型的网址，如艺术插画，AI创作等等，从discover中选择类型
driver.get(url)
time.sleep(2)

urls = []   #存放图文链接
titles = []  #存放图文标题
pagenum=1
#爬取某个图片大类下的多个页面
while True:
    #下拉，以获取该页面的所有图文栏目
    for j in range(15):
        action.scroll_by_amount(0, 1500)  # 将页面向下滚动20000像素
        action.perform()  # 执行
        time.sleep(0.1)
    elems = driver.find_elements(By.XPATH, '// *[ @ id = "__next"] / main / section / section[2] / section / div / section / div[1] / span[1] / a')

    #将图文栏目的url和标题保存到列表
    for elem in elems:
        name = elem.text
        url = elem.get_attribute('href')
        print(name, url)
        titles.append(name)
        urls.append(url)

    pagenum += 1
    #翻页，如果更改爬取的图片大类，此处链接需要随之调整
    urlupdate=f"https://www.zcool.com.cn/discover?cate=1&subCate=292&page={pagenum}"
    driver.get(urlupdate)
    time.sleep(1)
    #此处设置爬取的页数
    if pagenum>=2:
        break

i = 0
while i < len(urls):
    getPic(titles[i], urls[i])
    i = i + 1

#----------------------------part1-----------------------------------



#-------------------part2：按照关键词检索爬取----------------------------
# url = 'https://www.zcool.com.cn/search/content?word=AI'# 想要爬取的图片关键词网址
# driver.get(url)
# time.sleep(2)
#
# urls = []  # 存放图文链接
# titles = []  # 存放图文标题
#
# # 爬取某个图片大类下的多个页面
# while True:
#     # 下拉，以获取该页面的所有图文栏目
#     for j in range(15):
#         action.scroll_by_amount(0, 1500)  # 将页面向下滚动20000像素
#         action.perform()  # 执行
#         time.sleep(0.1)
#     elems = driver.find_elements(By.XPATH,
#                                  '// *[ @ id = "__next"] / main / div / div / div[2] / section[3] / section / section / div[*] / div[2] / a')
#
#
#     # 将图文栏目的url和标题保存到列表
#     for elem in elems:
#         name = elem.text
#         url = elem.get_attribute('href')
#         print(name, url)
#         titles.append(name)
#         urls.append(url)
#     break
#
# i = 0
# while i < len(urls):
#     getPic(titles[i], urls[i])
#     i = i + 1
#----------------------------part2---------------------------------