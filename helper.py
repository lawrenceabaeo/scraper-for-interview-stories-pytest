import time
import logging


class Helper():
    @staticmethod
    def sleep_to(seconds_to_sleep=6, why_message="to help evade bot detection"):
        logging.info(" sleeping " + str(seconds_to_sleep) 
        	         + " seconds " + why_message + "\n")
        time.sleep(seconds_to_sleep)

        