from scraper_module import Scraper

class CollocationsScraper(Scraper):
    def create_dict(self):
        self.info = {
        # "id": self.link_id,
        #         "uuid": self.link_uuid,
                "adj_rank-word-frequency": [],
                "adj_phrases": [],
                "verb_rank-word-frequency": [],
                "verb_phrases": []}
        #print(self.info)

    def get_words(self):        
        self.list_words = []
        # container_results = driver.find_element(By.XPATH, '//ul[@class="sentence-mode result-group list-group mt-4 "]')
        # list_results = container_results.find_elements(By.XPATH, './li')
        words = self.driver.find_elements(By.XPATH, '//span[@class="  result font-weight-bold text-success "]')
        # for result in list_results:
        #     words = result.find_elements(By.XPATH, '//span[@class="  result font-weight-bold text-success "]')
        for word in words:
            self.list_words.append(word.text)
        print(self.list_words)

    def get_infinitives(self):
        list_infinitives = []
        for word in self.list_words:
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
        print(list_infinitives)
    
    def get_phrases(self, word_class):
        self.adj_phrase_list = []
        self.verb_phrase_list = []
        new_url= f'{self.url}{word_class}/{self.search_term}'
        self.get_html(new_url)
        sentences = self.soup.findAll('li', {"class": "btn-result list-group-item list-group-item-action"})
        if word_class == 'adj':
            for sentence in sentences:
                self.adj_phrase_list.append(sentence.text)
                self.info["adj_phrases"] = self.adj_phrase_list      
        if word_class == 'v':
            for sentence in sentences:
                self.verb_phrase_list.append(sentence.text)
                self.info["verb_phrases"] = self.verb_phrase_list
 

    def get_frequency(self, word_class):
        self.adj_frequency_list = []
        self.verb_frequency_list = []
        new_url = f'{self.url}{word_class}/{self.search_term}?mode=frequency'
        self.driver.get(new_url)
        self.get_html(new_url)
        words_frequency = self.soup.findAll('li', {"class": "btn-result list-group-item list-group-item-action"})
        if word_class == 'adj':
            for frequency in words_frequency:
                str = frequency.text
                stripped_str = str.strip()
                self.adj_frequency_list.append(stripped_str)
                self.info["adj_rank-word-frequency"] = self.adj_frequency_list      
        if word_class == 'v':
            for frequency in words_frequency:
                self.verb_frequency_list.append(frequency.text)
                self.info["verb_rank-word-frequency"] = self.verb_frequency_list  
