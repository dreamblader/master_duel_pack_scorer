from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import pandas as pd
import datetime

from models.secret_banner_data import SecretBannerData
import web_elements
import var


#brave_path = "/home/gm3/.local/share/flatpak/exports/bin/com.brave.Browser"
#"/home/gm3/.local/share/flatpak/app/com.brave.Browser/x86_64/stable/8796334fbb4a98f635fadc617d67fe389c86dec73d16f839eeb7f29bb792d14c"


ygo_pro_api = "https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Dark Magician"


def init():
    global driver
    driver = start_webdriver()
    driver.get(web_elements.master_duel_meta_url+web_elements.secret_pack_endpoint)
    load_all_page()
    banners = get_banners(driver.page_source)   


def start_webdriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=chrome_options)


def load_all_page():
    load_button = get_load_button()

    while load_button is not None:
        load_button.click()
        load_button = get_load_button()
        

def get_load_button():
    try:
        wait = WebDriverWait(driver, var.WEB_DELAY)
        condition = expected_conditions.element_to_be_clickable(("css selector", web_elements.load_button_css_selector))
        return wait.until(condition)
    except:
        return None


def get_banners(html_source):
    banner_list = []
    content = BeautifulSoup(html_source, 'html.parser')
    banners_html = content.findAll("div", class_="column is-6-desktop is-6-tablet is-12-mobile")

    for banner_html in banners_html:
        banner_name = banner_html.find('p').decode_contents()
        banner_link = banner_html.find('a', role="button")['href']
        banner_date = banner_html.find('span', slot="customSubtitle").decode_contents()
        banner_item = SecretBannerData(banner_name, banner_link, getDate(banner_date))
        banner_list.append(banner_item)
    
    return banner_list


def getDate(date_str):
    return datetime.datetime.strptime(date_str, "Released on %B %dth, %Y")