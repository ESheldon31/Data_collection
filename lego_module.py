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
                
    def get_links(self, XPATH_container, XPATH_search_results):
        self.scroll_down_bottom()
        try:
            self.see_more('//*[@id="search-more"]/a')
            self.infinite_scroll()
            pass
        except NoSuchElementException:
            pass
        self.get_list_links(XPATH_container, XPATH_search_results)

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

    # def create_id(self, link):
    #     name, stripped_creator_name = self.get_name_date_creator(link)
    #     ID = f'{name}.{stripped_creator_name}'
    #     self.id_list.append(ID)
    
    def explore_product_ideas(self, XPATH1, XPATH2):
        self.click_button(XPATH1)
        self.click_button(XPATH2)

    def collate_info(self):
        print(self.info)

    def collect_info(self):
        for link in self.link_list:
            self.open_url(link)
            self.get_html(link)
            #self.get_name_date_creator(link)
            self.name_list.append(self.get_name(link))
            self.date_list.append(self.get_date(link))
            self.creator_list.append(self.get_creator_name(link))
            self.num_supporters_list.append(self.get_supporters())
            self.num_days_remaining_list.append(self.get_days_remaining())
            self.id_list.append(self.create_id(link))
            self.uuid_list.append(self.create_uuid())
            self.get_img_links(XPATH_main_image='//div[@class="image-sizing-wrapper"]', XPATH_thumbnail_container='//div[@class="thumbnails-tray"]', XPATH_thumbnails='./div')

    def scraping_now(self):
        try:
            self.accept_cookies(frame_id=None, XPATH= '//button[@aria-label="Reject cookies"]')
            self.search('//input[@name="query"]')
            self.get_links('//*[@id="search_results"]', './div')
            self.collect_info()
            self.collate_info()
            self.download_raw_data()
            #self.download_images()
        finally: self.quit()

# %%

# %%
