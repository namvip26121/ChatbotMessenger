# import os
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from googleapiclient.http import MediaFileUpload
#
# # Xác thực với Google Drive API
# creds = Credentials.from_authorized_user_file('F:/pythonProject/venv/credentials.json', ['https://www.googleapis.com/auth/drive'])
#
# # Tạo một service object để giao tiếp với API
# service = build('drive', 'v3', credentials=creds)
#
# # Tên tệp tin bạn muốn tải lên
# file_name = 'example.jpg'
#
# # Đường dẫn tới tệp tin trên ổ đĩa của bạn
# file_path = 'F:/a.jpg'
#
# # Tạo một MediaFileUpload object với tệp tin bạn muốn tải lên
# file_metadata = {'name': file_name}
# media = MediaFileUpload(file_path, resumable=True)
#
# # Gửi yêu cầu API để tải lên tệp tin
# file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#
# # In ra ID của tệp tin vừa được tải lên
# print('File ID: %s' % file.get('id'))


def Bieudo(list_max,list_min,x_labels):
    import matplotlib.pyplot as plt

    # Vẽ biểu đồ nhiệt độ tối đa và tối thiểu
    plt.plot(list_max, 'r', label='Max')
    plt.plot(list_min, 'b', label='Min')

    # Thêm tiêu đề và nhãn trục
    plt.title('Weekly Temperature')
    plt.xlabel('Day of Week')
    plt.ylabel('Temperature (°C)')

    # Thiết lập giới hạn trục y
    plt.ylim(0, max(list_max))

    # Thêm nhãn trục x
    plt.xticks(range(len(x_labels)), x_labels)

    # Thêm chú thích
    plt.legend(loc='upper right')

    # Thêm nhiệt độ vào mỗi điểm trên biểu đồ
    for i, temp_max in enumerate(list_max):
        plt.text(i, temp_max, str(temp_max) + '°', ha='center', va='bottom', color='red')
    for i, temp_min in enumerate(list_min):
        plt.text(i, temp_min, str(temp_min) + '°', ha='center', va='top', color='blue')

    # Hiển thị biểu đồ
    plt.show()