from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

import logging
import web_elements
import var

from models.secret_banner_data import SecretBannerData


class Scrapper():

    def __init__(self):
        self.driver = self.start_webdriver()
        

    def start_webdriver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        return webdriver.Chrome(options=chrome_options)
    

    def get_url(self, url) -> str:
        logging.info(f"Entering URL: {url}")
        return self.driver.get(url)


    def get_api_json(self, url) -> str:
        self.get_url(url)
        json_wrapper:WebElement = self.driver.find_element(By.TAG_NAME, "pre")
        return json_wrapper.text

    
    def get_secret_packs_source(self) -> str:
        url = web_elements.master_duel_meta_url+web_elements.secret_pack_endpoint
        self.get_url(url)
        logging.info("Loading Master Duel Meta Secret Packs Page...")
        self.load_all_page()
        return self.driver.page_source
    

    def get_detailed_secret_pack_source(self, banner_link:str) -> str:
        url = web_elements.master_duel_meta_url+banner_link
        self.get_url(url)
        wait = WebDriverWait(self.driver, var.WEB_DELAY)
        condition = expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "a.image-wrapper"))
        wait.until(condition)
        
        return self.driver.page_source


    def load_all_page(self):
       load_button = self.__get_load_button()

       while load_button is not None:
            load_button.click()
            load_button = self.wait_load_button(load_button)
    

    def __get_load_button(self) -> WebElement:
        try:
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                if button.text == web_elements.load_button_text:
                    return button
            raise Exception(f"Text \"{web_elements.load_button_text}\" not found in current button selection")
        except Exception as error:
            logging.warning("Load button not found. Check web_elements.py for any deprecated selector")
            logging.error(error)

            

    def wait_load_button(self, load_button:WebElement) -> WebElement:
        try:
            wait = WebDriverWait(self.driver, var.WEB_DELAY)
            condition = expected_conditions.element_to_be_clickable(load_button)
            return wait.until(condition)
        except:
            return None