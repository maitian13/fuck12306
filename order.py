import requests, time, datetime, re
from urllib import parse
import information, check_tickets, random
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Order(object):
	def __init__(self, headers, session):
		self.headers = headers
		self.req = session

	def buyorder(self, secret_str, DATE, from_station, to_station, left_ticket, train_no, station_train_code, train_date, seat_type, from_station_telecode, to_station_telecode, train_location):
	    now = str(datetime.datetime.now())[:11]
	    url = "https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
	    data = {
	        'secretStr': secret_str,
	        'train_date': DATE,
	        'back_train_date': now,
	        'tour_flag': 'dc',
	        'purpose_codes': 'ADULT',
	        'query_from_station_name': from_station,
	        'query_to_station_name': to_station,
	        'undefined': ''
	    }
	    print('****************************submitOrderRequest***************************')
	    r = self.req.post(url=url, data=data, headers=self.headers)
	    with open('submitOrderRequest.html', 'wb') as f:
	    	f.write(r.text.encode(encoding="utf-8"))
	    result_code = r.json()['status']
	    if result_code is not True:
	        print('下单失败1')

	    url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
	    data = {
	        '_json_att': ''
	    }
	    print('****************************initDc***************************')
	    r = self.req.post(url=url, data=data, headers=self.headers)
	    with open('initDc.html', 'wb') as f:
	    	f.write(r.text.encode(encoding="utf-8"))
	    REPEAT_SUBMIT_TOKEN = re.findall(r"globalRepeatSubmitToken = '(.*?)';", r.text)[0]
	    key_check_isChange = re.findall(r"'key_check_isChange':'(.*?)',", r.text)[0]

	    url = "https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs"
	    data = {
	        '_json_att': '',
	        'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN
	    }
	    print('****************************getPassengerDTOs***************************')
	    r = self.req.post(url=url, data=data, headers=self.headers)
	    with open('getPassengerDTOs.html', 'wb') as f:
	    	f.write(r.text.encode(encoding="utf-8"))
	    #print(bytes(r.text, encoding = 'utf-8').decode('utf-8'))
	    result_code = r.json()['status']
	    if result_code is not True:
	        print('下单失败2')

	    url = "https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
	    passengerTicketStr = ""
	    oldPassengerStr = ""
	    for i in range(0, len(information.identity_name)):
	    	passengerTicketStr = passengerTicketStr + seat_type + ',0,1,' + information.identity_name[i] + ',1,' + information.identity_card[i] + ',,N'
	    	oldPassengerStr += oldPassengerStr + information.identity_name[i] + ',1,' + information.identity_card[i] + ',1_'
	    	if i != (len(information.identity_name)-1):
	    		passengerTicketStr = passengerTicketStr + '_'
	    data = {
	        'cancel_flag': '2',
	        'bed_level_order_num': '000000000000000000000000000000',
	        'passengerTicketStr': passengerTicketStr,
	        'oldPassengerStr': oldPassengerStr,
	        'tour_flag': 'dc',
	        'randCode': '',
	        'whatsSelect': '1',
	        '_json_att': '',
	        'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN
	    }
	    print('****************************checkOrderInfo***************************')
	    r = self.req.post(url=url, data=data, headers=self.headers)
	    with open('checkOrderInfo.html', 'wb') as f:
	    	f.write(r.text.encode(encoding="utf-8"))
	    result_code = r.json()['status']
	    if result_code is not True:
	        print('下单失败3')

	    url = "https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"
	    data = {
	        'train_date': train_date,
	        'train_no': train_no,
	        'stationTrainCode': station_train_code,
	        'seatType': seat_type,
	        'fromStationTelecode': from_station_telecode,
	        'toStationTelecode': to_station_telecode,
	        'leftTicket': left_ticket,
	        'purpose_codes': '00',
	        'train_location': train_location,
	        '_json_att': '',
	        'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN
	    }
	    print('train_date:', train_date, '  train_no:', train_no, '  station_train_code:', station_train_code, '  seat_type:', seat_type, '  from_station_telecode:', from_station_telecode, '  to_station_telecode:', to_station_telecode, '  left_ticket:', left_ticket, '  train_location:', train_location, '  REPEAT_SUBMIT_TOKEN:', REPEAT_SUBMIT_TOKEN)
	    print('****************************getQueueCount***************************')
	    r = self.req.post(url=url, data=data, headers=self.headers)
	    with open('getQueueCount.html', 'wb') as f:
	    	f.write(r.text.encode(encoding="utf-8"))
	    result_code = r.json()['status']
	    if result_code is not True:
	        print('下单失败4')

	    url = "https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
	    data = {
	        'passengerTicketStr': passengerTicketStr,
	        'oldPassengerStr': oldPassengerStr,
	        'randCode': '',
	        'purpose_codes': '00',
	        'key_check_isChange': key_check_isChange,
	        'leftTicketStr': left_ticket,
	        'train_location': train_location,
	        'choose_seats': '',
	        'seatDetailType': '000',
	        'whatsSelect': '1',
	        'roomType': '00',
	        'dwAll': 'N',
	        '_json_att': '',
	        'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN
	    }
	    print(data)
	    print("try to order...........")
	    print('****************************confirmSingleForQueue***************************')
	    r = self.req.post(url=url, data=data, headers=self.headers)
	    print(r.text)
	    with open('confirmSingleForQueue.html', 'wb') as f:
	    	f.write(r.text.encode(encoding="utf-8"))
	    	result_code = r.json()['status']
	    if result_code is not True:
	    	print('下单失败5')

	    random_ = '151737731' + str(random.randint(1000, 9999))
	    url = "https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random={}&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN={}".format(random_, REPEAT_SUBMIT_TOKEN)
	    print('****************************queryOrderWaitTime***************************')
	    r = self.req.get(url)
	    print(r.text)
	    with open('queryOrderWaitTime.html', 'wb') as f:
	    	f.write(r.text.encode(encoding="utf-8"))
	    orderId = r.json()['data']['orderId']


	    url = "https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue"
	    data = {
	        'orderSequence_no':	orderId,
	        '_json_att': '',
	        'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN
	    }
	    print('****************************resultOrderForDcQueue***************************')
	    r = self.req.post(url=url, data=data, headers=self.headers)
	    print(r.text)
	    with open('resultOrderForDcQueue.html', 'wb') as f:
	    	f.write(r.text.encode(encoding="utf-8"))
	    result_code = r.json()['status']
	    if result_code is not True:
	        print('下单失败6')


	def main(self):
	    tickets_info, DATE, from_station, to_station = check_tickets.tickets()
	    TICKET = information.seat_type#input('要买哪种票(无座、硬座、硬卧、软卧、高级软卧、二等座、一等座、商务座)：')
	    seat_type_dict = {'硬座': '1', '硬卧': '3', '软卧': '4', '二等座': 'O', '商务座': 'P'}
	    seat_type = seat_type_dict[TICKET]
	    ticket_dict = {'无座': 26, '硬座': 29, '硬卧': 28, '软卧': 23, '高级软卧': 21, '二等座': 30, '一等座': 31, '商务座': 32}
	    TICKET_NUM = ticket_dict[TICKET]
	    train_date = time.strftime('%a %b %d %Y %H:%M:%S', time.strptime(DATE, '%Y-%m-%d')) + ' GMT+0800 (中国标准时间)'
	    for i in tickets_info:
	        temp_list = i.split('|')
	        print(temp_list[3] + ':' + temp_list[TICKET_NUM])
	        from_station_telecode = temp_list[4]
	        to_station_telecode = temp_list[5]
	        train_location = temp_list[15]
	        train_code = temp_list[3]
	        if temp_list[TICKET_NUM] == '' or temp_list[TICKET_NUM] == '无' or train_code not in information.train_codes:
	            continue
	        else:
	            secret_str = parse.unquote(temp_list[0])
	            left_ticket = temp_list[12]
	            train_no = temp_list[2]
	            station_train_code = temp_list[3]
	            try:
	            	self.buyorder(secret_str, DATE, from_station, to_station, left_ticket, train_no, station_train_code, train_date, seat_type, from_station_telecode, to_station_telecode, train_location)
	            	return True
	            except Exception as error:
	            	print(str(error))
	            	continue
	    else:
	        print('无票')
	        return False
