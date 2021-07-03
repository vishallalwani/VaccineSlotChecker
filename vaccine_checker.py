import requests
from datetime import datetime
import json,time

PINCODE="411041"
SLEEPER=60
min_age_limit=18
sessions_by_pin_7_days = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}"
DD_MM_YYYY = "%d-%m-%y"

    
    
def check_vaccine_availibility():
    response = get_availability_by_pincode(PINCODE,today())
    #print(response)
    if len(response['centers'])>0:
        for center in response['centers']:
            available_sessions =  center['sessions']
            for session in available_sessions:
                if session['available_capacity'] > 0 and session['min_age_limit'] == min_age_limit:
                    print ("Vaccine Available for 18+")
                    print (center)
                else:
                    print("No Vaccine Sessions Available, Retrying in {} seconds".format(SLEEPER))
                    time.sleep(SLEEPER)
                    check_vaccine_availibility()
        
        
        
def get_sessions(url):
    headers = {'Content-type': 'application/json'}
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return e
    return response.json()


def get_availability_by_pincode(pin_code: str, date: str):
    url = sessions_by_pin_7_days.format(pin_code,date)
    return get_sessions(url)


def today():
    return datetime.now().strftime(DD_MM_YYYY)   


check_vaccine_availibility()

