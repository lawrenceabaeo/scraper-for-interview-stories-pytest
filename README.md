# Scraper for Interview Stories, in Selenium with Python, pytest and Firefox

Scrapes the interview stories for a specified company, if that company is found on a popular company review website (this website will not be named here). The target website does not have a public API, so this python code collects interviews by using selenium to automate the process from the front-end UI. The target website has anti-bot measures in place including measuring how fast a user moves through the site, and the script has a lot of sleep statements to simulate how a real-end user would behave. Firefox is used because the target website detects and blocks chrome when chrome is used with selenium. The scraper is wrapped in pytest (a testing framework) - although with some careful study the script could be refactored to not use it. 

## Getting Started

Check the prerequisites. Download a copy of the code, then modify it for your local setup and other needs:

* Create a file called 'config\_file.py' and add in the details. Use the 'example\_config\_file.py' in the source code as a guide.

This script only collects interviews. If you want to scrape the other areas of the target website or scrape another website altogether, it may be easier to start a new project and just borrow pieces from here that might help your needs. 

### Prerequisites

1. Python 2.7+
    * For help on downloading and installing python, start here: [python.org 'Downloading Python'](https://wiki.python.org/moin/BeginnersGuide/Download)
2. Selenium Webdriver for Python
    * Type this command:
        * `pip install selenium`
    * For more help check here: [Installation for Selenium with Python](http://selenium-python.readthedocs.io/installation.html)
3. pytest
    * Type this command:
        * `pip install -U pytest`
    * For more help check here: [[pytest] Installation and Getting Started](https://docs.pytest.org/en/latest/getting-started.html)
4. Firefox and the geckodriver
    * [Click here to download Firefox](https://www.mozilla.org/en-US/firefox/)
    * [Click here to download geckodriver for your system](https://github.com/mozilla/geckodriver/releases) - look for your OS in the filename, like geckodr....1-win64.zip

## Running

The script is run from the command line. Navigate to the directory that contains test_scraper.py and type:

pytest

The '-s' flag for pytest will show info (like print statements) on the console:

pytest -s

Command line arguments include passing in a specific company and/or location - these will override any values hard-coded inside the script: 

pytest -s --company="Wally World" --location="New York, NY (US)"

pytest -s --company="OCP"

## Versioning

1.0.0

## Acknowledgments

* Google and StackOverflow were the main resources for this project. 

## BUGS and OTHER ITEMS
* 11.25.2017 - Does NOT scrape interview ANSWERS (maybe in a future update).
* 11.25.2017 - Script fails if an apostrophe is in the browser title. 
* 11.25.2017 - Script fails if unicode symbols are used in certain places (like a unicode ampersand). 

