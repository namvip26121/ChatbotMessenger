from textwrap import fill
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont,ImageFilter
import requests
from io import BytesIO
a = [1, '2023-04-09 09:00', 19.4, 19.4, 'U ám', 3.2, 86, 10.0, 4.0, 0, 0.0, '//cdn.weatherapi.com/weather/64x64/day/122.png']
def check_background(a):
    if a[0] == 1 or a[0] == "None":
        return "background_sang.png"
    else:
        return "background_toi.png"
def image_current(a,namecity,send_id,time):

    background = Image.open(check_background(a))

    # Tải ảnh từ đường dẫn và chuyển đổi thành định dạng Image
    response = requests.get("https:" + a[11])
    img1 = Image.open(BytesIO(response.content))
    img = img1.convert('RGBA')

    background.paste(img, (375, 150))
    draw = ImageDraw.Draw(background)
    y = 200
    font_size = 28
    font = ImageFont.truetype("times.ttf", font_size)

    draw.text((325, 50), f"{str(namecity.upper())}", font=ImageFont.truetype("times.ttf", 40), fill='white')
    draw.text((340, 100), f"{str(a[4])}", font=ImageFont.truetype("times.ttf", 20), fill='white')
    draw.text((25, 50), f"{a[1]}", font=ImageFont.truetype("times.ttf", 25), fill='white')
    draw.text((350, 220), f"{int(a[2])}℃", font=ImageFont.truetype("times.ttf", 50), fill='white')
    draw.line((50, 280, 800, 280), fill=(255, 255, 255))
    draw.text((50, y + 100), f"Tốc độ gió: {a[5]}km/h", font=font, fill='white')
    draw.text((450, y + 100), f"Nhiệt độ cảm nhận: {a[3]}℃", font=font, fill='white')
    draw.text((450, y + 180), f"Áp suất: {a[6]}", font=font, fill='white')
    draw.text((50, y + 180), f"Độ ẩm: {a[8]}%", font=font, fill='white')
    draw.text((50, y + 250), f"Tầm nhìn: {a[9]}km", font=font, fill='white')
    draw.text((450, y + 250), f"Chỉ số UV: {a[10]}", font=font, fill='white')
    file_image = f"F:/chatbot/image/{send_id}_{namecity}_{time}.png"
    background.save(file_image)
    return file_image
def image_day(a,b,namecity,send_id,time):
        background = Image.open(check_background(a))

        # Tải ảnh từ đường dẫn và chuyển đổi thành định dạng Image
        response = requests.get("https:" + a[11])
        img1 = Image.open(BytesIO(response.content))
        img = img1.convert('RGBA')
        background.paste(img, (375, 120))
        draw = ImageDraw.Draw(background)

        font = ImageFont.truetype("times.ttf", 28)

        draw.text((310, 20), f"{str(namecity.upper())}", font=ImageFont.truetype("times.ttf", 40), fill='white')
        draw.text((25, 50), f"{a[1]}", font=ImageFont.truetype("times.ttf", 25), fill='white')

        text_width, text_height = draw.textbbox((0, 0), a[5], font=font)[2:]
        draw.text((50, 200), f"Cao nhất", font=ImageFont.truetype("times.ttf", 30), fill='white')
        draw.text((65, 240), f"{int(a[2])}℃", font=ImageFont.truetype("times.ttf", 50), fill='white')

        draw.text((320, 200), f"Thấp nhất", font=ImageFont.truetype("times.ttf", 30), fill='white')
        draw.text((335, 240), f"{int(a[3])}℃", font=ImageFont.truetype("times.ttf", 50), fill='white')

        draw.text((550, 200), f"Trung bình", font=ImageFont.truetype("times.ttf", 30), fill='white')
        draw.text((570, 240), f"{int(a[4])}℃", font=ImageFont.truetype("times.ttf", 50), fill='white')
        draw.text(((800 - text_width) // 2, 70), f"{str(a[5])}", font=ImageFont.truetype("times.ttf", 23), fill='white')
        draw.line((50, 320, 800, 320), fill=(255, 255, 255))

        draw.text((50, 380), f"MT mọc: {b[0]}", font=font, fill='white')
        draw.text((425, 380), f"MT lặn: {b[1]}", font=font, fill='white')
        draw.text((50, 450), f"Tốc độ gió: {a[6]} km/h", font=font, fill='white')
        draw.text((425, 450), f"Tổng lượng mưa {a[7]} mm", font=font, fill='white')
        draw.text((425, 530), f"Tầm nhìn : {a[8]} km", font=font, fill='white')
        draw.text((50, 530), f"Độ ẩm: {a[9]} %", font=font, fill='white')
        draw.text((50, 600), f"Chỉ số UV: {a[10]}", font=font, fill='white')
        file_image = f"F:/chatbot/image/{send_id}_{namecity}_{time}.png"
        background.save(file_image)
        return file_image

def image_hour(a, namecity,send_id,time):
    background = Image.open(check_background(a))
    # Tải ảnh từ đường dẫn và chuyển đổi thành định dạng Image
    response = requests.get("https:" + a[11])
    img1 = Image.open(BytesIO(response.content))
    img = img1.convert('RGBA')

    background.paste(img, (360, 180))
    draw = ImageDraw.Draw(background)

    font = ImageFont.truetype("times.ttf", 28)
    text_width, text_height = draw.textbbox((0, 0), a[4], font=font)[2:]
    draw.text((340, 50), f"{str(namecity.upper())}", font=ImageFont.truetype("times.ttf", 40), fill='white')
    draw.text((25, 50), f"{a[1]}", font=ImageFont.truetype("times.ttf", 25), fill='white')
    draw.text(((800 - text_width) // 2, 120), f"{str(a[4])}", font=ImageFont.truetype("times.ttf", 23), fill='white')
    draw.text((350, 260),f"{a[2]}℃" , font=ImageFont.truetype("times.ttf", 40), fill='white')

    draw.line((0, 350, 800, 350), fill=(255, 255, 255))

    draw.text((60, 450), f"Tốc độ gió: {a[5]} km/h", font=font, fill='white')
    draw.text((425, 450), f"Độ ẩm: {a[6]} %", font=font, fill='white')
    draw.text((425, 600), f"Tầm nhìn : {a[7]} km", font=font, fill='white')

    draw.text((60, 600), f"Chỉ số UV: {a[8]}", font=font, fill='white')
    draw.text((60, 530), f"Khả năng mưa: {a[9]} %", font=font, fill='white')
    draw.text((425, 530), f"Lượng mưa: {a[10]} mm", font=font, fill='white')
    file_image = f"F:/chatbot/image/{send_id}_{namecity}_{time}.png"
    background.save(file_image)
    return file_image
def Bieudo(list_max,list_min,x_labels ,namecity,send_id,time):

    # Thiết lập trục x là ngày trong tuần từ thứ 2 đến chủ nhật
    fig, ax = plt.subplots(figsize=(9, 9))
    # Vẽ biểu đồ nhiệt độ tối đa và tối thiểu
    ax.plot(list_max, 'r', label='Max')
    ax.plot(list_min, 'b', label='Min')

    # Thêm tiêu đề và nhãn trục
    plt.title(f"Biểu đồ nhiệt tại {namecity}")
    plt.xlabel('Ngày')
    plt.ylabel('Nhiệt độ (°C)')

    # Thiết lập giới hạn trục y
    plt.ylim(min(list_min)-10, max(list_max)+10)

    # Thêm nhãn trục x
    plt.xticks(range(len(x_labels)), x_labels)

    # Thêm chú thích
    plt.legend(loc='upper right')

    # Thêm nhiệt độ vào mỗi điểm trên biểu đồ
    for i, temp_max in enumerate(list_max):
        plt.text(i, temp_max, str(temp_max) + '°', ha='center', va='bottom', color='red',fontsize=16)
    for i, temp_min in enumerate(list_min):
        plt.text(i, temp_min, str(temp_min) + '°', ha='center', va='top', color='blue',fontsize=16)
    file_image = f"F:/chatbot/bieudo/{send_id}_{namecity}_{time}.png"
    plt.savefig(file_image)
    return file_image

