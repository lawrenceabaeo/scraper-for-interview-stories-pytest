########################################
# Requires pytest to run properly
########################################

import logging

from selenium import webdriver

import config_file
from helper import Helper
import login
import working_at_page
import home_page
import interview_questions_page
import webapp


class TestClassForPyTest():
    
    # Using classic xUnit style setup/teardown with PyTest
    def setup_method(self):
        # Logging level
        logging.basicConfig(level=logging.INFO) # Use ERROR instead of INFO if
                                                # you don't want info printed.
        
        # Driver
        # NOTE: Selenium on Chrome detected/blocked IMMEDIATELY 
        # by the website I tried scraping, so I'm using Firefox
        firefox_driver_path = config_file.path_to_firefox_driver
        self.driver = webdriver.Firefox(executable_path=firefox_driver_path)

        # Company
        self.company_name = "Wally World" # <- change here or use command line 
                                          #    arg --company="Your Company"
        
        # Location (NOTE: Sometimes location doesn't matter)
        self.location = "New York, NY (US)" # <- change here or use command line
                                            #    arg --location="The Location"
        
        # Website user email/pass
        self.email = config_file.email
        self.passw = config_file.password

        # Test completion flag
        self.test_completed = False

    def teardown_method(self):
        logging.info(" At tearDown!")
        if (self.test_completed == True):
            logging.info("Destroying entire instance of driver")
            self.driver.quit()
        else:
            logging.info(" Something happened. Keeping driver open.")

    def test_get_interviews_questions(self, company, location): 
        # The function parameters 'company' and 'location' are pytest fixtures. 
        # These fixtures take values from command line and return them. 
        # If any command line args then overwrite setup_method variables.
        # Ex: c:> pytest -s --company="IBM" --location="San Jose, CA (US)"
        if (company != ""):
            logging.info(" company from command line: " + company)
            self.company_name = company
        
        if (location != ""):
            logging.info(" location from command line: " + location)
            self.location = location

        driver = self.driver

        # Home page
        home_pg = home_page.HomePageObject(driver)
        home_pg.go_to_website_homepage()

        # Login
        login_object = login.LoginObject(driver)
        login_object.login_with_valid_user_and_pass(self.email, self.passw)

        # Search for company from home page
        home_pg.from_homepage_search_for(self.location, self.company_name)

        # Check landing page
        webapp.WebApp.check_resulting_landing_page(driver, self.location, 
        	                                       self.company_name)

        # Company page
        company_page = working_at_page.WorkingAtPageObject(driver)
        company_page.verify_on_working_at_page() 

        # ^check if any interviews content
        number_of_interviews_text = company_page.text_for_number_of_interviews()
        if (number_of_interviews_text == "--"):
            logging.info(" found '--', meaning NO interviews")
            logging.info(" exiting automation")
            return
        
        # ^navigate to interviews page
        company_page.navigate_to_interviews_from_company_page()

        # Interview page
        # ^get interviews and write to file
        interview_questions_pg = \
            interview_questions_page.InterviewQuestionsPageObject(driver)
        interview_questions_pg.get_interviews_and_write_them_to_a_file()
        
        # Completion flag
        self.test_completed = True

