import datetime
import json
import math
import re
from _datetime import date

from CreatImage import check_background


def location_input(inputtext):
    with open('library_disscu.json', 'r', encoding='utf-8') as input_json:
        input_data = json.load(input_json)
        for data in input_data["intents"][0]["data"]:
            for x in data["patterns"]:
                if x in inputtext:
                    return (data["place"])

def data_input(input_str):
    lists = []
    list_date = []
    check_date = 0
    date_str = datetime.date.today()
    time_str="None"
	# tìm kiếm ngày và giờ trong chuỗi đầu vào bằng biểu thức chính quy
    match = 1
    while(match):
        match = re.search(r"(\d{1,2})[\s/-](\d{1,2})[\s/-](\d{4})?", input_str)
        if not match: break
        check_date = 1
    # nếu tìm thấy, lấy ngày và giờ từ kết quả tìm kiếm
        date_str = match.group()
        list_date.append(date_str)
        input_str = input_str.replace(date_str, "").strip()
    match1 = re.search(r"\d{1,2}(\s*(h|giờ))?", input_str)
    if match1:
        time_str = match1.group()
        match2 = re.search(r"\d{1,2}",time_str)
        check = match2.group()
        if len(check) == 1:
            time_str = '0' + time_str

        if int(time_str[:2]) >= 24:
            return "Thông tin về giờ không chính xác ngoài khoảng [0h-23h]\nVui lòng nhắn help để xem thêm thông tin"
        time_str = re.sub(r"\b(\d{1,2})\s*(h|giờ)\b", r"\1:00", time_str)
    # try:
    l = []
    if check_date:
        lists.append(input_str.replace(time_str, "").strip())
        for i in list_date:
            day,month,year = i.split("/")
            date_str = f"{year}/{month}/{day}"
            date_str = datetime.datetime.strptime(date_str, "%Y/%m/%d")
            l.append(date_str.date())
        lists.append(l)
        lists.append(time_str)
    else:
        lists.append(input_str.replace(time_str, "").strip())
        lists.append(date_str)
        lists.append(time_str)
    # except:
    #     return "Thông tin về ngày không chính xác"
    return lists
def output_data_current(lists,namecity):
    return f"Nhiệt độ : {lists[2]} ℃\n"\
           f"Nhiệt độ cảm nhận : {lists[3]} ℃\n"\
           f"Trời {lists[4]}."
def output_data_day(lists,namecity):
    return f"Nhiệt độ max: {lists[2]} ℃\n" \
           f"Nhiệt độ min: {lists[3]} ℃\n" \
           f"Nhiệt độ TB: {lists[4]} ℃\n" \
           f"Trời {lists[5]}.\n"
def output_data_hour(lists,namecity):
    return f"Nhiệt độ : {lists[2]} ℃\n"\
           f"Nhiệt độ cảm nhận : {lists[3]} ℃\n"\
           f"Trời {lists[4]}.\n"\
           f"Khả năng mưa {lists[10]} %."
def help():
    return f"1.Xem thời tiết hiện tại. " \
           f"\n2.Xem lại thời tiết của vài ngày trước.Ví dụ : thời tiết Hà Nội vào ngày d/m/y(d/m/y -> d/m/d) , giờ cụ thể nếu có."\
           f"\n3.Dự báo thời tiết trong 1 tuần tiết theo.Ví dụ: thời tiết Hà Nội vào ngày d/m/y (d/m/y -> d/m/d), giờ cụ thể nếu có."\
           f"\n3.Biểu đồ nhiệt độ, lượng mưa trong vòng 1 tuần.Ví dụ biểu đồ nhiệt từ d/m/y ... đến  d/m/y"
def getdays(list,lists):
    if len(list) == 3:
        try:
            i =(lists[1] - lists[0]).days
            if lists[1] < lists[0] or i >= 7: return f"Thời gian không chính xác hoặc vượt quá số ngày dự báo"
            return int(i)
        except:
            return 0
    return 0