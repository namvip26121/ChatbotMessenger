import json
import requests

def getCity(city):
    with open("tinh.json", 'r',encoding='utf-8') as f:
        a = json.load(f)
    for tinh in a:
        lat = tinh[city]['lat']
        lon = tinh[city]['lon']
    return str(lat) + " " + str(lon)
def getsun_mood(data) :
    a = []
    sunrise = data['forecast']['forecastday'][0]['astro']['sunrise']
    sunset = data['forecast']['forecastday'][0]['astro']['sunset']
    a.append(sunset)
    a.append(sunrise)
    return a

def weather_hour(data,date,hour,namecity):
        information_weather = []
        weather_history = data['forecast']['forecastday']
        for i in weather_history[0]['hour']:
            if date +" " +hour== i['time']:
                #Trời sáng hay tối
                information_weather.append(i['is_day'])

                #Thời gian
                information_weather.append(i['time'])

                 #nhiệt độ hiện tại
                information_weather.append(i['temp_c'])

                # nhiệt độ cảm nhận
                information_weather.append(i['feelslike_c'])

                #Mô tả thời tiết
                information_weather.append(i['condition']['text'])

                # tốc độ gió
                information_weather.append(i['wind_kph'])

                #Độ ẩm
                information_weather.append(i['humidity'])

                 # tầm nhìn
                information_weather.append(i['vis_km'])

                # chỉ số uv
                information_weather.append(i['uv'] )

                #Khả năng mưa
                information_weather.append(i['chance_of_rain'])

                #lượng mưa
                information_weather.append( i['precip_mm'])

                #icon
                information_weather.append(i['condition']['icon'])
        return information_weather

def weather_day(data,namecity):

        information_weather_day = []
        information_weather_day.append('None')
        information_weather_day.append(data['forecast']['forecastday'][0]['date'])
        i = data['forecast']['forecastday'][0]['day']
         # nhiệt độ max trong ngày
        information_weather_day.append(i['maxtemp_c'])

         # nhiệt độ min trong ngày
        information_weather_day.append(i['mintemp_c'])

         # nhiệt độ trung trong ngày
        information_weather_day.append(i['avgtemp_c'])

        # mô tả
        information_weather_day.append(i['condition']['text'])

         # tốc độ gió  max trong ngày
        information_weather_day.append(i['maxwind_kph'] )

        # tổng lương mưa
        information_weather_day.append(i['totalprecip_mm'])

        # tầm nhìn xa
        information_weather_day.append(i['avgvis_km'])

        # độ ẩm
        information_weather_day.append(i['avghumidity'])

        # chỉ số uv
        information_weather_day.append(i['uv'])

        information_weather_day.append(i ['condition']['icon'])


        return information_weather_day

def weather_current(data,namecity):
        information_weather_day = []
        # buổi sáng hay tối
        information_weather_day.append(data["current"]['is_day'])
        #thời gian gần nhất
        information_weather_day.append(data["current"]["last_updated"])
        # nhiệt độ hiện tại
        information_weather_day.append(data["current"]["temp_c"])
        # nhiệt độ cảm nhận
        information_weather_day.append(data["current"]["feelslike_c"])
        # mô tả thơi tiết
        information_weather_day.append(data["current"]["condition"]["text"])
        #tốc độ gió
        information_weather_day.append(data["current"]["wind_mph"])
        #hướng gió
        #áp suất
        information_weather_day.append(data["current"]["pressure_mb"])
        #Lương mưa
        information_weather_day.append(data["current"]["precip_mm"])
        # độ ẩm
        information_weather_day.append(data["current"]["humidity"])
        # Tầm nhìn
        information_weather_day.append(data["current"]["vis_km"])
        #chỉ số UV
        information_weather_day.append(data["current"]["uv"])
        information_weather_day.append(data["current"]["condition"]["icon"])
        return information_weather_day
