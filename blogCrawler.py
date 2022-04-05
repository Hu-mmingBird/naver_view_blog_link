from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import os
import threading
import telegram
from telegram.ext import Updater, CommandHandler
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# [0]에서 메모한 정보를 넣어주세요
my_api_key = "5115834164:AAG43dsLBxt9g5ybkZ3aZP2LGu94ueohHAs"   #내 API 키 정보
chat_room_id = 1872321401   # 채팅방 ID
current_address = ""

# 텔레그램 봇 세팅
my_bot = telegram.Bot(my_api_key)
updater = Updater(my_api_key)       # 봇에게 들어온 메시지가 있는지 체크
updater.dispatcher.stop()
updater.job_queue.stop()
updater.stop()

def TextPrint(receiver):
    my_bot.sendMessage(chat_id=chat_room_id, text=receiver)


def checker():
    global current_address
    address = ""
    while True:
        if address != current_address:
            my_bot.sendMessage(chat_id=chat_room_id, text=address)
            address = current_address
        time.sleep(10)  # 10초 마다 동작하도록 딜레이

# 기능과 명령어 연결
updater.dispatcher.add_handler(CommandHandler("hi", TextPrint))

# 텔레그램 봇 시작
updater.start_polling()
updater.idle()

t=threading.Thread(target=checker)
t.start()

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
    for i in post_lst:
        # print(i.text)
        # print(i['href'])
        for id in id_list:
            if id in i['href']:
                alert_id_info.append(id+' '+i['href']+'\n')

    if alert_id_info:
        print("!-!-!-!-!-!-!BLOGs FOUND!-!-!-!-!-!-!")
        tmp = ""
        for k in alert_id_info:
            tmp +=  k
        current_address = tmp
        # print(*alert_id_info,sep='\n')
        
    else:
        print('-----------BLOGs NOT FOUND-----------')
    break
