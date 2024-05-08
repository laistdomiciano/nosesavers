from crud_database import *
from welcome_message import welcome_message
from pollen_daily_forecast import get_user_dependant_info, get_info_database
from smsmessage import *
import sys


USERS_DATA = get_info_database()


def show_options_for_user():
    print()
    print("""\u001b[36mIf you are a new subscriber please select 1 to register.
If not please select one of the available options:
1. Create an account 
2. Update subscription
3. Delete my account
q. To exit the program\u001b[0m
""")


def sms_choice():
    """Send SMSs to single or multiple users"""
    print("""\u001b[42m\u001b[47mIf you want to send a SMS alert:
L/l to send a message to the \u001b[1mLast subscriber
W/w to send a message to the \u001b[1mWhole database\u001b[0m\u001b[0m
""")
    send_sms_choice = input("Please select L or W: ")
    if send_sms_choice == "W":
        get_user_dependant_info(USERS_DATA)
        messages = create_pollen_alert_message()
        phone_numbers = get_phone_numbers()
        response = send_sms(phone_numbers, messages)
    elif send_sms_choice == "L":
        get_user_dependant_info([USERS_DATA[-1]])
        message = create_pollen_alert_message()
        phone_number = get_phone_numbers()
        response = send_sms(phone_number, message)


def user_selection():
    user_choice = input("Your selection: ")

    if user_choice == "1":
        add_user()
        sms_choice()
    elif user_choice == "2":
        update_user()
    elif user_choice == "3":
        delete_user()
    elif user_choice == "q":
        quit()

    input("Press Enter to continue...")

    while True:
        print()
        user_choice = input('Do you want to select another option (Y/N)?')
        if user_choice == 'Y' or user_choice == 'y':
            show_options_for_user()

            user_choice = input("What do you want to do next: ")
            if user_choice == "1":
                add_user()
                sms_choice()
            elif user_choice == "2":
                update_user()
            elif user_choice == "3":
                delete_user()
            elif user_choice == "q":
                sys.exit()

        elif user_choice == 'N' or user_choice == 'n':
            sys.exit()
        else:
            print('Select Y for Yes or, N for No ')


def main():
    print(f"\u001b[33m\u001b[1m{welcome_message()}\u001b[0m")
    show_options_for_user()
    user_selection()


if __name__ == "__main__":
    main()

