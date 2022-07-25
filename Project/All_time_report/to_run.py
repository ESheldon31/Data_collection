#%%

from Project.All_time_report.script import AllTimeScraper

if __name__ == '__main__': 

    def web_scraper_lego():
        #search_term = input('I would like to search for... ')
        search_term = ''
        scraper = AllTimeScraper('https://8wires.eu.teamwork.com/#/everything/time', search_term)
        scraper.scraping_now()
        scraper.quit()
    web_scraper_lego()
# %%
