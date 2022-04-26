#%%
from scraper_module import Scraper
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class LegoScraper(Scraper):
    def __init__(self, url, search_term, headless=False):
        self.name_list = []
        self.date_list = []
        self.creator_list =[]
        self.num_supporters_list = []
        self.num_days_remaining_list = []
        super().__init__(url, search_term, headless=False)
    
    def get_links(self, XPATH_container, XPATH_search_results):
        self.scroll_down_bottom()
        try:
            self.see_more('//*[@id="search-more"]/a')
            self.infinite_scroll()
            pass
        except NoSuchElementException:
            pass
        self.get_list_links(XPATH_container, XPATH_search_results)

    def get_supporters_days_remaining(self):
        numbers = self.find_all_in_html('div', 'class', 'count')
        supporters = numbers[0].text
        stripped_supporters = supporters.strip()
        self.try_append(self.num_supporters_list, stripped_supporters)
        days_remaining = numbers[1].text
        stripped_days_remaining = days_remaining.strip()
        self.try_append(self.num_days_remaining_list, stripped_days_remaining)

    '''Uses self and works'''
    def get_name_date_creator(self, link):
        self.name = self.find_in_html(link, 'h1', None, None)
        self.try_append(self.name_list, self.name)

        date = self.find_in_html(link, 'span', 'class', 'published-date')
        self.try_append(self.date_list, date)

        creator_name = self.find_in_html(link, 'a', 'data-axl', 'alias')
        self.stripped_creator_name = creator_name.strip()
        self.try_append(self.creator_list, self.stripped_creator_name)
    
    '''Uses self (and works)'''
    def create_id(self):
        ID = f'{self.name}.{self.stripped_creator_name}'
        self.id_list.append(ID)
        
    '''Returns it appended to the lists three times!'''
    def get_name_date_creator(self, link):
        r = self.get_html(link)
        soup = bs(r.text, 'html.parser')
        name = soup.find('h1').text
        self.name_list.append(name)

        date = soup.find('span', {"class":"published-date"}).text
        self.date_list.append(date)

        creator_name = soup.find('a', {'data-axl':"alias"}).text
        stripped_creator_name = creator_name.strip()
        self.creator_list.append(stripped_creator_name)
        return name, stripped_creator_name

    '''Uses returned items (and works)'''
    def create_id(self, link):
        name, stripped_creator_name = self.get_name_date_creator(link)
        ID = f'{name}.{stripped_creator_name}'
        self.id_list.append(ID)
    

    
    def explore_product_ideas(self, XPATH1, XPATH2):
        self.click_button(XPATH1)
        self.click_button(XPATH2)

    def collate_info(self):
        self.info = {
                "id": self.id_list,
                "uuid": self.uuid_list,
                "URL": self.link_list,
                "idea_name": self.name_list,
                "date": self.date_list,
                "creator": self.creator_list,
                "number_of_supporters": self.num_supporters_list,
                "number_of_days_remaining": self.num_days_remaining_list,
                "image_links": self.img_list}
        #return self.info necessary?
        print(self.info)

    def collect_info(self):
        for link in self.link_list:
            self.open_url(link)
            self.get_html(link)
            self.get_name_date_creator(link)
            self.get_supporters_days_remaining()
            self.create_id()
            self.create_uuid()
            self.get_img_links(XPATH_main_image='//div[@class="image-sizing-wrapper"]', XPATH_thumbnail_container='//div[@class="thumbnails-tray"]', XPATH_thumbnails='./div')

    def scraping_now(self):
        try:
            self.accept_cookies(frame_id=None, XPATH= '//button[@aria-label="Reject cookies"]')
            self.search('//input[@name="query"]')
            self.get_links('//*[@id="search_results"]', './div')
            self.collect_info()
            self.collate_info()
            #self.download_raw_data()
            #self.download_images()
        finally: self.quit()

# %%

# %%
