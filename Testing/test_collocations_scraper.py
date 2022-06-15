import unittest
import json
from Base_class.scraper_module import Scraper
from Data_collection.Project.Collocations_scraper.collocations_module import CollocationsScraper
# todo: refactor so can put in lego scraper too
# test that values are lists (or null)

def parse(filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except ValueError as e:
        print('Invalid json')
        return None

class TestCollocationsScraper(unittest.TestCase):

    def setUp(self, search_term):
        # initialises the class that will then be tested
        self.scraper = CollocationsScraper('https://inspirassion.com/es/', search_term)

    def test_inherited_class(self):
        # tests that the scraper created is an instance of the CollocationsScraper class
        self.assertIsInstance(self.scraper, CollocationsScraper)
        print('The scraper is an instance of the CollocationsScraper class.')

    def test_base_class(self):
        # tests that the scraper created is an instance of the Scraper class, through inheritance
        self.assertIsInstance(self.scraper, Scraper)
        print('The scraper has inherited from the base Scraper class.')

    def test_driver_set_up(self):
        # tests that the initialisation of the scraper object goes to the correct url
        expected_url = f'https://inspirassion.com/es/'
        actual_url = self.scraper.driver.current_url()
        self.assertEqual(expected_url, actual_url)
        print('The scraper initialises on the correct url.')

    # def test_search(self):
    #     # tests that the search method goes to the correct url
    #     expected_url = f'https://inspirassion.com/es/adj/{self.scraper.search_term}'
    #     actual_url = self.scraper.driver.current_url()
    #     self.assertEqual(expected_url, actual_url)

    # def test_list_created(self):
    #     pass

    def test_scraping_now(self):
        # tests that a json is created
        self.scraper.scraping_now()
        self.assertIsInstance(parse('data.json'), dict)
        print('The "scraping now" method creates a json file.')

class TestCollocationsScraperOutcome(unittest.TestCase):
    def setUp(self):
        # opens json file to then test contents
        with open('Data_collection/Project/Collocations_scraper/raw_data_coll/data.json', mode='r') as f:
            self.data = json.load(f)

        # with open('../Scraper_Project/coins_images.json', mode='r') as f:
        #     self.image_list = json.load(f)   
    
    def test_keys(self):
        # tests that the dictionary in the json file has the correct keys
        dict_keys = self.data.keys()
        expected_keys = ['uuid_list', 
                        'id_list',
                        'link_list', 
                        'img_list', 
                        'adj_rank_word_frequency', 
                        'adj_phrases', 
                        'verb_rank_word_frequency', 
                        'infinitive_verb', 
                        'verb_phrase']
        self.assertListEqual(dict_keys, expected_keys)
        print('Data.json has the correct keys.')

#test that values are lists (or null)
    # def test_file_created(self):
    #     # tests that a json is created
    #     self.assertIsInstance(parse('data.json'), dict)
    

def suite():
    # a function to create a test suite so the tests run in the required order
    suite = unittest.TestSuite()
    suite.addTest(TestCollocationsScraper('name of test'))
    suite.addTest(TestCollocationsScraper('name of test'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

#Check instance of a class has been created

#check whether it has gone to the right url

#check list has been created.

#check length of list

# check instance of dataclass made

#check it has info in it (how?)

#check json is made?

#    def scraping_now(self):
        # try:
        #     self._close_pop_up('//div[@class="drift-controller-icon--close"]')
        #     self._search('//input[@id="query"]') - check whether it has gone to the right url print(browser.current_url)
        #     list_words = self._get_words()
        #     coll_data = self._collect_info(list_words)
        #     self._download_raw_data(coll_data, file_name='raw_data_coll')
        # finally: self._quit()


        
#self.assertIsInstance(result, webdriver.chrome.webdriver.WebDriver)

#def parse(filename): 
#   try: 
#       with open(filename) as f: 
#           return json.load(f) 
#   except ValueError as e: print('invalid json: %s' % e) 
#           return None