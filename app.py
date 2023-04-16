import os, sys,Send_image
import datetime

import CreatImage
from flask import Flask, request
import requests
from pymessenger import Bot
import json
import weather
import messages_users

app = Flask(__name__)

API_KEY_WEATHER = 'DFE1F06F78594F709C3184958230504'
FB_API_URL = 'https://graph.facebook.com/v13.0/me/messages'
PAGE_ACCESS_TOKEN = "EAAJQwAVS4moBAOAK1CQbQARSswl5Ujz6UKcu6WDIey3qZBaELeiCtLXOyjZALwaEZBEbrHHHZApXNq5FzmaqwR156BcxvvS5l3sYvT09W8srAbBQrZBWhIhfmcjKG8O1W1lSQnCovlPrubRJJIK1YXeLW8eNCkJ2UOvyXm9nxd3ZByz8JSIJPye9QmDnZBf9ZCUZBkFPTUkzHNgZDZD"
bot = Bot(PAGE_ACCESS_TOKEN)

list_input = ["help","hi","hello","xin chào","chào","chào bạn"]

def geturl_current(API_KEY_WEATHER,city):
    lat , lon = weather.getCity(city).split()
    print("current",lat,lon)
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY_WEATHER}&q={lat},{lon}&lang=vi"
    response = requests.get(url)
    print(response.json())
    if response.status_code == 200:
        return response
    return "Không kết nối đươc đến Server API"
def geturl_history_or_forecast(API_KEY_WEATHER,city,Date,Respone):
    lat, lon = weather.getCity(city).split()
    print("history",lat, lon)
    url = f"https://api.weatherapi.com/v1/{Respone}?key={API_KEY_WEATHER}&q={lat},{lon}&dt={Date}&&lang=vi"
    response = requests.get(url)
    if response.status_code == 200:
        return response
    return "Không kết nối đươc đến Server API"

@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
    data = json.loads(request.data.decode("utf-8"))
    log(data)
    messenger_error=None
    processing = True
    try:
        if data['object'] == "page" and processing:
            processing =False
            entries = data['entry']
            for entry in entries:
                sender_id = entry['messaging'][0]['sender']['id'] #lấy id của người dùng
                try:
                    messenger_text = str(entry['messaging'][0]['message']['text']) #lấy nội dung tin nhắn từ người dùng
                except:bot.send_text_message(sender_id,f"Xin lỗi tôi không hiểu\nVui lòng nhắn help để xem hướng dẫn")
                recipient_id = entry['messaging'][0]['recipient']['id'] # id của chatbot
                #timesstamp = entry['messaging'][0]['timestamp']
                if messenger_text.lower() in list_input:  # hướng dẫn người dùng
                    if messenger_text.lower() != "help":
                        bot.send_text_message(sender_id,f"Chào bạn!\n" \
                        f"Tôi là chatbot giúp xem thời tiết 63 tỉnh thành tại Việt Nam\n"\
                        f"Vui lòng chat help để xem hướng dẫn.")
                    else:
                        bot.send_text_message(sender_id,messages_users.help())
                    break
                try:
                    name_city = messages_users.location_input(messenger_text) # xử lý để lấy tên của tỉnh
                    print(name_city)
                    lists_data_input = messages_users.data_input(messenger_text) # tách các dữ liệu ngày , giờ
                    if isinstance(lists_data_input,str):
                        messenger_error = lists_data_input # thông báo nếu lỗi về ngày/giờ
                        break

                    string_city_input = lists_data_input[0]
                    date_now = datetime.date.today()
                    dateinput = lists_data_input[1]
                    time_input = lists_data_input[2]
                    print(dateinput)
                    days = messages_users.getdays(lists_data_input,dateinput) # số ngày dự báo
                    if isinstance(days,str):
                        messenger_error = days # thông báo lỗi từ người dùng
                        break
                    date_input = ""

                    if isinstance(dateinput,list):
                        date_input = dateinput[0]
                    else: date_input = dateinput

                    date_bieu_do = date_input
                    if "biểu đồ" in messenger_text:
                        list_max = []
                        list_min = []
                        list_day= []
                        for i in range(0, days + 1):
                            response_weather =""
                            print(date_bieu_do)
                            if date_now < date_bieu_do:
                                response_weather = geturl_history_or_forecast(API_KEY_WEATHER, name_city,date_bieu_do,"forecast.json").json()
                            else:
                                response_weather = geturl_history_or_forecast(API_KEY_WEATHER, name_city,date_bieu_do,"history.json").json()
                            list_max.append(response_weather['forecast']['forecastday'][0]['day']['maxtemp_c'])
                            list_min.append(response_weather['forecast']['forecastday'][0]['day']['mintemp_c'])
                            list_day.append(response_weather['forecast']['forecastday'][0]['date'][-5:])
                            date_bieu_do = date_bieu_do + datetime.timedelta(days=1)

                        Send_image.send_image(PAGE_ACCESS_TOKEN,sender_id,Send_image.layattachment_id(PAGE_ACCESS_TOKEN,
                                            CreatImage.Bieudo(list_max,list_min,list_day,name_city,sender_id,response_weather['location']['localtime_epoch'])))
                        break
                    for i in range(0,days+1):
                        if date_now == date_input:
                            # thời tiết hiện tại
                            if time_input == "None":
                                response_weather= geturl_current(API_KEY_WEATHER,name_city).json()
                                list_weather_current = weather.weather_current(response_weather,name_city)
                                text = f"Thời tiết {name_city} vào {list_weather_current[1]}:\n" + \
                                       messages_users.output_data_current(list_weather_current,name_city)
                                print(text)
                                Send_image.send_image(PAGE_ACCESS_TOKEN,sender_id,Send_image.layattachment_id(
                                    PAGE_ACCESS_TOKEN,CreatImage.image_current(list_weather_current,name_city,sender_id,response_weather['location']['localtime_epoch'])))
                                bot.send_text_message(sender_id, text)

                        else:
                            if date_input < date_now:
                                response_weather = geturl_history_or_forecast(API_KEY_WEATHER, name_city, date_input,"history.json").json()
                            else: response_weather = geturl_history_or_forecast(API_KEY_WEATHER, name_city, date_input,"forecast.json").json()

                            if time_input == 'None':
                                # nếu không có giờ cụ thể
                                list_weather_day = weather.weather_day(response_weather, name_city)
                                list_weather_day2 = weather.getsun_mood(response_weather)
                                text =f"Thời tiết {name_city} trong ngày {date_input}:\n"+  \
                                      messages_users.output_data_day(list_weather_day, name_city) # tạo nội dung


                                Send_image.send_image(PAGE_ACCESS_TOKEN,sender_id,Send_image.layattachment_id(
                                PAGE_ACCESS_TOKEN,CreatImage.image_day(list_weather_day,list_weather_day2,name_city,sender_id,response_weather['location']['localtime_epoch'])))
                                bot.send_text_message(sender_id,text) #gửi nội dung
                            else:
                                #nếu có giờ cụ thể
                                list_weather_hour = weather.weather_hour(response_weather,str(date_input),time_input,name_city)
                                text = f"Thời tiết {name_city} vào {date_input} {time_input}:\n" + messages_users.output_data_hour(
                                                                                      list_weather_hour,name_city)
                                Send_image.send_image(PAGE_ACCESS_TOKEN,sender_id,Send_image.layattachment_id(
                                    PAGE_ACCESS_TOKEN,CreatImage.image_hour(list_weather_hour,name_city,sender_id,response_weather['location']['localtime_epoch'])))
                                bot.send_text_message(sender_id,text)
                        date_input = date_input + datetime.timedelta(days=1) # ngày tiếp theo nếu có

                except Exception as e:
                    print("Đã có lỗi xảy ra:", e)
                    if messenger_error == None:
                        bot.send_text_message(sender_id,f"Xin lỗi tôi không hiểu\nVui lòng nhắn help để xem hướng dẫn")
            if messenger_error != None:
                bot.send_text_message(sender_id, messenger_error)
    except:
        print("lỗi tin nhắn")

    return "OK"
def log(message):
    print(message)
    sys.stdout.flush()
if __name__ == '__main__':
    app.run(debug=True,port= '8000')