#%%
from scraper_module import Scraper

class CollocationsScraper(Scraper):
    def create_dict(self):
        self.info = {
        # "id": self.link_id,
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

    def get_infinitives(self, list_words):
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
    
    # def get_phrases(self, word_class):
    #     adj_phrase_list = []
    #     verb_phrase_list = []
    #     new_url= f'{self.url}{word_class}/{self.search_term}'
    #     self.get_html(new_url)
    #     sentences = self.soup.findAll('li', {"class": "btn-result list-group-item list-group-item-action"})
    #     if word_class == 'adj':
    #         for sentence in sentences:
    #             adj_phrase_list.append(sentence.text)
    #             self.info["adj_phrases"] = adj_phrase_list      
    #     if word_class == 'v':
    #         for sentence in sentences:
    #             verb_phrase_list.append(sentence.text)
    #             self.info["verb_phrases"] = verb_phrase_list
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
        
    # def get_frequency(self, word_class):
    #     self.adj_frequency_list = []
    #     self.verb_frequency_list = []
    #     new_url = f'{self.url}{word_class}/{self.search_term}?mode=frequency'
    #     self.driver.get(new_url)
    #     self.get_html(new_url)
    #     words_frequency = self.soup.findAll('li', {"class": "btn-result list-group-item list-group-item-action"})
    #     if word_class == 'adj':
    #         for frequency in words_frequency:
    #             str = frequency.text
    #             stripped_str = str.strip()
    #             self.adj_frequency_list.append(stripped_str)
    #             self.info["adj_rank-word-frequency"] = self.adj_frequency_list      
    #     if word_class == 'v':
    #         for frequency in words_frequency:
    #             self.verb_frequency_list.append(frequency.text)
    #             self.info["verb_rank-word-frequency"] = self.verb_frequency_list  

# %%
