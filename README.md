# Scraper for Interview Stories, in Selenium with Python, PyTest and Firefox

Scrapes the interview stories for a specified company, if that company is found on a popular company review website (this website will not be named here). The target website does not have a public API, so this python code collects interviews by using selenium to automate the process from the front-end UI. The target website has anti-bot measures in place including measuring how fast a user moves through the site, and the script has a lot of sleep statements to simulate how a real-end user would behave. Firefox is used because the target website detects and blocks chrome when chrome is used with selenium. The scraper is wrapped in PyTest (a testing framework) - although with some careful study the script could be refactored to not use it. 

## Getting Started

Check the prerequisites. Download a copy of the code, then modify it for your local setup and other needs:

* Create a file called 'configurations\_file.py' and add in the details. Use the 'example\_configurations\_file.py' in the source code as a guide.

This script only collects interviews. If you want to scrape the other areas of the target website or scrape another website altogether, it may be easier to start a new project and just borrow pieces from here that might help your needs. 

### Prerequisites

* Python 3
* Selenium
* PyTest
* Firefox

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

