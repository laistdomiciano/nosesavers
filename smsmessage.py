import json
import requests

BASE_URL = 'https://43l848.api.infobip.com'
AUTHORIZATION = 'App 3dec643d54c66b6fab8fbfcce32f8081-27aba670-39dd-40be-8371-0f5acd088797'
SEND_SMS_URL = '/sms/2/text/advanced'

def create_message(location, pollen_type):
    return f"🌼 Pollen Alert! 🌼\n\n Hey {user_name} You are in {location} and in this location you will get pollen from {pollen_type} trees."

def send_sms(phone_number, message):
    try:
        assert len(str(phone_number)) > 5, 'Destination phone number must be at least 6 digits long'
        assert message != '', 'Message text cannot be empty'
        url = BASE_URL + SEND_SMS_URL
        request_headers = {
            'Authorization': AUTHORIZATION,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        payload = json.dumps({
            'messages': [
                {
                    'destinations': [
                        {
                            'to': phone_number
                        }
                    ],
                    'from': 'NoseSaver',
                    'text': message
                }
            ]
        })
        response = requests.post(url, data=payload, headers=request_headers)
        response_data = response.json()
        print("The message was sent", response_data)
        return response_data
    except Exception as e:
        print(f'An error occurred while attempting to send SMS message to "{phone_number}" (message: "{message}"). \nError: {e}')
        return None

user_name = 'John'
location = 'Germany'
pollen_type = 'oak'
message = create_message(location, pollen_type)
phone_number = '491734508014'
response = send_sms(phone_number, message)

