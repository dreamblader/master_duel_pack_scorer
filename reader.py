from models.secret_banner_data import SecretBannerData
from models.secret_pack_data import SecretPackData
from models.card_data import CardData
from bs4 import BeautifulSoup
from fetcher import Fetcher
from scrapper import Scrapper
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
    cards_href = scrapper.get_detailed_secret_pack_source(banner.link)
    secret_pack = SecretPackData(banner.name, banner.date)

    for card_href in cards_href:
        name = card_href.replace("https://www.masterduelmeta.com/cards/", "").replace("%20", " ")
        card: CardData = CardData(name)
        logging.info(f"Adding card \"{name}\" in {secret_pack.name}")
        fetcher.fetch_card(scrapper, card)
        secret_pack.add_card(card)
        print("TEST -", card.name, card.type, card.rarity, card.tcg_date, card.ocg_date)
    
    return secret_pack


def getDate(date_str:str):
    return datetime.datetime.strptime(date_str, "Released on %B %dth, %Y").date()