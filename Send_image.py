import requests
import json
PAGE_ACCESS_TOKEN = "EAAJQwAVS4moBAMRQiLZBpJ0qlPrEt5uGimi6DBHGdZAX30OCZA1U7ZAFO1ZB1hqYaZALiBlZB0ZCHzmd4eiWckcotdRjDIfoWnEX5FdXDZBKQqoZA3Rd3ZBPAO6emOASvzthsA3QJO6YU1us3WjovYPu6XaJ1nfXt5Co3hbmDoTHhslEkeoPy44HPCHivZCz0dCBuD7LAbZA3zHWjYQZDZD"
# lấy attachment của ảnh
def layattachment_id(PAGE_ACCESS_TOKEN,file_image) :
    url = 'https://graph.facebook.com/v16.0/me/message_attachments'
    params = {'access_token': PAGE_ACCESS_TOKEN}

    data = {
        'message': '{"attachment":{"type":"image", "payload":{"is_reusable":true}}}',
    }
    files = {
        'filedata': (file_image, open(file_image, 'rb'), 'image/png')
    }

    response = requests.post(url, params=params, data=data, files=files)
    # Lấy attachment_id từ response
    attachment_id = response.json()['attachment_id']
    return attachment_id

# Gửi tin nhắn chứa attachment đã được lưu trữ trên Facebook
def send_image(PAGE_ACCESS_TOKEN,recipient_id,attachment_id):
    response = requests.post(
    'https://graph.facebook.com/v16.0/me/messages',
    params={'access_token': PAGE_ACCESS_TOKEN},
    headers={'Content-Type': 'application/json'},
    data=json.dumps({
        'recipient': {
            'id': recipient_id
        },
        'message': {
            'attachment': {
                'type': 'image',
                'payload': {
                    'attachment_id': attachment_id
                }
            }
        }
    })
    )
    print(response.json())
# Kiểm tra xem tin nhắn đã được gửi thành công hay chưa
    if response.status_code == 200:
        print('Ảnh đã được gửi thành công.')
    else:
        print('Đã có lỗi xảy ra khi gửi ảnh .')


