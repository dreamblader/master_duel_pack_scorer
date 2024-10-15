from models.secret_banner_data import SecretBannerData
from models.secret_pack_data import SecretPackData
from models.card_data import CardData
from bs4 import BeautifulSoup
import logging
import datetime


def get_banners(html_source:str) -> list[SecretBannerData]:
    banner_list = []
    content = BeautifulSoup(html_source, 'html.parser')
    banners_html = content.findAll("div", class_="column is-6-desktop is-6-tablet is-12-mobile")

    for banner_html in banners_html:
        banner_name = banner_html.find('p').decode_contents()
        banner_link = banner_html.find('a', role="button")['href']
        banner_date = banner_html.find('span', slot="customSubtitle").decode_contents()
        banner_item = SecretBannerData(banner_name, banner_link, getDate(banner_date))
        logging.info(banner_item)
        banner_list.append(banner_item)
    
    return banner_list


def get_secret_pack(html_source:str, banner:SecretBannerData) -> SecretPackData:
    secret_pack = SecretPackData(banner.name, banner.date)
    content = BeautifulSoup(html_source, 'html.parser')
    cards_html = content.findAll("a", class_="image-wrapper")

    for card_html in cards_html:
        card_href = card_html['href']
        name = card_href.replace("/cards/", "").replace("%20", " ")
        card = CardData(name)
        logging.info(f"Adding card \"{name}\" in {secret_pack.name}")
        secret_pack.add_card(card)
    
    return secret_pack


def get_json(html_source:str):
    pass #TODO


def getDate(date_str:str):
    return datetime.datetime.strptime(date_str, "Released on %B %dth, %Y")