#%%
from scraper_module import Scraper
from bs4 import BeautifulSoup as bs

class LegoScraper(Scraper):
    def __init__(self, url, search_term, headless=False):
        self.name_list = []
        self.date_list = []
        self.creator_list =[]
        self.num_supporters_list = []
        self.num_days_remaining_list = []
        super().__init__(url, search_term, headless=False)
    
    def get_supporters_days_remaining(self):
        soup = bs(self.driver.page_source, 'html.parser')
        numbers = soup.findAll('div', class_= "count")
        self.num_supporters_list.append(numbers[0].text)
        self.num_days_remaining_list.append(numbers[1].text)
    
    def create_id(self):
        self.id_list = []
        for i in range(len(self.link_list)):
            ID = self.link_list[i][-12:]
            self.id_list.append(ID)

    def explore_product_ideas(self, XPATH1, XPATH2):
        self.click_button(XPATH1)
        self.click_button(XPATH2)

    def get_name_date_creator(self, link):
        self.get_html(link)
        name = self.soup.find('h1').text
        self.name_list.append(name)

        date = self.soup.find('span', {"class":"published-date"}).text
        self.date_list.append(date)

        creator_name = self.soup.find('a', {'data-axl':"alias"}).text
        self.creator_list.append(creator_name)

    def collate_info(self):
        self.info = {
            # "id": self.link_id,
            #     "uuid": self.link_uuid,
                "URL": self.link_list,
                "idea_name": self.name_list,
                "date": self.date_list,
                "creator": self.creator_list,
                "number_of_supporters": self.num_supporters_list,
                "number_of_days_remaining": self.num_days_remaining_list}
                #"image_links": self.img_list}
        #return self.info
        print(self.info)

    def collect_info(self):
        for link in self.link_list:
            self.open_url(link)
            #self.get_html(link)
            self.get_name_date_creator(link)
            self.get_supporters_days_remaining()

# %%
