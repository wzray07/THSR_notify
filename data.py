import json
from datetime import datetime

def delete_data(num):
    try:
        with open("data.json", 'r') as file:
            load_data = json.load(fp = file)
    except:
        print("查詢失敗")
    idNum = list(load_data[num-1])[0]
    load_data.pop(num-1)

    try:
        with open("data.json", 'w') as file:
            json.dump(load_data, file)
            
        with open("search.log", 'a') as log_file:
            log_file.write(datetime.strftime(datetime.now(),'%Y/%m/%d-%H:%M:%S') + ' delete a serach condition, id: ' + idNum + '\n')
    except:
        print('資料處理失敗')


def view_data():
    try:
        with open("data.json", 'r') as file:
            load_data = json.load(fp = file)
    except:
        print("查詢失敗")
    print("\n------------------------------------")
    for i in range(len(load_data)):
        print(str(i+1)+'.')
        idNum = list(load_data[i])[0]
        print("id："+ idNum)
        print("欲查詢日期："+ load_data[i][idNum]["Date"])
        print("欲查詢時間區間："+ load_data[i][idNum]["time_interval"] )
        print("啟程站："+ load_data[i][idNum]["startStation"] )
        print("目的地："+ load_data[i][idNum]["endStation"] )
        print("------------------------------------")

def new_data():
    try:
        with open("data.json", 'r') as file:
            load_data = json.load(fp = file)
    except:
        print("查詢失敗")
    all_date = str(input("請輸入日期 ex.2023/1/1 ："))
    time_interval = str(input("請輸入欲查詢的時間區間(24 小時制) ex.12:00~13:00 ："))
    startStation = str(input("請輸入啟程站全名 ex.南港："))
    endStation = str(input("請輸入目的地站全名 ex.左營："))
    record_time = datetime.strftime(datetime.now(),'%Y/%m/%d-%H:%M:%S')
    record_data = {
        record_time:{
            'Date': all_date,
            'time_interval': time_interval,
            'startStation': startStation,
            'endStation': endStation
        }
    }
    load_data.append(record_data)
    try:
        with open("data.json", 'w') as file:
            json.dump(load_data, file)
        print('完成資料寫入\n')
        with open("search.log", 'a') as log_file:
            log_file.write(datetime.strftime(datetime.now(),'%Y/%m/%d-%H:%M:%S') + ' new a serach condition'+ '\n')
    except:
        print('資料寫入失敗\n')
