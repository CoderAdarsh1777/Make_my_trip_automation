from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

class Login:

    def __init__(self, driver):
        self.driver = driver
        self.account_type = (By.XPATH, "//li[@data-acctype='personal']")
        self.county_dropdown = (By.XPATH, "//p[@class='makeFlex hrtlCenter flagCountryCode']")
        self.country_code = (By.XPATH, "//input[@placeholder='Country Name or Code']")
        self.country_name_dropdown = (By.XPATH, "//div[@class='li makeFlex hrtlCenter font12']/span[2]")
        self.mobile_number = (By.XPATH, "//input[@placeholder='Enter Mobile Number']")
        self.countinue_button = (By.XPATH, "//button[@class='capText font16']")
        self.otp_box = (By.CSS_SELECTOR, "#otp")
        self.login_btn = (By.XPATH, "//div[@class='btnContainer appendBottom25']/button")
        self.pop_up_close = (By.XPATH, "//span[@class='cstmModal__close']")
        self.email_image = (By.XPATH, "//img[@class='appendLeft15 mousePointer signInByEmailButton']")
        self.email_box = (By.XPATH, "//input[@placeholder='Enter Email Address']")
        self.email_continue_button = (By.XPATH, "//button[@class='capText font16']")
    
    def handle_otp(self):
        wait = WebDriverWait(self.driver, 30)
        otp_input = wait.until(expected_conditions.presence_of_element_located(self.otp_box))
        otp_value = input("Enter the otp received in phone: ")
        otp_input.send_keys(otp_value)

    def login_by_mobile_number(self, firstthreeletterofcountry, countrytoselect, mobilenumber):
        wait = WebDriverWait(self.driver, 20)
        wait.until(expected_conditions.element_to_be_clickable(self.account_type)).click()
        wait.until(expected_conditions.presence_of_element_located(self.county_dropdown)).click()
        wait.until(expected_conditions.presence_of_element_located(self.country_code)).send_keys(firstthreeletterofcountry)
        country_names = self.driver.find_elements(*self.country_name_dropdown)
        for country in country_names:
            full_text = country.text.strip()
            only_name = full_text.split(" (")[0].strip()
            if only_name == countrytoselect:
                country.click()
                break
        self.driver.find_element(*self.mobile_number).send_keys(mobilenumber)
        self.driver.find_element(*self.countinue_button).click()
        # element = self.driver.find_element(*self.countinue_button)
        # self.driver.execute_script("arguments[0].click();", element)
        self.handle_otp()
        time.sleep(5)
        wait.until(expected_conditions.element_to_be_clickable(self.login_btn)).click()
        wait.until(expected_conditions.presence_of_element_located(self.pop_up_close)).click()
    
    def login_by_email(self, emailid):
        wait = WebDriverWait(self.driver, 20)
        wait.until(expected_conditions.element_to_be_clickable(self.account_type)).click()
        wait.until(expected_conditions.presence_of_element_located(self.email_image)).click()
        wait.until(expected_conditions.presence_of_element_located(self.email_box)).send_keys(emailid)
        wait.until(expected_conditions.element_to_be_clickable(self.email_continue_button)).click()

