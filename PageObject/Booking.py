import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from datetime import datetime
import time
from Utils.commonmethods import common

class Booking:

    def __init__(self, driver):
        self.driver = driver
        self.simops = common(self.driver)
        self.wait = WebDriverWait(self.driver, 20)
        self.flight_icon = (By.XPATH, "//li[@class='menu_Flights']")
        self.one_way = (By.XPATH, "//li[@data-cy='oneWayTrip']")
        self.round_trip = (By.XPATH, "//li[@data-cy='roundTrip']")
        self.multicity = (By.XPATH, "//li[@data-cy='mulitiCityTrip']")
        self.from_city_xpath = (By.CSS_SELECTOR, "#fromCity")
        self.from_city_textbox = (By.XPATH, "//input[@placeholder='From']")
        self.from_city_list = (By.XPATH, "//ul[@class='react-autosuggest__suggestions-list']/li/div/div/p/span/span")
        self.to_city_xpath = (By.CSS_SELECTOR, "#toCity")
        self.to_city_textbox = (By.XPATH, "//input[@placeholder='To']")
        self.departure_date = (By.XPATH, "//p[@data-cy='departureDate']")
        self.return_date = (By.XPATH, "//p[@data-cy='returnDate']")
        self.next_btn = (By.XPATH, "//span[@aria-label='Next Month']")
        self.number_of_traveller = (By.XPATH, "//label[@for='travellers']")
        self.traveller_apply = (By.XPATH, "//button[@data-cy='travellerApplyBtn']")
        self.search_button = (By.XPATH, "//p[@data-cy='submit']/a")
        self.flight_name = (By.XPATH, "//p[@class='boldFont blackText airlineName']")
        self.flight_codes = (By.XPATH, "//p[@class='fliCode']")
        self.flights_departure_time = (By.XPATH, "//div[@class='flexOne timeInfoLeft']/p[1]/span")
        self.flights_arrival_time = (By.XPATH, "//div[@class='flexOne timeInfoRight']/p[1]/span")
        self.flight_onboarding_location = (By.XPATH, "//div[@class='flexOne timeInfoLeft']/p[2]/font")
        self.flight_deboarding_location = (By.XPATH, "//div[@class='flexOne timeInfoRight']/p[2]/font")
        self.flight_fare_details = (By.XPATH, "//div[@data-test='component-fare']/span")
        self.total_flight_time = (By.XPATH, "//div[@class='stop-info flexOne']/p")
        self.flight_stops = (By.XPATH, "//p[@class='flightsLayoverInfo']")
    
    def count_of_traveller(self, number_of_adult_traveller, number_of_childrens_travellers, number_of_infants, Travel_class):
        self.driver.find_element(*self.number_of_traveller).click()
        self.driver.find_element(By.XPATH, f"//li[@data-cy='adults-{number_of_adult_traveller}']").click()
        self.driver.find_element(By.XPATH, f"//li[@data-cy='children-{number_of_childrens_travellers}']").click()
        self.driver.find_element(By.XPATH, f"//li[@data-cy='infants-{number_of_infants}']").click()
        # for class_type, class_value in Travel_class.items():
        #     if class_value == "1":
        #         self.driver.find_element(By.XPATH, f"//ul[@class='guestCounter classSelect font12 darkText']/li[text()='{class_type}']").click()
        self.driver.find_element(*self.traveller_apply).click()
    
    def from_city(self, cityname):
        self.driver.find_element(*self.from_city_xpath).click()
        self.driver.find_element(*self.from_city_textbox).send_keys(cityname)
        cityavailable = self.driver.find_elements(*self.from_city_list)
        for item in cityavailable:
            if item.text == cityname:
                item.click()
                break
    
    def to_city(self, cityname):
        self.driver.find_element(*self.to_city_xpath).click()
        self.driver.find_element(*self.to_city_textbox).send_keys(cityname)
        cityavailable = self.driver.find_elements(*self.from_city_list)
        for item in cityavailable:
            if item.text == cityname:
                item.click()
                break
    
    def convert_to_aria_label(self, date_str):
        date_obj = datetime.strptime(date_str, "%d %b %Y")
        weekday = date_obj.strftime("%a")
        return date_obj.strftime(f"{weekday} %b %d %Y")

    def select_date(self, final_label):
        date_xpath = f"//div[contains(@class,'DayPicker-Day') and @aria-label='{final_label}']"

        while True:
            try:
                element = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, date_xpath)))
                self.driver.execute_script("arguments[0].click();", element)
                break
            except:
                self.driver.find_element(*self.next_btn).click()
    
    def date_selector_for_trips(self, type_of_trip, departure_date, return_date):

        if type_of_trip == "One_way":
            date_feild = self.driver.find_element(*self.departure_date)
            self.driver.execute_script("arguments[0].click();", date_feild)   
            departure_label = self.convert_to_aria_label(departure_date)
            self.select_date(departure_label)
        
        elif type_of_trip == "Round_trip":
            date_feild = self.driver.find_element(*self.departure_date)
            self.driver.execute_script("arguments[0].click();", date_feild) 

            dep_date = self.convert_to_aria_label(departure_date) 
            xpath = f"//div[contains(@aria-label,'{dep_date}')]//div[@class='dateInnerCell']"
            ele = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].click();", ele)

            ret_date = self.convert_to_aria_label(return_date)
            xpath = f"//div[contains(@aria-label,'{ret_date}')]//div[@class='dateInnerCell']"
            ele = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].click();", ele)
    
    def slow_scroll_to_bottom(self):
        last_height = 0
        while True:
            self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
    def Booking_for_travel(self, type_of_trip, from_city_name, to_city_name, departure_date, return_date,number_of_adult_traveller, number_of_childrens_travellers, number_of_infants, Travel_class, customer_type):
        # wait = WebDriverWait(self.driver, 15)
        time.sleep(2)
        self.simops.remove_all_blockers()  # Should be removed once the login system is active
        time.sleep(5)
        try:
            self.driver.find_element(By.XPATH, "//span[@class='coachmark']").click()
        except:
            pass
        # wait.until(expected_conditions.element_to_be_clickable(self.flight_icon)).click()
        if type_of_trip == "One_way":
            self.driver.find_element(*self.one_way).click()
            self.simops.remove_overlays()
            self.from_city(from_city_name)
            self.to_city(to_city_name)
            self.date_selector_for_trips(type_of_trip, departure_date, return_date=None)
            time.sleep(2)
            self.count_of_traveller(number_of_adult_traveller, number_of_childrens_travellers, number_of_infants, Travel_class)
        elif type_of_trip == "Round_trip":
            self.driver.find_element(*self.round_trip).click()
            self.simops.remove_overlays()
            self.from_city(from_city_name)
            self.to_city(to_city_name)
            self.date_selector_for_trips(type_of_trip, departure_date, return_date)
            time.sleep(5)
            self.count_of_traveller(number_of_adult_traveller, number_of_childrens_travellers, number_of_infants)
        elif type_of_trip == "Multicity":
            self.driver.find_element(*self.multicity).click()
        for cust_type, select in customer_type.items():
            if select == "1":
                try:
                    self.wait.until_not(expected_conditions.presence_of_element_located((By.CLASS_NAME, "hsBackDrop")))
                except:
                    pass
                element = self.driver.find_element(By.XPATH, f"//div[@class='fareCardItem']/div/div[1][text()='{cust_type}']")
                self.driver.execute_script("arguments[0].click();", element)
        self.driver.find_element(*self.search_button).click()
        time.sleep(5)
        try:
            self.driver.find_element(By.XPATH, "//button[@class='okayButton fontSize16']").click()
        except:
            pass
        time.sleep(5)
        self.slow_scroll_to_bottom()
        flight_names = self.wait.until(expected_conditions.presence_of_all_elements_located(self.flight_name))
        flight_codes = self.driver.find_elements(*self.flight_codes)
        flight_departure_times = self.driver.find_elements(*self.flights_departure_time)
        flight_arrival_times = self.driver.find_elements(*self.flights_arrival_time)
        flight_departure_locations = self.driver.find_elements(*self.flight_onboarding_location)
        flight_arrival_locations = self.driver.find_elements(*self.flight_deboarding_location)
        flight_time = self.driver.find_elements(*self.total_flight_time)
        flight_fares = self.driver.find_elements(*self.flight_fare_details)
        flight_stops = self.driver.find_elements(*self.flight_stops)

        if flight_names is None:
            print("No flights available for the selected route and dates.")
        else:
            for name, code, dep_time, arr_time, dep_loc, arr_loc, flight_time, flight_stops, fare in zip(flight_names, flight_codes, flight_departure_times, flight_arrival_times, flight_departure_locations, flight_arrival_locations, flight_time, flight_stops, flight_fares):
                print(f"Flight Name: {name.text}, Flight Code: {code.text}, Departure Time: {dep_time.text}, Arrival Time: {arr_time.text}, Departure Location: {dep_loc.text}, Arrival Location: {arr_loc.text}, Total Flight Time: {flight_time.text}, Stops: {flight_stops.text}, Fare: {fare.text}")