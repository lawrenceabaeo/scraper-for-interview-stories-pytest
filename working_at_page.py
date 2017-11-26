import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import popup
import overlay
from helper import Helper


class WorkingAtPageObject():

    def __init__(self, driver):
        self.driver = driver

    def navigate_to_interviews_from_company_page(self):
        # This is just a wrapper to group 
        # a sequence of functions together.
        # This function assumes user is already logged in. 

        self.click_on_interviews_link()

        # ^close any popup
        popup_object = popup.PopupObject(self.driver)
        popup_object.check_and_close_any_popups()

        # ^close any ovelay
        # Don't really need this, because
        # Not-logged-in users see a sign-up/login/upsell overlay
        # when clicking the interviews link
        overlay_object = overlay.OverlayObject(self.driver)
        overlay_object.check_and_close_any_overlay()

        Helper.sleep_to(3)

    def verify_on_working_at_page(self):
        # August 25, 2017 - This is a fragile function, 
        # the website uses different titles
        logging.info(" checking if on a company review page")
        if (self.on_working_at_page() == False):
            raise Exception("NOT on Company Reviews page! Expected to be on Company Reviews page!")

    def text_for_number_of_interviews(self):
        # NOTE: the website doesn't always use numbers, sometimes it's like 1.5k
        # NOTE: the website displays '--' to represent '0',
        # will NOT convert to 0, will leave as is 
        # and let the calling function handle '--'
        css_for_number_of_interviews = "a.interviews span.num"
        interview_number_text = self.driver.find_element_by_css_selector(css_for_number_of_interviews).text
        logging.info(" interview number displayed is: " + interview_number_text)
        if (interview_number_text == "--"):
            logging.info(" '--' means that NO interviews were returned for this search!")
        return interview_number_text

    def on_working_at_page(self):
        #NOTE: This is a long function because there are two different titles
        try:
            expected_title = "Working at"
            wait_time = 10 # Keep at 10, sometimes it takes a while
            WebDriverWait(self.driver, wait_time) \
                .until(expected_conditions.title_contains(expected_title))
            logging.info(" title of current page: " + self.driver.title)
            logging.info(" on a company review page")
            return True
        except TimeoutException:
            try: 
                expected_title = "Pay & Benefits"
                wait_time = 5 
                WebDriverWait(self.driver, wait_time) \
                    .until(expected_conditions.title_contains(expected_title))
                logging.info(" title of current page: " + self.driver.title)
                logging.info(" on a company review page")
                return True
            except TimeoutException: 
                logging.info(" NOT on a company review page")
                logging.info(" title of current page: " + self.driver.title)
                return False

    def verify_on_this_specific_company_page(self, company_text):
        logging.info(" checking if on the '" + company_text + "' company page")
        wait_seconds_company_h1 = 10 
        # NEED TO SOLVE FOR a company with apostrophe in it, for now
        # just use what's below
        css_for_company_h1 = "h1.strong.tightAll" # This has differed in the past
        WebDriverWait(self.driver, wait_seconds_company_h1) \
            .until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, css_for_company_h1)))
        company_h1 = self.driver.find_element_by_css_selector(css_for_company_h1)

    def click_on_interviews_link(self):
        # NOTE: popup sometimes occurs for not-logged-in users, 
        # but this script assumes the user is logged-in.
        # NOTE: The interviews 'link' is really just an element that 
        # javascript attaches to, and that js makes the element click-able
        Helper.sleep_to(3, "because selenium is faster than this website's js handler attachments")
        # and I don't feel like implementing polling here
        css_for_company_interviews = "a.eiCell.cell.interviews"
        WebDriverWait(self.driver, 5) \
            .until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, css_for_company_interviews)))
        
        logging.info(" clicking 'Interviews' sub-heading")
        company_interviews_link = self.driver.find_element_by_css_selector(css_for_company_interviews)
        company_interviews_link.click()
        Helper.sleep_to(6)

