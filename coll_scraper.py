#%%

from collocations_module import CollocationsScraper

def web_scraper_collocations():
    search_term = 'libertad'
    scraper = CollocationsScraper('https://inspirassion.com/es/', search_term)
    scraper.scraping_now()
web_scraper_collocations()
# %%
