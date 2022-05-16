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

    def get_words(self):
        url = f'https://inspirassion.com/es/v/{self.search_term}'
        self.driver.get(url)        
        list_words = []
        try:
            words = self.driver.find_elements(By.XPATH, '//span[@class=" result  "]')
            #print(words)
        except NoSuchElementException:
            print('Element not found.')
        for word in words:
            list_words.append(word.text)
        print(list_words)
        return list_words
    
    def create_id(self, word_list, word_class):
        for i in range(len(word_list)):
            id = f'{self.search_term}.{word_class}.{i}'
            return id
            
    
    
    def get_infinitives(self, list_words):
        #ToDo: investigate why this is not working
        if bool(list_words) == True:
            list_infinitives = []
            dictionary_url = f'https://es.thefreedictionary.com/'
            self.driver.get(dictionary_url)
            try:
                accept_cookies = self.driver.find_element(By.XPATH, '/html/body/div[5]/div/div[1]/div/div/div[2]/a[1]')
                accept_cookies.click()
            except NoSuchElementException:
                pass
            for word in list_words:
                try:
                    self._wait_for('//input[@type="search"]', click=False)
                    self.search('//input[@type="search"]', word)
                    infinitive = self.driver.find_element(By.TAG_NAME, 'h1')
                    list_infinitives.append(infinitive.text)
                except:
                    list_infinitives.append('N/A')
                search_bar = self.driver.find_element(By.XPATH, '//input[@type="search"]')
                search_bar.clear()
            print(list_infinitives)
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

    def collect_info(self, list_words):
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
        
        coll_data.verb_rank_word_frequency = self.get_frequency_and_phrases(word_class='v', url_mode='?mode=frequency', tag='div', attribute='class', 
                                                            attribute_name='d-flex flex-wrap justify-content-between align-items-center px-3')
        coll_data.infinitive_verb = self.get_infinitives(list_words)
        
        return coll_data

    def scraping_now(self):
        try:
            self.close_pop_up('//div[@class="drift-controller-icon--close"]')
            self.search('//input[@id="query"]', self.search_term)
            list_words = self.get_words()
            coll_data = self.collect_info(list_words)
            self.download_raw_data(coll_data, file_name='raw_data_coll')
        finally: self.quit()

# %%
