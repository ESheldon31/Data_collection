#%%
import dataclasses
#import selenium
import os
import json
import csv
import uuid
import urllib
import requests
import time
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
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
from bs4 import BeautifulSoup as bs
from abc import ABC, abstractmethod

#import pandas as pd
from pathlib import Path
from Project.Base_class.data_template import Data

# ToDo: add decorator file to elegantly handle errors
# ToDo: add details of public methods for class
# ToDo: finish docstrings for methods
# ToDo: add type hinting

def no_element_exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except NoSuchElementException:
            print(f'{func.__name__} couldn\'t find the element. Check your XPATH.')
    return wrapper

'''
This module contains the scraper base class and its methods.

'''

class Scraper:
    '''
    A class that contains generalised methods for scraping any website.
    
    ...
    
    Attributes 
    --------------
    
    url : str
        the starting url of the website you would like to scrape
    search_term : str
        the item you want to search for
    driver : the Selenium Chrome webdriver that automatically navegates the webpage

    Methods
    --------------

    # ToDo: finish
    '''




    def __init__(self, url, search_term, headless=False):
        ''' 
        Constructs all the necessary attributes

        Parameters
        -------------
        url : str
            the starting url of the website you would like to scrape
        search_term : str
            the item you want to search for
        headless : bool
            sets the webdrive to run in headless mode. Default = False

        '''
        options = Options()
        if headless:
            options.add_argument('--headless')
            self.driver = Chrome(ChromeDriverManager().install(), options=options)
        else:
            self.driver = Chrome(ChromeDriverManager().install())
        self.url = url
        self.search_term = search_term.upper()
        self.driver.get(self.url)
   
    def _open_url(self, url):
        '''
        opens the webpage for the url passed as a parameter
        
        Parameters
        -------------
        url : str
            url of the webpage to be opened

        '''
        self.driver.get(url)

    # @no_element_exception_handler
    # def search(self, XPATH, search_term):
    #     search_bar = self.driver.find_element(By.XPATH, XPATH)
    #     search_bar.click()
    #     search_bar.send_keys(search_term)
    #     search_bar.send_keys(u'\ue007')
    
    @no_element_exception_handler
    def _search(self, XPATH):
        
        search_bar = self.driver.find_element(By.XPATH, XPATH)
        search_bar.click()
        search_bar.send_keys(self.search_term)
        search_bar.send_keys(u'\ue007')

    def _click_button(self, XPATH):
        ''''''
        button = self.driver.find_element(By.XPATH, XPATH)
        button.click()

    def _wait_for(self, XPATH, click=True, delay=10):
        try:    
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, XPATH)))
            if click == True:
                self._click_button(XPATH)
        except TimeoutException:
            pass

    def _scroll_up_top(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollTop)")

    def _scroll_down_bottom(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    @staticmethod
    def _create_empty_dataclass():
        pass

    @no_element_exception_handler
    def _accept_cookies(self, frame_id, XPATH):
        if frame_id!=None:
            self._switch_frame(frame_id)
        else: pass
        self._click_button(XPATH)

    def _switch_frame(self, frame_id):
        self._wait_for(frame_id)
        self.driver.switchTo().frame(frame_id)
   
    def _close_pop_up(self, XPATH):
        self._wait_for(XPATH)

    def quit(self):
        self.driver.quit()

    def _next_page(self, url):
        self._open_url(url)

    def _see_more(self, XPATH):
        self._scroll_down_bottom()
        self._click_button(XPATH)
    
    def _infinite_scroll(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self._scroll_down_bottom()
            time.sleep(3)   
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def _get_list_links(self, XPATH_container, XPATH_search_results):
        try: 
            search_list = self._container_to_list(XPATH_container, XPATH_search_results)
            link_list = []
            for result in search_list:
                link = self._get_link(result, 'a', 'href')
                link_list.append(link)
            return link_list

        except NoSuchElementException:
            print('No results found. Try another search term.')
            self._restart_search()

    def _restart_search(self):
        self.driver.get(self.url)
        search_term = input('I would like to search for... ')
        self.search_term = search_term.upper()
        self._search()

    def _get_img_links(self, XPATH_main_image, XPATH_thumbnail_container, XPATH_thumbnails):
        individual_img_list = []
        img_list = []
        try:
            main_image = self.driver.find_element(By.XPATH, XPATH_main_image)
            main_image_link = self._get_link(main_image, 'img', 'src')
            individual_img_list.append(main_image_link)
            if XPATH_thumbnail_container != None:
                thumbnail_list = self._container_to_list(XPATH_thumbnail_container, XPATH_thumbnails)
                for thumbnail in thumbnail_list:
                    thumbnail_link = self._get_link(thumbnail, 'img', 'src')
                    individual_img_list.append(thumbnail_link)
                img_list.append(individual_img_list)  
        except NoSuchElementException:
            individual_img_list.append('N/A')
            img_list.append(individual_img_list)
        return img_list

    #@no_element_exception_handler
    def _container_to_list(self, XPATH_container: str, XPATH_items_in_container: str) -> str:
        container = self.driver.find_element(By.XPATH, XPATH_container)
        list_items = container.find_elements(By.XPATH, XPATH_items_in_container)
        return list_items
   
    def _get_link(self, element, tag_name, attribute_name):
        tag = element.find_element(By.TAG_NAME, tag_name)
        link = tag.get_attribute(attribute_name)
        return link

    @staticmethod
    def _create_uuid():
        UUID = str(uuid.uuid4())
        return UUID

    def _get_html(self, url):
        r = requests.get(url)
        return r

    def _get_html_and_java(self):
        soup = bs(self.driver.page_source, 'html.parser')
        return soup

    def _find_in_html(self, url, tag, attribute, attribute_name):
        r = self._get_html(url)
        soup = bs(r.text, 'html.parser')
        if attribute == None:
            element = soup.find(tag).text
        else:
            element = soup.find(tag, {attribute: attribute_name}).text
        return element

    def _find_all_in_html(self, tag, attribute, attribute_name):
        soup = self._get_html_and_java()
        elements = soup.findAll(tag, {attribute: attribute_name})
        return elements

    # def download_raw_data(self, path='.', file_name='raw_data'):
    #     if not os.path.exists(f'{path}/{file_name}'):
    #         os.makedirs(f'{path}/{file_name}')
    #     with open (f'{path}/{file_name}/data.json', 'w') as f:
    #         json.dump(self.info, f, indent="")

    @staticmethod
    def _download_raw_data(data_class, path='.', file_name='raw_data'):
        if not os.path.exists(f'{path}/{file_name}'):
            os.makedirs(f'{path}/{file_name}')
        with open (f'{path}/{file_name}/data.json', 'w') as f:
            data_class = dataclasses.asdict(data_class)
            #print(type(data_class))
            json.dump(data_class, f)

    def _download_images(self, img_list, path='.'):
        if not os.path.exists(f'{path}/{self.search_term}'):
            os.makedirs(f'{path}/{self.search_term}')

        for i, lst in enumerate(img_list):
            for j, img in enumerate(lst):
                urllib.request.urlretrieve(img, f'{path}/{self.search_term}/{self.search_term}{i}.{j}.webp')




# %%
