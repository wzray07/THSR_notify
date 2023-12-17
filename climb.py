from selenium import webdriver  # auto 
from selenium.webdriver.support.ui import Select  # 下拉式選單
from selenium.common.exceptions import NoSuchElementException
#  verify code ocr
from PIL import Image
import ddddocr
import os
import time
from datetime import datetime
import json
import data
import bot

def check_train(allTime, time_interval):
    t1 = datetime.strptime(time_interval[0], '%H:%M').time()
    t2 = datetime.strptime(time_interval[1], '%H:%M').time()
    # alltime 有票的時刻表出發時間 比對使用者希望的時間
    for i in range(len(allTime)):
        tmp = datetime.strptime(allTime[i], '%H:%M').time()
        if t1 <= tmp <= t2:
            return tmp, False
        else:
            continue

    return "0", True


def check_ticket(driver):
    
    try:
        driver.find_element("xpath", "//span[@class='feedbackPanelERROR' and text()='去程查無可售車次或選購的車票已售完，請重新輸入訂票條件。']")
        return True
    except NoSuchElementException:
        return False

def fill_in(driver, time_interval):
    
    amount = driver.find_element("name", "ticketPanel:rows:0:ticketAmount")
    Select(amount).select_by_visible_text("1")
    stime = driver.find_element("name", "toTimeTable")
    Select(stime).select_by_visible_text(time_interval[0])
    driver.find_element("id", "BookingS1Form_homeCaptcha_passCode").screenshot("./captcha.png")
    img = Image.open("./captcha.png")
    ocr = ddddocr.DdddOcr(beta=True)
    res = ocr.classification(img)
    driver.find_element("name", "homeCaptcha:securityCode").send_keys(res)
    driver.find_element("name", "SubmitButton").click()
    status = False
    match_time = "0"
    os.remove("captcha.png")
    # try:
    #     test = driver.find_elements("xpath", "//input[@name='TrainQueryDataViewPanel:TrainGroup']")
    # except NoSuchElementException:
    #     time.sleep(5)
    #     status = check_ticket(driver)
    #     driver.refresh()
    #     return False, status, match_time
    test = driver.find_elements("xpath", "//input[@name='TrainQueryDataViewPanel:TrainGroup']")
    allTime = []
    for i in range(len(test)):
        allTime.append(test[i].get_attribute('querydeparture'))
    if len(allTime) == 0:
        status = check_ticket(driver) # check 是否為沒票狀態 (True 為沒票)
        if(status): # 檢查過後 確定改為沒票的話代表已完成查詢
            flag = True
        else:
            flag = False
            driver.refresh()
    else:
        match_time, status = check_train(allTime, time_interval)
        flag = True
    time.sleep(1)
    return flag, status, match_time


def climb(start, end, month_int, month, date, year, time_interval, record_time, num):
    flag = False # 有沒有完成查詢 
    status = False # 有沒有票
    option = webdriver.ChromeOptions()
    # delete auto header
    option.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=option)
    driver.get("https://irs.thsrc.com.tw/IMINT/?locale=tw")
    # cookie confirm
    driver.find_element("id", "cookieAccpetBtn").click()
    StartStation = driver.find_element("name", "selectStartStation")
    Select(StartStation).select_by_visible_text(start)
    endStation = driver.find_element("name", "selectDestinationStation")
    Select(endStation).select_by_visible_text(end)

    time.sleep(1)
    driver.find_element("xpath", "//input[@class='uk-input' and @readonly='readonly']").click()
    if datetime(int(year), int(month_int), int(date)).date() != datetime.now():
        driver.find_element("xpath", "//span[@class='flatpickr-day' and @aria-label='{} {}, {}']".format(month, date, year)).click()
    
    # 如果要選當天的名稱不同，要寫判斷
    time.sleep(1)
    while(flag == False):
        flag, status, match_time = fill_in(driver, time_interval)
    if status:
        print('no ticket')
        with open("search.log", 'a') as log_file:
            log_file.write(datetime.strftime(datetime.now(),'%Y/%m/%d-%H:%M:%S') + ' completed search but no ticket, id:'+ record_time + '\n')
    else:
        print('已匹配到票')
        print('出發時間：' + str(match_time))
        now_time = datetime.strftime(datetime.now(),'%Y/%m/%d-%H:%M:%S')
        bot.send_msg("已於"+now_time+"成功匹配到票\n出發時間："+str(match_time)+"\n啟程站："+start+"\n目的站："+end+"\n請儘速購票！！\n此筆搜尋條件已為您刪除")
        with open("search.log", 'a') as log_file:
            log_file.write(now_time + ' completed search , match time:'+ str(match_time) +', id:'+ record_time + '\n')
        data.delete_data(num)
    return

def main():
    try:
        with open("data.json", 'r') as file:
            load_data = json.load(fp = file)
    except:
        print("File isn't exist")
    allMonth = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    for i in range(len(load_data)):
        idNum = list(load_data[i])[0]
        all_date = load_data[i][idNum]["Date"].split('/')
        time_interval = load_data[i][idNum]["time_interval"].split('~')
        tmp = time_interval[0].split(':')
        if datetime.now() > datetime(int(all_date[0]), int(all_date[1]), int(all_date[2]), int(tmp[0]), int(tmp[1])): # expire
            data.delete_data(i)
            continue
        startStation = load_data[i][idNum]["startStation"]
        endStation = load_data[i][idNum]["endStation"]
        month = allMonth[int(all_date[1])-1]
        date = all_date[2]
        year = all_date[0]
    
        climb(startStation, endStation, all_date[1], month, date, year, time_interval, idNum, i)


if __name__ == '__main__':
    main()
