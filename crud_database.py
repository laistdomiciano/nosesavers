import json
import uuid


def read_database():
    """Reads the database"""
    with open("subscribers_database.json", "r") as fileobj:
        subscribers_database = fileobj.read()
    return json.loads(subscribers_database)


USERS_DATABASE = read_database()


def sync_database():
    """Synchronizes the database"""
    updated_database = json.dumps(USERS_DATABASE)
    with open('subscribers_database.json', 'w') as fileobj:
        fileobj.write(updated_database)


def add_user():
    """Adds new entries in the database"""
    while True:
        try:
            user_first_name = input("Please insert your first name: ")
            user_last_name = input("Please insert your last name: ")
            phone_number = input("Please insert a phone number: ")
            if not phone_number.isdigit():
                raise ValueError("Phone number must contain only digits.")
            if len(phone_number) != 13:
                raise ValueError("Please insert a valid phone number.")
            location = input("Please insert a location: ")
            USERS_DATABASE.append({
                "id": str(uuid.uuid4()),
                "user_name": [user_first_name, user_last_name],
                "phone_number": str(phone_number),
                "location": location
            })
            print("User added successfully!")
            break
        except ValueError as e:
            print("Error:", e)
    sync_database()


def update_user():
    """Updates any of the fields in the database based on the user selection"""
    updated = False
    while not updated:
        user_to_be_updated = input("Please select an user to be updated (use last name): ")
        found = False
        for i in range(len(USERS_DATABASE)):
            if USERS_DATABASE[i]["user_name"][1].lower() == user_to_be_updated.lower():
                print("""What would you like to update?
Select one of the options below:
0 for User first name
1 for User last name
2 for User phone number
3 for User user location
""")
                user_choice = int(input("Please select one of the options above: "))
                if user_choice == 0:
                    USERS_DATABASE[i]["user_name"][0] = input("Please enter an update for the first name: ")
                    updated = True
                elif user_choice == 1:
                    USERS_DATABASE[i]["user_name"][1] = input("Please enter an update for the last name: ")
                    updated = True
                elif user_choice == 2:
                    while True:
                        try:
                            phone_number = input("Please enter an update for the phone number: ")
                            if not USERS_DATABASE[i]["phone_number"].isdigit():
                                raise ValueError("Phone number must contain only digits.")
                            if len(USERS_DATABASE[i]["phone_number"]) != 12:
                                raise ValueError("Please insert a valid phone number.")
                            USERS_DATABASE[i]["phone_number"] = phone_number
                            updated = True
                            break
                        except ValueError as e:
                            print("Error:", e)
                elif user_choice == 3:
                    USERS_DATABASE[i]["location"] = input("Please enter an update for the location: ")
                    updated = True
                found = True
                break
            else:
                print("The option is not available")
        if not found:
            print("Error! The user you are trying to update is not part of the database!")

    sync_database()


def delete_user():
    """Deletes entries in the database based on user input (last name selection for user)"""
    while True:
        user_to_be_deleted = input('Please insert the last name of the user you want to delete: ')
        found = False
        for i in range(len(USERS_DATABASE)):
            if USERS_DATABASE[i]["user_name"][1].lower() == user_to_be_deleted.lower():
                del USERS_DATABASE[i]
                print('User deleted successfully.')
                found = True
                break
        if not found:
            print('User not found. Please select a valid user to delete!')
        else:
            break

    sync_database()


def crud_database():
    """Calls the functions in the program"""
    read_database()
    print(read_database())
    add_user()
    update_user()
    delete_user()


if __name__ == "__main__":
    crud_database()