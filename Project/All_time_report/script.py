#%%

from Project.Base_class.scraper_module import Scraper
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.by import By

from dotenv import load_dotenv
import os #provides ways to access the Operating System and allows us to read the environment variables

load_dotenv()

my_email = os.getenv("EMAIL_ADDRESS")
#my_secret_key = os.getenv("SECRET_KEY")
print(my_email)

class AllTimeScraper(Scraper):
    '''
    A child class of Scraper designed specifically to scrape the LegoIdeas website.

    '''
    
    def __init__(self, url, search_term, headless=False):
        '''
        calls the necessary attributes from the parent class
        '''
        super().__init__(url, search_term, headless)
        search_term = ''

    def log_in(self, XPATH_email, email_address, XPATH_password, password):
        email_log_in = self.driver.find_element(By.XPATH, XPATH_email)
        email_log_in.click()
        email_log_in.send_keys(email_address)
        password_log_in = self.driver.find_element(By.XPATH, XPATH_password)
        password_log_in.click()
        password_log_in.send_keys(password)
        
     #loginemail
    def scraping_now(self):
        self.log_in(XPATH_email='//input[@id="loginemail"]', email_address='', )

# %%
