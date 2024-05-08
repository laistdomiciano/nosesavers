import json
import requests

BASE_URL = 'https://43l848.api.infobip.com'
AUTHORIZATION = 'App 3dec643d54c66b6fab8fbfcce32f8081-27aba670-39dd-40be-8371-0f5acd088797'
SEND_SMS_URL = '/sms/2/text/advanced'

"""Reads json file"""
with open('user_dependant_pollen_data.json', 'r') as file:
        data = json.load(file)

data = data


def create_pollen_alert_message():
    """ Creates the message with data from database"""

    global data

    messages = []

    for entry in data:
        user_name = entry['user_name'][0]
        location = entry['location']
        date = entry['date']

        message = f"🌼 Pollen Alert! 🌼\n\nHey {user_name},\nYou are in {location}.\nThe pollen forecast for {date} indicates:"

        for i in range(len(entry['plants_data'])):
            message = f"{entry['plants_data'][i]['plant_name']}, with a maximum value of {entry['plants_data'][i]['max_pollen_value']} at {{entry['plants_data'][i]['equivalent_time']}}), "
            messages.append(message)
        message = "Time to close the windows"
        messages.append(message)

    return messages


def get_phone_numbers():
    """Get phone numbers from database"""

    global data

    phone_numbers = []
    for entry in data:
        phone_numbers.append(entry["phone_number"])
    return phone_numbers

def send_sms(phone_numbers, messages):
    """Sends sms with API"""

    for message in messages:
        for phone_number in phone_numbers:
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

# messages = create_pollen_alert_message()
# phone_numbers = get_phone_numbers()
# response = send_sms(phone_numbers, messages)

