#%%

from collocations_module import CollocationsScraper

def web_scraper_collocations():
    search_term = 'libertad'
    scraper = CollocationsScraper('https://inspirassion.com/es/', search_term)
    try:
        scraper.search('//input[@id="query"]')
        scraper.create_dict()
        scraper.get_frequency_and_phrases(word_class='adj', dict_key='adj_phrases', url_mode='')
        scraper.get_frequency_and_phrases(word_class='adj', dict_key='adj_rank-word-frequency', url_mode='?mode=frequency')
        scraper.get_frequency_and_phrases(word_class='v', dict_key='v_phrases', url_mode='')
        scraper.get_frequency_and_phrases(word_class='v', dict_key='v_rank-word-frequency', url_mode='?mode=frequency')
        scraper.get_infinitives()
        # scraper.get_frequency(word_class='v')
        # scraper.get_phrases(word_class='v')
        #scraper.collate_data()
        scraper.download_raw_data(file_name='raw_data_coll')
        #time.sleep(2)
        # scraper.click_button('//span[@class="gl-new-dropdown-button-text"]')
        # scraper.click_button('//*[@class="gl-new-dropdown-item"][6]')
    finally: scraper.quit()
web_scraper_collocations()
# %%
