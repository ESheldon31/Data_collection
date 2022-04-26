#%%
from scraper_module import Scraper
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class CollocationsScraper(Scraper):
    def create_dict(self):
        self.info = {
          "id": self.id_list,
        #         "uuid": self.link_uuid,
                "adj_rank-word-frequency": [],
                "adj_phrases": [],
                "verb_rank-word-frequency": [],
                "infinitive_verb": [],
                "verb_phrases": []}
        #print(self.info)

    def get_words(self):        
        list_words = []
        words = self.driver.find_elements(By.XPATH, '//span[@class="  result font-weight-bold text-success "]')
        for word in words:
            self.list_words.append(word.text)
        return list_words
    
    def create_id(self, word_list, word_class):
        for i in range(len(word_list)):
            id = f'{self.search_term}.{word_class}.{i}'
            self.id_list.append(id)
            
    def get_infinitives(self):
        list_words = self.get_words()
        list_infinitives = []
        for word in list_words:
            dictionary_url = f'https://es.thefreedictionary.com/{word}'
            self.driver.get(dictionary_url)
            try:
                accept_cookies = self.driver.find_element(By.XPATH, '/html/body/div[5]/div/div[1]/div/div/div[2]/a[1]')
                accept_cookies.click()
            except NoSuchElementException:
                pass
            try:
                infinitive = self.driver.find_element(By.tag_name, 'h1')
                list_infinitives.append(infinitive.text)
            except NoSuchElementException:
                list_infinitives.append('N/A')
            self.driver.close()
        self.info["infinitive_verbs"] = list_infinitives
    
    def choose_mode(self):
        mode_dict = {
            'word_class': ['adj', 'v'],
            'url_mode': ['', '?mode=frequency']
        }

    def get_frequency_and_phrases(self, word_class, dict_key, url_mode):
        temp_list = []
        new_url= f'{self.url}{word_class}/{self.search_term}{url_mode}'
        self.get_html(new_url)
        sentences = self.soup.findAll('li', {"class": "btn-result list-group-item list-group-item-action"})
        for sentence in sentences:
            temp_list.append(sentence.text)
        self.info[dict_key] = temp_list      


# %%
