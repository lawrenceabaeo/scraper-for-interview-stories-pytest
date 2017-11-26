import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

import popup


class CompanySearchResultsPageObject():

    def __init__(self, driver):
        self.driver = driver

    def on_company_search_results_page(self):
        logging.info(" checking if on company search results page")
        expected_title = "Reviews "
        try:
            WebDriverWait(self.driver, 10) \
                .until(expected_conditions.title_contains(expected_title))
            logging.info(" title of current page: " + self.driver.title)
            logging.info(" on search results page (containing '" 
                         + expected_title + "')")
            return True
        except TimeoutException:
            logging.info(" NOT on search results page (containing '" 
                         + expected_title + "')")
            logging.info(" title of current page: " + self.driver.title)
            return False

    def click_first_company_link(self):
        logging.info(" clicking link for company")
        company_link_css = "a.h2.tightAll" # this has changed in the past
        self.driver.find_element_by_css_selector(company_link_css).click()
        
        # ^handle popup
        # sometimes a popup appears after clicking company
        popup_object = popup.PopupObject(self.driver)
        popup_object.check_and_close_any_popups()
    
    def no_matching_companies(self):
        # Not waiting, assuming page rendered already
        logging.info(" checking if no matches were returned")
        suggestions_text_css = "div#SearchSuggestions" # This css changed before
        if (len(self.driver.find_elements_by_css_selector(suggestions_text_css)) > 0):
            logging.info(" suggestions css found")
            # NOTE: The search suggestions text used to be 'Search Suggestions', 
            # now it is 'Adjust your search'. Will NOT verify the text anymore, 
            # and instead rely on if the SearchSuggestions div exists
            return True
        else: 
            logging.info(" no search suggestions css found...")
            logging.info(" ... assuming companies were found")
            return False
            
