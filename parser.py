from typing import Any
import urllib.parse
from models.secret_banner_data import SecretBannerData
from models.secret_pack_data import SecretPackData
from models.card_data import CardData
from bs4 import BeautifulSoup
import utils
import urllib
import logging


def html_to_SecretBannerData_list(html_source:str) -> list[SecretBannerData]:
    banner_list = []
    content = BeautifulSoup(html_source, 'html.parser')
    banners_html = content.findAll("div", class_="column is-6-desktop is-6-tablet is-12-mobile")

    for banner_html in banners_html:
        banner_name = banner_html.find('p').decode_contents()
        banner_link = banner_html.find('a', role="button")['href']
        banner_date = banner_html.find('span', slot="customSubtitle").decode_contents()
        banner_item = SecretBannerData(banner_name, banner_link, utils.getDate(banner_date))
        logging.info(banner_item)
        banner_list.append(banner_item)
    
    return banner_list


def html_to_cards_names(html_source:str) -> SecretPackData:
    content = BeautifulSoup(html_source, 'html.parser')
    cards_html = content.findAll("a", class_="image-wrapper")
    cards_name = []

    for card_html in cards_html:
        card_href = card_html['href']
        name = fix_mistranslation(urllib.parse.unquote(card_href.replace("/cards/", "")))
        cards_name.append(name)
    
    return cards_name


def konami_db_html_to_date(html_source:str) -> str:
    content = BeautifulSoup(html_source, 'html.parser')
    return content.find("div", class_="time").decode_contents().strip()


def add_api_data_to_card(api_data:dict, card:CardData) -> list[str]:
    info = api_data["misc_info"][0]
    card.type = api_data["type"]
    card.rarity = info.get("md_rarity", "N/A")
    card.konami_id = info.get("konami_id", -1)
    key_warning("md_rarity", info)
    ocg_date = "" if key_warning("ocg_date", info) else info["ocg_date"]
    tcg_date = "" if key_warning("tcg_date", info) else info["tcg_date"]
    return [ocg_date, tcg_date]


def add_db_data_to_card(db_data: Any, card: CardData):
    card.type = db_data[1]
    card.rarity = db_data[2]
    card.set_dates(db_data[4], db_data[3])


def key_warning(key:str, dictionay:dict) -> bool:
    if key not in dictionay.keys():
        logging.warning(f"Value {key} not found in API. Need to check in another source and UPDATE the Database")
        return True
    return False


def fix_mistranslation(name: str) -> str:
    match name:
        case "Flametongue the Burning Blade":
            return "Flametongue the Blazing Magical Blade"
        case _:
            return name