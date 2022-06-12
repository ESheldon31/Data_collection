import unittest
import json
from Base_class.scraper_module import Scraper
from Data_collection.Project.Collocations_scraper.collocations_module import CollocationsScraper

def parse(filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except ValueError as e:
        print('Invalid json')
        return None

class TestCollocationsScraper(unittest.TestCase):

    def setUp(self, search_term) -> None:
        # sets up the variable used in the tests
        self.scraper = CollocationsScraper('https://inspirassion.com/es/', search_term)

    def test_inherited_class(self):
        # tests that the scraper created is an instance of the CollocationsScraper class
        self.assertIsInstance(self.scraper, CollocationsScraper)
    
    def test_base_class(self):
        # tests that the scraper created is an instance of the Scraper class, through inheritance
        self.assertIsInstance(self.scraper, Scraper)
    
    def test_driver_set_up(self):
        # tests that the initialisation of the scraper object goes to the correct url
        expected_url = f'https://inspirassion.com/es/'
        actual_url = self.scraper.driver.current_url()
        self.assertEqual(expected_url, actual_url)

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

    def test_keys(self):
        pass
 
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