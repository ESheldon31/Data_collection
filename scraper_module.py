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
        self.id_list = []
        self.img_list = []
        self.info = {}
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

    def get_list_links(self, XPATH_container, XPATH_search_results):
        try: 
            search_list = self.container_to_list(XPATH_container, XPATH_search_results)
            self.link_list = []
            for result in search_list:
                link = self.get_link(result, 'a', 'href')
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
        individual_img_list = []
        try:
            main_image = self.driver.find_element(By.XPATH, XPATH_main_image)
            main_image_link = self.get_link(main_image, 'img', 'src')
            individual_img_list.append(main_image_link)
            
            thumbnail_list = self.container_to_list(XPATH_thumbnail_container, XPATH_thumbnails)
            for thumbnail in thumbnail_list:
                thumbnail_link = self.get_link(thumbnail, 'img', 'src')
                individual_img_list.append(thumbnail_link)
            self.img_list.append(individual_img_list)  
        
        except NoSuchElementException:
            individual_img_list.append('N/A')
            self.img_list.append(individual_img_list)


    def container_to_list(self, XPATH_container, XPATH_items_in_container):
        container = self.driver.find_element(By.XPATH, XPATH_container)
        list_items = container.find_elements(By.XPATH, XPATH_items_in_container)
        return list_items
   
    def get_link(self, element, tag_name, attribute_name):
        tag = element.find_element(By.TAG_NAME, tag_name)
        link = tag.get_attribute(attribute_name)
        return link

    def try_append(self, list_to_append_to, items_to_append):
        try:
            list_to_append_to.append(items_to_append)
        except:
            list_to_append_to.append('N/A')

    # def create_uuid(self):
    #     UUID = str(uuid.uuid4())
    #     self.uuid_list.append(UUID)
    
    @staticmethod
    def create_uuid():
        UUID = str(uuid.uuid4())
        return UUID

    def get_html(self, url):
        r = requests.get(url)
        return r

    def get_html_and_java(self):
        soup = bs(self.driver.page_source, 'html.parser')
        return soup

    def find_in_html(self, url, tag, attribute, attribute_name):
        r = self.get_html(url)
        soup = bs(r.text, 'html.parser')
        if attribute == None:
            element = soup.find(tag).text
        else:
            element = soup.find(tag, {attribute: attribute_name}).text
        return element

    def find_all_in_html(self, tag, attribute, attribute_name):
        soup = self.get_html_and_java()
        elements = soup.findAll(tag, {attribute: attribute_name})
        return elements

    def download_raw_data(self, path='.', file_name='raw_data'):
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
