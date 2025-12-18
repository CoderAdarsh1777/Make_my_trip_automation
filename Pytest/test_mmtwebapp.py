import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PageObject.Login import Login
from PageObject.Booking import Booking
import time
import pytest
import json

test_data_path = os.path.join(os.path.dirname(__file__), "..", "data", "test_mmtwebapp.json")
with open(test_data_path, "r") as f:
    test_data = json.load(f)
    test_list = test_data["data"]

@pytest.mark.parametrize("test_list_item", test_list)
def test_e2e(browserinvoke, test_list_item):
    driver = browserinvoke
    driver.get(test_list_item["link"])

    # Login function

    # logintoweb = Login(driver)

    # choice = input("Which Login meethod do you want to use? (1- Email, 2- Mobile Number): ")
    # if choice == "1":
    #     logintoweb.login_by_email(test_list_item["email"])
    # elif choice == "2":
    #     logintoweb.login_by_mobile_number(test_list_item["firthredig"], test_list_item["country_name"], test_list_item["mobile_number"])
    
    # Booking function

    booking_trip = Booking(driver)
    booking_trip.Booking_for_travel(test_list_item["trip_type"], test_list_item["from_city"], test_list_item["to_city"], test_list_item["departure_date"], test_list_item["return_date"],test_list_item["number_of_adult_traveller"], test_list_item["numer_of_childrens_traveller"], test_list_item["number_of_infants"], test_list_item["Travel_class"],test_list_item["customer_type"])

    time.sleep(5)
