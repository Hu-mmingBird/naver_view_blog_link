from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import time
import requests
import os
import threading
import telegram
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# [0]에서 메모한 정보를 넣어주세요
my_api_key = ""   #내 API 키 정보
chat_room_id = 1234567890   # 채팅방 ID
current_address = ""

# 텔레그램 봇 세팅
my_bot = telegram.Bot(my_api_key)

def TextPrint(receiver):
    try:
        my_bot.sendMessage(chat_id=chat_room_id, text=receiver)
    except:
        with open(THIS_FOLDER+"/log.txt","a") as f:
            f.write(str(datetime.now())+"\n")
        print("응답없음")

#######################main########################
while True:

    time.sleep(1)
    url="https://search.naver.com/search.naver?where=view&sm=tab_jum&query=%EB%A7%9B%EC%A7%91"
    driver=webdriver.PhantomJS(THIS_FOLDER+"\\phantomjs-2.1.1-windows\\bin\\phantomjs")
    driver.implicitly_wait(2)
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
    with open(THIS_FOLDER+"/"+"id_list.txt","r") as f:
        while True:
            id=f.readline().strip()
            if not id:
                break
            id_list.append(id)


    alert_id_info=[]
    cnt=1
    for i in post_lst:
        # print(i.text)
        # print(i['href'])
        for id in id_list:
            if id in i['href']:
                alert_id_info.append('['+str(cnt)+'] '+id+' '+i['href']+'\n')
        cnt+=1

    if alert_id_info:
        print("!-!-!-!-!-!-!BLOGs FOUND!-!-!-!-!-!-!")
        tmp = ""
        for k in alert_id_info:
            tmp +=  k
        if current_address != tmp:
            TextPrint(tmp)
            current_address = tmp
        print(*alert_id_info,sep='\n')
    else:
        print('-----------BLOGs NOT FOUND-----------')
