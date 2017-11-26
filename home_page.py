import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import config_file
from helper import Helper


class HomePageObject():
    
    def __init__(self, driver):
        self.driver = driver

    def go_to_website_homepage(self):
        logging.info(" navigating to home page")
        home_page_url = config_file.home_url
        self.driver.get(home_page_url)
        Helper.sleep_to(8)
        
        self.verify_browser_title()

    def from_homepage_search_for(self, location, company_name):
        # This is just a wrapper that groups a sequence of functions
        # together.
        # NOTE: Search results using 'Interviews' tab is not great
        # so search by going to 'Companies & Reviews' first and then 
        # click the 'Interviews tab on the company page'
        # NOTE: UNUSUAL WEBSITE BUSINESS RULE:
        # First time users that select anything other than default 'Jobs'
        # dropdown will launch a new tab, so function closes the extra tab
        logging.info(" company_name is: " + company_name)
        logging.info(" location is: " + location)
        self.click_companies_and_reviews_search_type()
        self.input_this_location(location)
        self.input_this_search_text(company_name)
        self.click_search_button()
        self.close_original_tab_and_focus_on_new_tab()
        Helper.sleep_to(8)

    def verify_browser_title(self):
        # Note: 09-16-2016 website takes a while to load with no cache
        # Wow, My machine can be sloooooow, needs at least 10 seconds sometimes
        # I think it's because the title element is listed below a lot of scripts
        expected_home_page_title = config_file.home_title
        seconds_to_wait_for_title = 10
        WebDriverWait(self.driver, seconds_to_wait_for_title) \
            .until(expected_conditions.title_contains(expected_home_page_title), \
                   "Did NOT find a matching title!")
        # self.assertIn(expected_home_page_title, self.driver.title)
        # logging.info(" correct home page title found")
        # TODO: figure out if I want to assert here again, for the scraper

    def click_companies_and_reviews_search_type(self):
        #************************#
        #NOTE: Searching using 'Interviews' tab kind of sucks
        # so search by going to 'Companies & Reviews' first and then 
        # click the 'Interviews tab on the company page'

        # click to open 'fake' drop down list
        secs = 15 # Yes it takes a while sometimes...
        css_for_jobs_li = 'li[data-search-type="JOBS"] span'
        logging.info(" checking for JOBS css")
        WebDriverWait(self.driver, secs) \
            .until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, css_for_jobs_li)))
        logging.info(" clicking JOBS css")
        jobs_element = self.driver.find_element_by_css_selector(css_for_jobs_li)
        jobs_element.click()
        Helper.sleep_to(12) # bumped to 12 seconds...
        # ...because got error at companies_element.click(), even at 8 seconds
        
        # click to select a search type
        seconds_to_wait_for_search_type = 8 # Yes it takes a while sometimes...
        css_for_companies_li = 'li[data-search-type="EMPLOYER"] span'
        logging.info(" checking for EMPLOYER + span css")
        WebDriverWait(self.driver, seconds_to_wait_for_search_type) \
            .until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, css_for_companies_li)))
        logging.info(" clicking text for EMPLOYER + span css")
        companies_element = self.driver.find_element_by_css_selector(css_for_companies_li)
        companies_element.click()
        Helper.sleep_to(6, "to give time for webapp to change to company search type")

    def input_this_search_text(self, search_text):
        # NOTE: the website reuses the same main input field for the 
        # different searches (Company, Jobs, Interviews, Salaries...)
        logging.info(" entering this search text: " + search_text)
        keyword_field_css = "form input.keyword" 
        search_input = self.driver.find_element(By.CSS_SELECTOR, keyword_field_css)
        search_input.send_keys(search_text)
        Helper.sleep_to(5)

    def input_this_location(self, text_for_location):
        logging.info(" entering location text: " + text_for_location)
        # NOTE: The search section change depending on if you are logged in or not
        # not sure if I want to put in  logic to figure out if you are logged in
        # location_input = self.driver.find_element(By.ID, 'LocationSearch')
        location_input = self.driver.find_element(By.ID, 'sc.location')
        location_input.clear()
        location_input.send_keys(text_for_location)
        Helper.sleep_to(5)

    def click_search_button(self):
        # MAJOR NOTE: The website's business rules seem to launch a new page 
        # from homepage search IF something other than 'Jobs' is selected, 
        # and IF it is the user's first time visiting. Very unusual behavior
        css_for_search_button = 'div.container-form form button'
        WebDriverWait(self.driver, 5) \
            .until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, css_for_search_button)))
        logging.info(" clicking search button")
        search_button = self.driver.find_element_by_css_selector(css_for_search_button)
        search_button.click()
        # 20 seconds - website landing page sometimes takes a while
        Helper.sleep_to(20, "so landing page can fully load")

    def close_original_tab_and_focus_on_new_tab(self):
        # First time users that use a different drop down will launch a new tab, 
        # so close the original tab
        # THIS ASSUMES NEW TAB is already open!
        self.driver.switch_to.window(self.driver.window_handles[0])
        logging.info(" closing extra tab that is for job openings")
        self.driver.close()
        Helper.sleep_to(5)
        self.driver.switch_to.window(self.driver.window_handles[0])

