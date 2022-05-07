#%%
from scraper_return_module import Scraper
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from data_template import LegoData

class LegoScraper(Scraper):
    def __init__(self, url, search_term, headless=False):
        super().__init__(url, search_term, headless=False)

    def get_links(self, XPATH_container, XPATH_search_results):
        self.scroll_down_bottom()
        try:
            self.see_more('//*[@id="search-more"]/a')
            self.infinite_scroll()
            pass
        except NoSuchElementException:
            pass
        list_links = self.get_list_links(XPATH_container, XPATH_search_results)
        return list_links

    def get_figures(self):
        numbers = self.find_all_in_html('div', 'class', 'count')
        return numbers
    
    def get_supporters(self):
        supporters = (self.get_figures())[0].text
        stripped_supporters = supporters.strip()
        return stripped_supporters

    def get_days_remaining(self):
        days_remaining = (self.get_figures())[1].text
        stripped_days_remaining = days_remaining.strip()
        return stripped_days_remaining

    def get_name(self, link):
        name = self.find_in_html(link, 'h1', None, None)
        return name

    def get_date(self, link):
        date = self.find_in_html(link, 'span', 'class', 'published-date')
        return date

    def get_creator_name(self, link):
        creator_name = self.find_in_html(link, 'a', 'data-axl', 'alias')
        stripped_creator_name = creator_name.strip()
        return stripped_creator_name

    def create_id(self, link):
        name = self.get_name(link)
        stripped_creator_name = self.get_creator_name(link)
        ID = f'{name}.{stripped_creator_name}'
        return ID
    
    def explore_product_ideas(self, XPATH1, XPATH2):
        self.click_button(XPATH1)
        self.click_button(XPATH2)

    def collect_info(self):
        link_list = self.get_links('//*[@id="search_results"]', './div')
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

        for link in link_list:
            self.open_url(link)
            self._get_html(link)
            lego_data.name_list.append(self.get_name(link))
            lego_data.date_list.append(self.get_date(link))
            lego_data.creator_list.append(self.get_creator_name(link))
            lego_data.num_supporters_list.append(self.get_supporters())
            lego_data.num_days_remaining_list.append(self.get_days_remaining())
            lego_data.id_list.append(self.create_id(link))
            lego_data.uuid_list.append(self.create_uuid())
            lego_data.img_list = self.get_img_links(
                XPATH_main_image='//div[@class="image-sizing-wrapper"]', 
                XPATH_thumbnail_container='//div[@class="thumbnails-tray"]', 
                XPATH_thumbnails='./div')
        return(lego_data)

    def scraping_now(self):
        try:
            self.accept_cookies(frame_id=None, XPATH= '//button[@aria-label="Reject cookies"]')
            self.search('//input[@name="query"]')
            lego_data = self.collect_info()
            self.download_raw_data(lego_data)
            self.download_images(lego_data)
        finally: self.quit()

# %%

# %%
