import logging

import working_at_page
import company_search_results_page


class WebApp():

    @staticmethod
    def check_resulting_landing_page(driver, location, company_name):
        #************************#
        # ~LANDING PAGE~
        #************************#
        # Possible landing page scenarios/results:
        # - A: lands directly on company page (ex. Pandora)
        # - B: lands on search results list, with 1 match
        # - C: lands on search results list, with multiple matches
        # (scenario C is NOT handled in this script)
        # TODO: Handle scenario C
        # - D: lands on search results, no matches
        # - E: lands on incorrect page
        
        # pseudo-code:
        # if lands directly on company page....move to company page verification
        # else, check if on search results page...else make an exception
        # ....on search results page...
        #..........if no matches, exit progra  m
        #..........else if matches, click first match, then do company page verification

        working_at_page_object = working_at_page.WorkingAtPageObject(driver)
        results_page_object = company_search_results_page.CompanySearchResultsPageObject(driver)

        # Check which landing page resulted:
        logging.info(" checking which landing page resulted")
        logging.info(" checking if first landed on company page.")

        if (working_at_page_object.on_working_at_page() == True): # Scen. A
            logging.info(" landed directly on company page")
        elif (results_page_object.on_company_search_results_page() == True): # Scen. B/C
            logging.info(" landed on search results page first and not company page")
            # Check if no matching companies
            if (results_page_object.no_matching_companies() == True): # Scen. D
                logging.info(" NO matching companies found! Input: " + company_name + " " + location)
                logging.info(" exiting automation")
                exception_message = "Did NOT find any matching companies! input was: " + company_name + " " + location
                raise Exception(exception_message)
            else: 
               results_page_object.click_first_company_link() # Scen. B/C
        else:
            title_message = "Landed on an unexpected page that has the title: " + driver.title # Scen. #
            raise Exception(title_message)

