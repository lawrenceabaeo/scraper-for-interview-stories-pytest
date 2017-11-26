import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from helper import Helper


class LoginObject():
    def __init__(self, driver):
        self.driver = driver

    def login_with_valid_user_and_pass(self, user_email, user_passw):
        # NOTE: I separated login() from login_submit()
        # in case I wanted to run  login scenarios
        # with a different verification, example invalid password
        self.login_submit(user_email, user_passw)

        # verify if logged in
        logged_in = self.user_is_logged_in()
        assert(logged_in == True)
        logging.info(" verified user was logged in")


    def login_submit(self, user_email, user_passw):
        # NOTE: This does NOT verify the action after submit, 
        # this can be done separately
        logging.info(" starting log in process")
        if (self.user_is_logged_in()) == True:
            logging.info(" user is already logged in! Skipping rest of login function!")
            return

        # click Sign In:
        # 'Sign In' link isn't a link - find_elements_by_link_text will not work 
        logging.info(" clicking sign in link")
        sign_in_link_css = 'li.sign-in a.sign-in'
        sign_in_link = self.driver.find_element_by_css_selector(sign_in_link_css)
        sign_in_link.click()
         
        # Sometimes selenium is faster than the javascript event listener
        # attaching to the 'Sign In' div. When this happens, 
        # selenium clicks on 'Sign In' and nothing happens. This code retries
        # if it doesn't see the email field on the screen. keyword: race condition
        id_for_email_input_field = 'signInUsername'
        attempts_to_see_email_field = 0
        max_attempts_sign_in_click = 4
        logging.info(" checking for email input field")
        while attempts_to_see_email_field < max_attempts_sign_in_click:
            logging.info(" attempt #" + str(attempts_to_see_email_field) + " to see email field")
            try: 
                WebDriverWait(self.driver, 5) \
                    .until(expected_conditions.presence_of_element_located((By.ID, id_for_email_input_field)))
                logging.info(" email input field was found")
            except TimeoutException: 
                if (attempts_to_see_email_field + 1) < max_attempts_sign_in_click:
                    logging.info(" Could NOT see email field. Will click 'Sign In' again.")
                    sign_in_link.click()
                else: 
                    raise Exception("Did NOT see email field! Expected to see email text input field.")
                attempts_to_see_email_field += 1
            else: 
                attempts_to_see_email_field = 5
             
        email_field = self.driver.find_element_by_id('signInUsername')
        email_field.send_keys(user_email)
           
        password_field = self.driver.find_element_by_id("signInPassword")
        password_field.send_keys(user_passw)
            
        #Selenium runs faster than the page rendering the button.
        Helper.sleep_to(6, "to give time for page to render sign in button")
        WebDriverWait(self.driver, 5) \
           .until(expected_conditions.visibility_of_element_located((By.ID, 'signInBtn')))
        logging.info(" clicking sign in button")
        sign_in_button = self.driver.find_element_by_id("signInBtn")
        sign_in_button.click()
        Helper.sleep_to(10, "to let login action run to completion")
     
    def user_is_logged_in(self, seconds_to_wait=10):
        logging.info(" checking if user is logged in.")
        logging.info(" will wait " + str(seconds_to_wait) + " seconds to check related css.")
        profile_css_selector = 'li.signed-in'
        signin_displayed_css_selector = 'li.sign-in a.sign-in'
        try:
            WebDriverWait(self.driver, seconds_to_wait) \
                .until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, profile_css_selector)))
            logging.info(" user is logged in.")
            return True
        except TimeoutException: 
            seconds_to_see_signin = 2
            try: 
                WebDriverWait(self.driver, seconds_to_see_signin) \
                    .until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, signin_displayed_css_selector)))
                logging.info(" user is NOT logged in.")
                return False
            except:
                raise Exception("Did NOT see the css which shows if a user is logged in or not!")
        else: 
            raise Exception

