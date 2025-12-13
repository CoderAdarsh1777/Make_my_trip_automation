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
        # self.number_of_traveller = (By.XPATH, "//p[@data-cy='travellerText']")
        self.number_of_traveller = (By.XPATH, "//label[@for='travellers']")
        self.traveller_apply = (By.XPATH, "//button[@data-cy='travellerApplyBtn']")
        self.search_button = (By.XPATH, "//p[@data-cy='submit']/a")
    
    def count_of_traveller(self, number_of_adult_traveller, number_of_childrens_travellers, number_of_infants):
        self.driver.find_element(*self.number_of_traveller).click()
        self.driver.find_element(By.XPATH, f"//li[@data-cy='adults-{number_of_adult_traveller}']").click()
        self.driver.find_element(By.XPATH, f"//li[@data-cy='children-{number_of_childrens_travellers}']").click()
        self.driver.find_element(By.XPATH, f"//li[@data-cy='infants-{number_of_infants}']").click()
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
    
    # def date_selector_for_trips(self, type_of_trip, departure_date, return_date):

    #     if type_of_trip == "One_way":
    #         date_feild = self.driver.find_element(*self.departure_date)
    #         self.driver.execute_script("arguments[0].click();", date_feild)   
    #         departure_label = self.convert_to_aria_label(departure_date)
    #         self.select_date(departure_label)
        
    #     elif type_of_trip == "Round_trip":
    #         date_feild = self.driver.find_element(*self.departure_date)
    #         self.driver.execute_script("arguments[0].click();", date_feild) 

    #         dep_date = self.convert_to_aria_label(departure_date) 
    #         xpath = f"//div[contains(@aria-label,'{dep_date}')]//div[@class='dateInnerCell']"
    #         ele = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, xpath)))
    #         self.driver.execute_script("arguments[0].click();", ele)

    #         ret_date = self.convert_to_aria_label(return_date)
    #         xpath = f"//div[contains(@aria-label,'{ret_date}')]//div[@class='dateInnerCell']"
    #         ele = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, xpath)))
    #         self.driver.execute_script("arguments[0].click();", ele)

    def date_selector_for_trips(self, type_of_trip, departure_date, return_date):

        # Open the calendar in all cases
        date_field = self.driver.find_element(*self.departure_date)
        self.driver.execute_script("arguments[0].click();", date_field)

        if type_of_trip == "One_way":
            dep_label = self.convert_to_aria_label(departure_date)
            self.select_date(dep_label)

        elif type_of_trip == "Round_trip":
            dep_label = self.convert_to_aria_label(departure_date)
            self.select_date(dep_label)

            ret_label = self.convert_to_aria_label(return_date)
            self.select_date(ret_label)

            # IMPORTANT: wait for the calendar overlay to go away
            self.wait.until(
                expected_conditions.invisibility_of_element_located(
                    (By.CSS_SELECTOR, "div.DayPicker-Months")
                )
            )
            
    def Booking_for_travel(self, type_of_trip, from_city_name, to_city_name, departure_date, return_date,number_of_adult_traveller, number_of_childrens_travellers, number_of_infants):
        # wait = WebDriverWait(self.driver, 15)
        time.sleep(2)
        self.simops.remove_all_blockers()  # Should be removed once the login system is active
        # wait.until(expected_conditions.element_to_be_clickable(self.flight_icon)).click()
        if type_of_trip == "One_way":
            self.driver.find_element(*self.one_way).click()
            self.simops.remove_overlays()
            self.from_city(from_city_name)
            self.to_city(to_city_name)
            self.date_selector_for_trips(type_of_trip, departure_date, return_date=None)
            time.sleep(2)
            self.count_of_traveller(number_of_adult_traveller, number_of_childrens_travellers, number_of_infants)
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
        self.driver.find_element(*self.search_button).click()
        self.simops.remove_all_blockers()
     