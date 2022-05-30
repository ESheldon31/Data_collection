#%%

from Project.Collocations_scraper.collocations_module import CollocationsScraper

if __name__ == '__main__':
        
    def web_scraper_collocations():
        search_term = 'libertad'
        scraper = CollocationsScraper('https://inspirassion.com/es/', search_term)
        scraper.scraping_now()
    web_scraper_collocations()
# %%
