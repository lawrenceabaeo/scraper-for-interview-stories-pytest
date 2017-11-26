import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class OverlayObject():
  
    def __init__(self, driver):
        self.driver = driver

    def check_and_close_any_overlay(self):
        if (self.overlay_found() == True):
            logging.info(" closing overlay")
            css_for_overlay_close_button = "button.mfp-close"
            overlay_close_button = self.driver.find_element_by_css_selector(css_for_overlay_close_button)
            logging.info(" overlay found, closing overlay")
            overlay_close_button.click()
            if (self.overlay_found(2) == True):
                raise Exception("Overlay found AFTER clicking close button!. Was not expecting overlay to remain!")

    def overlay_found(self, seconds_to_wait=5):
        logging.info(" checking for overlay")
        try: 
            css_for_overlay = "div.mfp-bg.mfp-ready"
            WebDriverWait(self.driver, seconds_to_wait) \
                .until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, css_for_overlay)))
            logging.info(" overlay found")
            return True
        except TimeoutException:
            logging.info(" no overlay found")
            return False

