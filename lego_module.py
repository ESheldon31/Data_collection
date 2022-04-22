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
    
    def get_name_date_creator(self, link):
        r = self.get_html(link)
        soup = bs(r.text, 'html.parser')
        name = soup.find('h1').text
        self.name_list.append(name)

        date = soup.find('span', {"class":"published-date"}).text
        self.date_list.append(date)

        creator_name = soup.find('a', {'data-axl':"alias"}).text
        # stripped_creator_name = creator_name.strip(' ')
        # stripped_stripped_creator_name = stripped_creator_name.strip('/n')
        self.creator_list.append(creator_name)

        return name, creator_name

    def create_id(self, link):
        name = self.get_name_date_creator(link)[0]
        creator_name = self.get_name_date_creator(link)[1]
        ID = f'{name}.{creator_name}'
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
                "number_of_days_remaining": self.num_days_remaining_list}
                #"image_links": self.img_list}
        #return self.info
        print(self.info)

    def collect_info(self):
        for link in self.link_list:
            self.open_url(link)
            self.get_html(link)
            self.get_name_date_creator(link)
            self.get_supporters_days_remaining()
            self.create_id(link)
            self.create_uuid()

# %%
