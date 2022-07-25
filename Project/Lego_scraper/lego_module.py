#%%
# import sys
# sys.path.append('/Users/ESheldon/Desktop/data_collection/Data_collection/Project/')
from Project.Base_class.scraper_module import Scraper
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException  #, TimeoutException
from Project.Base_class.data_template import LegoData

#ToDo: config file with XPATHs stored in dict
#ToDo: type hints
#ToDo: make final decision on which methods are protected and which are public
# ToDo: add details of public methods in class docstring
'''
This module contains a child scraper class and its methods.

'''
class LegoScraper(Scraper):
    '''
    A child class of Scraper designed specifically to scrape the LegoIdeas website.

    '''
    
    def __init__(self, url, search_term, headless=False):
        '''
        calls the necessary attributes from the parent class
        '''
        super().__init__(url, search_term, headless)

    def _get_links(self, XPATH_container, XPATH_search_results):
        '''
        collects the links to each idea page from the search results 
        uses infinite_scroll to ensure links for all results are collected
        
        Parameters:
            XPATH_container: str
                XPATH for the container that holds the search results
            XPATH_search_results: str
                XPATH for the individual search results
                
        Returns:
            list of links 
        '''
        self._scroll_down_bottom()
        try:
            self._see_more('//*[@id="search-more"]/a')
            self._infinite_scroll()
            pass
        except NoSuchElementException:
            pass
        list_links = self._get_list_links(XPATH_container, XPATH_search_results)
        return list_links

    def _get_figures(self):
        '''
        collects the numerical information from webpage. 
        
        Returns: list
            list of figures(str)
            
        '''
        numbers = self._find_all_in_html('div', 'class', 'count')
        return numbers
    
    def _get_supporters(self):
        '''
        finds the number of supporters for each Lego idea

        Returns : str
            number of supporters

        '''
        supporters = (self._get_figures())[0].text
        stripped_supporters = supporters.strip()
        return stripped_supporters

    def _get_days_remaining(self):
        '''
        finds the number of days the idea has left on the website. 
        This number increases with increasing numbers of supporters.

        Returns : str
            number of days remaining

        '''
        days_remaining = (self._get_figures())[1].text
        stripped_days_remaining = days_remaining.strip()
        return stripped_days_remaining

    def _get_name(self, link):
        '''
        finds the idea name for each Lego idea
        
        Parameters:
        link : str
            url of the Lego idea result page

        Returns : str
            idea name

        '''
        name = self._find_in_html(link, 'h1', None, None)
        return name

    def _get_date(self, link):
        '''
        for each Lego idea, finds the date it was submitted to the website
        
        Parameters:
        link : str
            url of the Lego idea result page

        Returns : str
            date
            
        '''
        date = self._find_in_html(link, 'span', 'class', 'published-date')
        return date

    def _get_creator_name(self, link):
        '''
        finds the creator's name for each Lego idea
        
        Parameters:
        link : str
            url of the Lego idea result page

        Returns : str
            creator's name

        '''
        creator_name = self._find_in_html(link, 'a', 'data-axl', 'alias')
        stripped_creator_name = creator_name.strip()
        return stripped_creator_name

    def _create_id(self, link):
        '''
        creates user-friendly ID for each Lego idea
        
        Parameters:
            link : str
                url of the Lego idea result page

        Returns : str
            ID

     '''
        name = self._get_name(link)
        stripped_creator_name = self._get_creator_name(link)
        ID = f'{name}.{stripped_creator_name}'
        return ID
    
    def _explore_product_ideas(self, XPATH1, XPATH2):
        #not used. Remove?
        self._click_button(XPATH1)
        self._click_button(XPATH2)

    @staticmethod
    def _create_empty_dataclass():
        lego_data = LegoData(
            uuid_list=[], 
            id_list=[], 
            img_list=[], 
            date_list=[], 
            creator_list=[], 
            name_list= [], 
            num_days_remaining_list=[], 
            num_supporters_list=[],
            link_list=None)
        return lego_data

    def _collect_info(self):
        '''
        collects list of links, for each link appends data to list in dataclass

        Returns:
            instance of dataclass with all data appended

        '''
        
        link_list = self._get_links('//*[@id="search_results"]', './div')
        lego_data = self._create_empty_dataclass()

        for link in link_list:
            self._open_url(link)
            self._get_html(link)
            lego_data.name_list.append(self._get_name(link))
            lego_data.date_list.append(self._get_date(link))
            lego_data.creator_list.append(self._get_creator_name(link))
            lego_data.num_supporters_list.append(self._get_supporters())
            lego_data.num_days_remaining_list.append(self._get_days_remaining())
            lego_data.id_list.append(self._create_id(link))
            lego_data.uuid_list.append(self._create_uuid())
            lego_data.img_list = self._get_img_links(
                XPATH_main_image='//div[@class="image-sizing-wrapper"]', 
                XPATH_thumbnail_container='//div[@class="thumbnails-tray"]', 
                XPATH_thumbnails='./div')
        
        return(lego_data)

    def scraping_now(self):
        '''
        runs the various methods to accept cookies, search, collect and download data and images
        '''
    
        self._accept_cookies(frame_id=None, XPATH= '//button[@aria-label="Reject cookies"]')
        self._search('//input[@name="query"]')
        lego_data = self._collect_info()
        self._download_raw_data(lego_data)
        self._download_images(lego_data.img_list)


# %%

# %%
