import urllib.parse
from models.secret_banner_data import SecretBannerData
from models.secret_pack_data import SecretPackData
from models.card_data import CardData
from bs4 import BeautifulSoup
from fetcher import Fetcher
from scrapper import Scrapper
import re
import urllib
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


def get_secret_pack(scrapper: Scrapper, banner:SecretBannerData) -> SecretPackData:
    fetcher = Fetcher()
    #TODO refactor create secretPackData outside and pass it, grab html source outside and pass it
    html_source = scrapper.get_detailed_secret_pack_source(banner.link)
    secret_pack = SecretPackData(banner.name, banner.date)

    content = BeautifulSoup(html_source, 'html.parser')
    cards_html = content.findAll("a", class_="image-wrapper")


    for card_html in cards_html:
        card_href = card_html['href']
        name = urllib.parse.unquote(card_href.replace("/cards/", ""))
        card: CardData = CardData(name)
        logging.info(f"Adding card \"{name}\" in {secret_pack.name}")
        fetcher.fetch_card(scrapper, card)
        secret_pack.add_card(card)
    
    secret_pack.calculate_score()
    
    return secret_pack


def get_date_in_konami_db(html_source:str) -> str:
    content = BeautifulSoup(html_source, 'html.parser')
    return content.find("div", class_="time").decode_contents()


def getDate(date_str:str):
    return datetime.datetime.strptime(date_str, "Released on %B %dth, %Y").date()


def clean_characters(s:str) -> str:
    return re.sub("/“|”/g", "\"", s)