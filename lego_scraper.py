#%%
from lego_module import LegoScraper

if __name__ == '__main__': 

    def web_scraper_lego():
        #search_term = input('I would like to search for... ')
        search_term = 'violin'
        scraper = LegoScraper('https://ideas.lego.com', search_term)
        try:
            scraper.accept_cookies(frame_id=None, XPATH= '//button[@aria-label="Reject cookies"]')
            scraper.search('//input[@name="query"]')
            scraper.get_links('//*[@id="search_results"]', './div')
            scraper.collect_info()
            scraper.collate_info()
            #scraper.download_raw_data()
            #scraper.download_images()
        finally: scraper.quit()




    web_scraper_lego()
    


# %%
