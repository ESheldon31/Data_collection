#%%
import selenium
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
import requests
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common import service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
#from time import sleep, time
import time
from bs4 import BeautifulSoup as bs
#import pandas as pd
from pathlib import Path
import os
import json
import csv
import uuid
import urllib


'''
This module contains the scraper base class and its methods.
'''

class Scraper:
    def __init__(self, url, search_term, headless=False):
        options = Options()
        if headless:
            options.add_argument('--headless')
            self.driver = Chrome(ChromeDriverManager().install(), options=options)
        else:
            self.driver = Chrome(ChromeDriverManager().install())
        self.url = url
        self.search_term = search_term.upper()
        self.uuid_list = []
        self.driver.get(self.url)
   
    def open_url(self, url):
        self.driver.get(url)
    
    def search(self, XPATH):
        search_bar = self.driver.find_element(By.XPATH, XPATH)
        search_bar.click()
        search_bar.send_keys(self.search_term)
        search_bar.send_keys(u'\ue007')

    def click_button(self, XPATH):
        button = self.driver.find_element(By.XPATH, XPATH)
        button.click()

    def scroll_up_top(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollTop)")

    def scroll_down_bottom(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    def accept_cookies(self, frame_id, XPATH):
        try:
            if frame_id!=None:
                self.switch_frame(frame_id)
            else: pass
            self.wait_for(XPATH)
            self.click_button(XPATH)
        except NoSuchElementException:
            pass

    def wait_for(self, XPATH, delay = 10):
        try:    
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, XPATH)))
        except TimeoutException:
            print('Loading took too long. Timeout occurred.')

    def switch_frame(self, frame_id):
        self.wait_for(frame_id)
        self.driver.switchTo().frame(frame_id)

    def quit(self):
        self.driver.quit()

    def next_page(self, url):
        self.open_url(url)

    def see_more(self, XPATH):
        self.scroll_down_bottom()
        self.click_button(XPATH)
    
    def infinite_scroll(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.scroll_down_bottom()
            time.sleep(3)   
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def get_list_links(self, XPATH_container, XPATH_search_results, delay=10):
        try: 
            self.scroll_down_bottom()
            try:
                self.see_more('//*[@id="search-more"]/a')
                self.infinite_scroll()
                pass
            except NoSuchElementException:
                pass
            container = self.driver.find_element(By.XPATH, XPATH_container)
            search_list = container.find_elements(By.XPATH, XPATH_search_results)

            self.link_list = []

            for result in search_list:
                a_tag = result.find_element(By.TAG_NAME, 'a')
                link = a_tag.get_attribute('href')
                self.link_list.append(link)

        except NoSuchElementException:
            print('No results found. Try another search term.')
            self.restart_search()
    
    def restart_search(self):
        self.driver.get(self.url)
        search_term = input('I would like to search for... ')
        self.search_term = search_term.upper()
        self.search()

    def get_img_links(self, XPATH_main_image, XPATH_thumbnail_container, XPATH_thumbnails):
        self.img_list = []
        try:
            for link in self.link_list:
                self.open_url(link)
                individual_img_list = []
                main_image = self.driver.find_element(By.XPATH, XPATH_main_image)
                img_tag = main_image.find_element(By.TAG_NAME, 'img')
                img_link = img_tag.get_attribute('src')
                individual_img_list.append(img_link)
                thumbnail_container = self.driver.find_element(By.XPATH, XPATH_thumbnail_container)
                thumbnail_list = thumbnail_container.find_elements(By.XPATH, XPATH_thumbnails)
                for thumbnail in thumbnail_list:
                    img_tag = thumbnail.find_element(By.TAG_NAME, 'img')
                    thumbnail_link = img_tag.get_attribute('src')
                    individual_img_list.append(thumbnail_link)
                self.img_list.append(individual_img_list)  
        except NoSuchElementException:
            self.individual_img_list.append('N/A')
            self.img_list.append(self.individual_img_list)
            pass
   

    def create_uuid(self):
        UUID = str(uuid.uuid4())
        self.uuid_list.append(UUID)
    
    # def create_uuid(self, result_list):
        
    #     for i in range(len(result_list)):
    #         UUID = str(uuid.uuid4())
    #         self.uuid_list.append(UUID)

    def get_html(self, url):
        r = requests.get(url)
        self.soup = bs(r.text, 'html.parser')

    def find_in_html(self, tag, attribute, attribute_name):
        self.soup.find(tag, {attribute: attribute_name}).text


    def download_raw_data(self,path='.', file_name='raw_data'):
        if not os.path.exists(f'{path}/{file_name}'):
            os.makedirs(f'{path}/{file_name}')
        with open (f'{path}/{file_name}/data.json', 'w') as f:
            json.dump(self.info, f, indent="")


    def download_images(self, path='.'):
        if not os.path.exists(f'{path}/{self.search_term}'):
            os.makedirs(f'{path}/{self.search_term}')

        for i, lst in enumerate(self.img_list):
            for j, img in enumerate(lst):
                urllib.request.urlretrieve(img, f'{path}/{self.search_term}/{self.search_term}{i}.{j}.webp')




# %%
