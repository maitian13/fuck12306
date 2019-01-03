import requests
import re
import information


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Referer': 'https://kyfw.12306.cn/otn/login/init'
}


def station():
    url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9044"
    r = requests.get(url, headers=headers)
    station = re.findall("'(.*)'", r.text)[0]
    station_list = station.split('@')[1:]
    station_dict = {}
    for i in station_list:
        temp_list = i.split('|')
        station_dict[temp_list[1]] = temp_list[2]
    return station_dict


def tickets():
    station_dict = station()
    DATE = information.date
    #FROM_STATION = 'BJP'
    #TO_STATION = 'CDW'
    #DATE = input('输入如下格式的日期2018-01-20：')
    #from_station = input("输入出发地车站：")
    from_station = information.from_station
    to_station = information.to_station
    #to_station = input("输入目的地车站：")
    FROM_STATION = station_dict[from_station]
    TO_STATION = station_dict[to_station]
    url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT".format(DATE, FROM_STATION, TO_STATION)
    r = requests.get(url, headers=headers)
    with open('leftTicketDTO.html', 'wb') as f:
        f.write(r.text.encode(encoding="utf-8"))
    tickets_info = r.json()['data']['result']
    return tickets_info, DATE, from_station, to_station


if __name__ == "__main__":
    tickets()
