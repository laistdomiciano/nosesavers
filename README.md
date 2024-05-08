# NoseSavers
This in an app that will save your nose from pollens!

<<<<<<< HEAD

# Program Walkthrough

## Welcome Screen: 
When opening the app, users are greeted with a welcome screen with info of the service
Function: welcome_screen

## Subscription: 
User is asked to subscribe to the service by providing their phone number

## Location Input: 
Users are asked to input their current location

## Plant Selection: 
Users have the choice to select the type of plants they want to receive pollen info about - One, two, all of them? That’s their option

## API Request: 
Based on the previous information, the app sends a request to the API

## SMS Alert:
The app processes the data and extract the pollen information of the selected plant types, which is sent to the user’s phone via SMS alert
Functions:
create_message and send_sms

# Guidelines
To run the app you need to import Request library (pip install requests)

# Authors 
Ibrahim - blvlblbl
Maria -
Laís - 
=======
# Requirements:
You need to run the following commands in the terminal:
$ pip install requests
$ pip install uuid
$ pip install datetime 

# How to Run NoseSaver:
$ git clone https://github.com/laistdomiciano/nosesavers
$ cd nosesavers
$ python3 main.py



The pollen forecast is based on the European 11-kilometre air quality forecast from CAMS and the global 40-kilometre atmospheric composition forecast from CAMS. The European and global ranges are not coupled and may show different forecasts.

![Code_1.png](..%2F..%2F..%2FDownloads%2FCode_1.png)
