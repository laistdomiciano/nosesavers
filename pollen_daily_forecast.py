import json
import requests
from datetime import date


REQUEST_URL = 'https://air-quality-api.open-meteo.com/v1/air-quality?latitude=52.52&longitude=13.41&start_date=2024-05-06&end_date=2024-05-06&hourly='
LOCATION_RQ_URL = 'https://api.mapbox.com/geocoding/v5/mapbox.places/__enter__location__here__.json?limit=1&access_token=pk.eyJ1Ijoic2F2a292aWNsYXphcjEiLCJhIjoiY2xoNm05ODE4MDY0bzNwcGc1ZTVrcHBucyJ9.ThvLS1wl4OM-Ahpbi5Wmew'


def get_date():
    today = date.today()
    return str(today)


def get_info_database():
    """Retrieves info from the database"""
    with open("subscribers_database.json", "r") as fileobj:
        users_data_str = fileobj.read()
        users_data = json.loads(users_data_str)
    return users_data


USERS_DATA = get_info_database()


def get_location(USERS_DATA):
    """Receives as parameter the users database and returns the longitude and latitude
    for a particular location the user selected"""

    global LOCATION_RQ_URL
    longitude = 0.0
    latitude = 0.0

    for user_data in USERS_DATA:
        if "__enter__location__here__" in LOCATION_RQ_URL:
            LOCATION_RQ_URL = LOCATION_RQ_URL.replace("__enter__location__here__", user_data["location"])
            location_info = requests.get(LOCATION_RQ_URL)
            res_location = location_info.json()
            longitude = res_location["features"][0]["center"][0]
            latitude = res_location["features"][0]["center"][1]
    # print("Longitude: ", longitude, "\nLatitude", latitude)
    return round(longitude,6), round(latitude,6)


def get_pollen_info_plant(plant_name):
    """Retrieves pollen data for a particular plant"""
    global REQUEST_URL
    global USERS_DATA

    if "2024-05-06" in REQUEST_URL: # Replaces the date in the URL
        REQUEST_URL = REQUEST_URL.replace("2024-05-06", get_date())
    # print("Change date", REQUEST_URL)

    # Replaces the longitude and latitude in the URL with user dependant data
    longitude, latitude = get_location(USERS_DATA)
    if "latitude=" in REQUEST_URL:
        REQUEST_URL = REQUEST_URL.replace("52.52", str(latitude))
    # print("Check change in latitude: ", REQUEST_URL)
    if "longitude=" in REQUEST_URL:
        REQUEST_URL = REQUEST_URL.replace("13.41", str(longitude))
    # print("Check change in longitude: ", REQUEST_URL)

    pollen_info = requests.get(f'{REQUEST_URL}{plant_name}')
    res = pollen_info.json()

    # Retrieves the maximum value for the pollen in the dictionary
    max_pollen_value = max(res['hourly'][plant_name])

    # Retrieves the time at which the max value of the pollen is happening
    time_index = res['hourly'][plant_name].index(max_pollen_value)
    equivalent_time = res['hourly']['time'][time_index][-5:]

    res['hourly']["max_pollen_value"] = max_pollen_value
    res['hourly']["equivalent_time"] = equivalent_time

    if "_" in plant_name:
        plant_name = plant_name.replace("_", " ")
    res['hourly']["plant_name"] = plant_name

    # print(res['hourly'])
    return res['hourly']


def get_user_dependant_info(USERS_DATA):
    """Retrieves pollen data for a number of max 6 types of plants based on user
     selection in the database and writes a JSON file containing the user selection"""

    plants_data = []
    retrieved_user_dependant_data = []


    for i in range(len(USERS_DATA)):
        # print(USERS_DATA[i]["plants_data"])
        for search_term in USERS_DATA[i]["plants_data"]:
            plants_data.append(get_pollen_info_plant(search_term))

    id_user = {}
    for user_data in USERS_DATA:
        user_info = {
            "user_name": user_data["user_name"],
            "phone_number": user_data["phone_number"],
            "location": user_data["location"],
            "date" : get_date(),
            "plants_data": plants_data
        }
        id_user.update(user_info)
        retrieved_user_dependant_data.append(id_user.copy())
    # print(retrieved_user_dependant_data)

    with open('user_dependant_pollen_data.json', 'w') as fileobj:
        fileobj.write(json.dumps(retrieved_user_dependant_data))
    print(f"Successfully printed user-dependant pollen data to file!")


if __name__ == "__main__":
    get_user_dependant_info()




