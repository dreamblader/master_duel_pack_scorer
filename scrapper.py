from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import logging
import web_elements
import var


#brave_path = "/home/gm3/.local/share/flatpak/exports/bin/com.brave.Browser"
#"/home/gm3/.local/share/flatpak/app/com.brave.Browser/x86_64/stable/8796334fbb4a98f635fadc617d67fe389c86dec73d16f839eeb7f29bb792d14c"


ygo_pro_api = "https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Dark Magician"

class Scrapper():

    def __init__(self):
        self.driver = self.start_webdriver()
        

    def start_webdriver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        return webdriver.Chrome(options=chrome_options)
    
    
    def get_secret_packs_source(self) -> str:
        self.driver.get(web_elements.master_duel_meta_url+web_elements.secret_pack_endpoint)
        logging.info("Loading Master Duel Meta Secret Packs Page...")
        self.load_all_page()
        return self.driver.page_source


    def load_all_page(self):
       load_button = self.get_load_button()

       while load_button is not None:
            load_button.click()
            load_button = self.wait_load_button(load_button)
    

    def get_load_button(self) -> WebElement:
        try:
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                if button.text == web_elements.load_button_text:
                    return button
            raise Exception("Text \"{}\" not found in current button selection".format(web_elements.load_button_text))
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