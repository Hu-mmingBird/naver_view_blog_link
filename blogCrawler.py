from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

url="https://search.naver.com/search.naver?where=view&sm=tab_jum&query=%EB%A7%9B%EC%A7%91"
driver=webdriver.PhantomJS("D:\\2021-2\\lesson\\blogCrawler\\phantomjs-2.1.1-windows\\bin\\phantomjs")
driver.implicitly_wait(1)
driver.get(url)

scroll_time=2
scroll_pause_time=2
last_height=driver.execute_script("return document.body.scrollHeight")

#스크롤 아래까지 내리기
while True:
    for i in range(scroll_time):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
    new_height=driver.execute_script("return document.body.scrollHeight")
    if new_height==last_height:
        break
    last_height=new_height


html=driver.page_source
soup=BeautifulSoup(html,'html.parser')
post_lst=soup.find_all(attrs={
    'class':'_more_contents_event_base',
    'class':'lst_total _list_base',
    'class':'bx _svp_item',
    'class':'total_wrap api_ani_send',
    'class':'total_area',
    'class':'api_txt_lines total_tit _cross_trigger'
})

id_list=[]

with open("D:/2021-2/lesson/blogCrawler/id_informations.txt","r") as f:
    while True:
        id=f.readline().strip()
        if not id:
            break
        id_list.append(id)

alert_id_info=[]
for i in post_lst:
    for id in id_list:
        if id in i['href']:
            print(i.text)
            print(i['href'])
            alert_id_info.append(id+' '+i['href'])
print(alert_id_info)
