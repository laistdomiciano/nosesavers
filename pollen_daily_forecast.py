import json
import requests
from datetime import date


REQUEST_URL = 'https://air-quality-api.open-meteo.com/v1/air-quality?latitude=52.52&longitude=13.41&start_date=2024-05-06&end_date=2024-05-06&hourly='
LOCATION_RQ_URL = 'https://api.mapbox.com/geocoding/v5/mapbox.places/__enter__location__here__.json?limit=1&access_token=pk.eyJ1Ijoic2F2a292aWNsYXphcjEiLCJhIjoiY2xoNm05ODE4MDY0bzNwcGc1ZTVrcHBucyJ9.ThvLS1wl4OM-Ahpbi5Wmew'

def display_plant_options():
    print("""Please select one or more plants to which you are allergic from the following list: 
Alder
Birch
Grass
Mugwort
Olive
Ragweed
""")


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

    global LOCATION_RQ_URL

    for user_data in USERS_DATA:
        if user_data["user_name"][0] == "Martin" and "__enter__location__here__" in LOCATION_RQ_URL: #  # I need to modify this to check for the id not a single name
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

    # print(res['hourly'])
    return res['hourly']


def get_user_dependant_info():
    """Retrieves pollen data for a number of max 6 types of plants based on user
     selection and writes a JSON file containing the user selection"""
    plants_data = []
    user_dependant_data = []
    while True:
        display_plant_options()
        try:
            plants_no = int(input("For how many plants would you like to get the daily forecast? "))
            if isinstance(plants_no, int) and 0 < plants_no <= 6:
                break
            else:
                print("Please enter a valid integer between 1 and 6.")
        except ValueError as e:
            print("Please enter a valid integer between 1 and 6.")

    plant_choices = ["alder", "birch", "grass", "mugwort", "olive", "ragweed"]
    date = {"date": get_date()}

    for i in range(0, plants_no):
        search_term = input("Please enter a plant name: ")
        while search_term.lower() not in plant_choices:
            search_term = input("Please enter a valid plant name: ")
        search_term = search_term.lower() + "_pollen"
        plants_data.append(get_pollen_info_plant(search_term))
        plants_data.append(date)



    user_dependant_data.append(plants_data)

    with open('user_dependant_pollen_data.json', 'w') as fileobj:
        fileobj.write(json.dumps(user_dependant_data))
    print(f"Successfully printed user-dependant pollen data to file!")


if __name__ == "__main__":
    get_user_dependant_info()




