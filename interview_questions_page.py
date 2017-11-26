import logging

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from helper import Helper


class InterviewQuestionsPageObject():

    def __init__(self, driver):
        self.driver = driver

    def get_interviews_and_write_them_to_a_file(self):
        # This is just a wrapper to group together a sequence of functions.
        # NOTE: A previous step should have checked 
        # if there were no interviews (and if none, it should have exited).
        self.verify_on_interview_questions_page()
        self.sort_interviews_by_date()
        self.collect_interviews_into_a_file()

    def verify_on_interview_questions_page(self):
        logging.info(" checking if on interview questions page")
        expected_text = 'Candidate Interview Review' # <- Notice I left it singular, 
                                                     # it's either Review or Reviews
        css_only_found_on_interview_questions_page = "div.interviewsAndFilter"
        css_for_h2_text = "div.interviewsAndFilter div.eiFilter div.basicForm h2"
        WebDriverWait(self.driver, 10) \
            .until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, css_only_found_on_interview_questions_page)))

    def sort_interviews_by_date(self):
        # NOTE: might be nice to have more elegant way of clicking and detecting 
        # if clicked worked (due to race condition with attaching js handlers), 
        # but for now just using sleep
        css_date_sort = "div.hideHH span.sorts span.filterSorts a.sortByDate"
        WebDriverWait(self.driver, 10) \
            .until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, css_date_sort)))
        date_link = self.driver.find_element_by_css_selector(css_date_sort) 
        if ('strong' not in date_link.get_attribute('class')):
            logging.info(" date not sorted")
            msg = "because selenium gets ahead of js attaching handlers"
            Helper.sleep_to(4, msg)
            logging.info(" clicking to sort date")
            date_link.click()
            Helper.sleep_to(6, "to give enough time for sort to finish")
        else:
            logging.info(" already sorted by date")
            pass
        
        # ^verify sort by date descending
        logging.info(" checking if sorted by date")
        css_date_sort_strong = css_date_sort + ".strong"
        # got a TimeoutException error here, so using a long 12 seconds here
        WebDriverWait(self.driver, 12) \
            .until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, css_date_sort_strong)))
        date_link_again = self.driver.find_element_by_css_selector(css_date_sort)
        
    def collect_interviews_into_a_file(self):
        # NOTE: Assumes interviews were found
        # NOTE: NEED something more complex to handle middle row of 'Outcomes'
        # or try use of 'nth-child(nn)

        # open a file
        filename = "scrape_results.txt"
        target = open(filename, 'w')
        self.get_interviews_on_pages(target)
        target.close()

    def get_interviews_on_pages(self, target_file):
        # NOTE: for this function to work, user must be logged in, otherwise 
        # they might see an overly about logging in
        # This function is separate from 'collect_interviews_into_a_file'
        #  so that recursion can happen when collecting interviews across
        #  different pages.  
        css_for_interview_list_item = "li.empReview"
        list_items_for_interview_reviews = self.driver.find_elements_by_css_selector(css_for_interview_list_item)
        
        target = target_file
        self.write_list_items_to_file(list_items_for_interview_reviews, target)
        
        # Check if more pages
        logging.info(" checking if next button exists for more pages")
        css_for_next_page_button = "ul li.next a"
        page_button_list = self.driver.find_elements_by_css_selector(css_for_next_page_button)
        if (len(self.driver.find_elements_by_css_selector(css_for_next_page_button)) > 0):
            # NOTE: I haven't found a graceful way to navigate 
            # to the next page without using sleep
            logging.info(" -found next button")
            logging.info(" clicking next button")
            before_url = self.driver.current_url
            page_button_list[0].click()
            Helper.sleep_to(6, "to let new *url* appear in url bar")
            
            # ^check if new url loaded
            if (before_url == self.driver.current_url):
                Helper.sleep_to(6, "again, to let new *url* appear in url bar")
                if (before_url == self.driver.current_url):
                    raise Exception("New url did NOT load in the browser's url field?!")
            else: 
                logging.info(" -new url was loaded into browser address bar")

            Helper.sleep_to(6, "to allow extra time for new page to load")
                
            self.verify_on_interview_questions_page()
            self.get_interviews_on_pages(target)
        else:
            logging.info(" -no next button, assuming no more pages")

    def write_list_items_to_file(self, list_items, target_file):
        for item in list_items:
            text_start = "==========================================\n"
            target_file.write(text_start)
            print (text_start)

            # title
            css_for_job_title = "div.tbl div.row div.cell h2.summary a span"
            text_for_title = item.find_element_by_css_selector(css_for_job_title).text + "\n"
            target_file.write(text_for_title)
            print (text_for_title)

            # author
            css_for_author = "div.author.minor"
            text_for_author = "written by: " + \
                item.find_element_by_css_selector(css_for_author).text + "\n"
            target_file.write(text_for_author)
            print (text_for_author)

            # Each interview can show 3 outcome 'aspects', 
            # but do not appear to be required:
            # Offer | Experience | Difficulty
            # The order can change depending on which aspects are displayed, 
            # so I won't be writing any descriptions
            css_for_interview_outcomes = "div.interviewOutcomes div.flex-grid div.tightLt span"
            outcomes = item.find_elements_by_css_selector(css_for_interview_outcomes)
            if (len(outcomes) > 0):
                for each_outcome_aspect in outcomes:
                    target_file.write(each_outcome_aspect.text + " ")
                    print(each_outcome_aspect.text) 
            target_file.write("\n")

            # Show More
            css_for_show_more_content = "span.moreContent span.moreLink"
            spans_for_show_more= len(item.find_elements_by_css_selector(css_for_show_more_content))
            if (spans_for_show_more > 0):
                logging.info(" 'Show More' found - there's more to capture for the interview")
                show_more_span = item.find_element_by_css_selector(css_for_show_more_content)
                logging.info(" clicking the 'Show More' span")
                show_more_span.click()
                Helper.sleep_to(2, "to let web app finish opening more content")
            
            # Interview Details
            css_for_interview_details = "p.interviewDetails"
            text_for_int_details = "Interview\n" + \
                item.find_element_by_css_selector(css_for_interview_details).text + "\n"
            target_file.write(text_for_int_details)
            print (text_for_int_details)

            # job application description
            css_for_application_description = "p.applicationDetails"
            num_application_details = len(item.find_elements_by_css_selector(css_for_application_description))
            if (num_application_details > 0):
                text_for_application_description = "Application\n" + \
                    item.find_element_by_css_selector(css_for_application_description).text + "\n"
                target_file.write(text_for_application_description)
                print (text_for_application_description)

            # interview questions
            css_for_questions = "div.interviewQuestions li"
            css_for_individual_question = "span.interviewQuestion"
            list_of_questions = item.find_elements_by_css_selector(css_for_questions)
            if (len(list_of_questions) > 0):
                logging.info(" found interview question(s)")
                text_for_questions = "\nQuestions:\n"
                for entry in list_of_questions:
                    question_text = entry.find_element_by_css_selector(css_for_individual_question).text
                    text_for_questions += (question_text + "\n")
                    target_file.write(text_for_questions)                    
                    print (question_text)
                target_file.write("\n")

