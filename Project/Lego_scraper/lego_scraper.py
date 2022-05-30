#%%
from Project.Lego_scraper.lego_module import LegoScraper

if __name__ == '__main__': 

    def web_scraper_lego():
        #search_term = input('I would like to search for... ')
        search_term = 'violin'
        scraper = LegoScraper('https://ideas.lego.com', search_term)
        scraper.scraping_now()

    web_scraper_lego()
    


# %%
