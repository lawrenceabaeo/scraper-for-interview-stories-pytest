import logging

from helper import Helper


class PopupObject():
    def __init__(self, driver):
        self.driver = driver

    def check_and_close_any_popups(self):
        if (self.popups_found() == True):
            second_window = self.driver.window_handles[1]
            self.driver.switch_to_window(second_window);
            logging.info(" closing popup")
            self.driver.close()
            self.driver.switch_to_window(self.driver.window_handles[0])
            if (self.popups_found() == True):
                raise Exception("Popup still found! Expected popup to be close!")

    def popups_found(self):
        # NOTE: popups seem to trigger fast, so only waiting 2 seconds.
        Helper.sleep_to(2, "then checking for popups")
        if len(self.driver.window_handles) > 1:
            logging.info(" multiple windows found")
            return True
        else:
            logging.info(" no popup found")
            return False

            