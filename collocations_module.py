#%%
from scraper_module import Scraper
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from data_template import CollocationsData

#ToDo: tidy up
#ToDo: Docstrings
#ToDo: fix get_words and get_infinitives
#ToDo: create methods for id and uuid
#ToDo: create config file 

class CollocationsScraper(Scraper):
    def __init__(self, url, search_term, headless=False):
        super().__init__(url, search_term, headless)
    #     self.info = {
    #             #"id": self.id_list,
    #     #         "uuid": self.link_uuid,
    #             "adj_rank-word-frequency": [],
    #             "adj_phrases": [],
    #             "verb_rank-word-frequency": [],
    #             "infinitive_verb": [],
    #             "verb_phrases": []}
    # # def create_dict(self):

    #     #print(self.info)

    def get_words(self):
        url = f'https://inspirassion.com/es/v/{self.search_term}'
        self.driver.get(url)        
        list_words = []
        try:
            words = self.driver.find_elements(By.XPATH, '//span[@class=" result  "]')
            print(words)
        except NoSuchElementException:
            print('Element not found.')
        for word in words:
            list_words.append(word.text)
        print(list_words)
        return list_words
    
    # def create_id(self, word_list, word_class):
    #     for i in range(len(word_list)):
    #         id = f'{self.search_term}.{word_class}.{i}'
    #         self.id_list.append(id)
            
    def get_infinitives(self):
        #ToDo: investigate why this is not working
        list_words = self.get_words()
        if bool(list_words) == True:
            list_infinitives = []
            for word in list_words:
                original_window = self.driver.current_window_handle
                dictionary_url = f'https://es.thefreedictionary.com/{word}'
                self.driver.get(dictionary_url)
                try:
                    accept_cookies = self.driver.find_element(By.XPATH, '/html/body/div[5]/div/div[1]/div/div/div[2]/a[1]')
                    accept_cookies.click()
                except NoSuchElementException:
                    pass
                try:
                    infinitive = self.driver.find_element(By.TAG_NAME, 'h1')
                    list_infinitives.append(infinitive.text)
                except NoSuchElementException:
                    list_infinitives.append('N/A')
                self.driver.close()
                self.driver.switch_to.window(original_window)
            return list_infinitives
        else: print('list_words does not exist')
    

    def get_frequency_and_phrases(self, word_class, url_mode, tag, attribute, attribute_name):
        temp_list = []
        new_url= f'{self.url}{word_class}/{self.search_term}{url_mode}'
        self.open_url(new_url)
        element = self.find_all_in_html(tag, attribute, attribute_name)
        for element in element:
            temp_list.append(element.text)
        return temp_list      

    def collect_info(self):
        coll_data = CollocationsData(
            uuid_list=[],
            id_list=[],
            img_list=None,
            link_list=None, 
            adj_phrases=[],
            adj_rank_word_frequency=[],
            verb_phrases=[],
            verb_rank_word_frequency=[],
            infinitive_verb=[])

        coll_data.adj_phrases = self.get_frequency_and_phrases(word_class='adj', 
                                                            url_mode='', 
                                                            tag='p', 
                                                            attribute='class', 
                                                            attribute_name='btn-result text-start border-gray-300 border-bottom p-4 bg-hover-light-dark m-0')
        coll_data.adj_rank_word_frequency = self.get_frequency_and_phrases(word_class='adj', url_mode='?mode=frequency', tag='div', attribute='class', 
                                                            attribute_name='d-flex flex-wrap justify-content-between align-items-center px-3')
        coll_data.verb_phrases = self.get_frequency_and_phrases(word_class='v', url_mode='', tag='p', 
                                                            attribute='class', 
                                                            attribute_name='btn-result text-start border-gray-300 border-bottom p-4 bg-hover-light-dark m-0')
        coll_data.infinitive_verb = self.get_infinitives()
        coll_data.verb_rank_word_frequency = self.get_frequency_and_phrases(word_class='v', url_mode='?mode=frequency', tag='div', attribute='class', 
                                                            attribute_name='d-flex flex-wrap justify-content-between align-items-center px-3')
        
        return coll_data

    def scraping_now(self):
        try:
            self.close_pop_up('//div[@class="drift-controller-icon--close"]')
            self.search('//input[@id="query"]')
            coll_data = self.collect_info()
            #self.create_dict()
            # self.get_frequency_and_phrases(word_class='adj', dict_key='adj_phrases', url_mode='')
            # self.get_frequency_and_phrases(word_class='adj', dict_key='adj_rank-word-frequency', url_mode='?mode=frequency')
            # self.get_frequency_and_phrases(word_class='v', dict_key='v_phrases', url_mode='')
            # self.get_frequency_and_phrases(word_class='v', dict_key='v_rank-word-frequency', url_mode='?mode=frequency')
            # self.get_infinitives()
            # print(self.info)
            # scraper.get_frequency(word_class='v')
            # scraper.get_phrases(word_class='v')
            #scraper.collate_data()
            self.download_raw_data(coll_data, file_name='raw_data_coll')
        finally: self.quit()

# %%
