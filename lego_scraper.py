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
            scraper.get_list_links('//*[@id="search_results"]', './div')

            # scraper.get_img_links(XPATH_main_image='//div[@class="image-sizing-wrapper"]', XPATH_thumbnail_container='//div[@class="thumbnails-tray"]', XPATH_thumbnails='./div')
            #scraper.create_uuid(scraper.link_list)

            scraper.collect_info()
            # #scraper.get_info()
            scraper.collate_info()
            # scraper.download_raw_data()
            #scraper.download_images()
            #scraper.create_uuid()
            # scraper.scroll_down_bottom()
            # time.sleep(2)
            # scraper.see_more('//*[@id="search-more"]/a')
            # #scraper.scroll_up_top()
            # time.sleep(4)
        finally: scraper.quit()




    web_scraper_lego()
    


# %%
