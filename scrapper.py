from selenium import webdriver 
from bs4 import BeautifulSoup
import pandas as pd
import web_elements

#brave_path = "/home/gm3/.local/share/flatpak/exports/bin/com.brave.Browser"
#"/home/gm3/.local/share/flatpak/app/com.brave.Browser/x86_64/stable/8796334fbb4a98f635fadc617d67fe389c86dec73d16f839eeb7f29bb792d14c"

master_duel_meta_url = "https://www.masterduelmeta.com"
secret_pack_url = "/secret-packs"
ygo_pro_api = "https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Dark Magician"


def init():
    driver = start_webdriver()
    driver.get(master_duel_meta_url+secret_pack_url)
    load_all_page(driver)


def start_webdriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=chrome_options)


def load_all_page(driver):
    buttons = driver.find_elements("tag name", "button")
    load_button = buttons[len(buttons)-1]
    load_button.click()