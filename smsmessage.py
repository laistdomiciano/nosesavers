import json
import requests

BASE_URL = 'https://43l848.api.infobip.com'
AUTHORIZATION = 'App 3dec643d54c66b6fab8fbfcce32f8081-27aba670-39dd-40be-8371-0f5acd088797'
SEND_SMS_URL = '/sms/2/text/advanced'

"""Reads json file"""
with open('user_dependant_pollen_data.json', 'r') as file:
        data = json.load(file)

def create_pollen_alert_message(data):
    """ Creates the message with data from database"""
    messages = []

    for entry in data:
        user_names = entry['user_name']
        location = entry['location']
        date = entry['date']

        for plant_data in entry['plants_data']:
            pollen_type = ''
            max_pollen_value = 0.0

            if 'ragweed_pollen' in plant_data:
                pollen_type = 'ragweed'
                max_pollen_value = max(plant_data['ragweed_pollen'])
            elif 'birch_pollen' in plant_data:
                pollen_type = 'birch'
                max_pollen_value = max(plant_data['birch_pollen'])
            elif 'alder_pollen' in plant_data:
                pollen_type = 'alder'
                max_pollen_value = max(plant_data['alder_pollen'])
            elif 'mugwort_pollen' in plant_data:
                pollen_type = 'mugwort'
                max_pollen_value = max(plant_data['mugwort_pollen'])
            elif 'grass_pollen' in plant_data:
                pollen_type = 'grass'
                max_pollen_value = max(plant_data['grass_pollen'])

            message = f"🌼 Pollen Alert! 🌼\n\nHey {', '.join(user_names)},\nYou are in {location}.\nThe pollen forecast for {date} indicates {pollen_type} pollen, with a maximum value of {max_pollen_value}. Time to close the windows"
            messages.append(message)

    return messages

def get_phone_numbers(data):
    """Get phone numbers from database"""
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

messages = create_pollen_alert_message(data)
phone_numbers = get_phone_numbers(data)
response = send_sms(phone_numbers, messages)

