from models.secret_banner_data import SecretBannerData
from bs4 import BeautifulSoup
import logging
import datetime


def get_banners(html_source) -> list[SecretBannerData]:
    banner_list = []
    content = BeautifulSoup(html_source, 'html.parser')
    banners_html = content.findAll("div", class_="column is-6-desktop is-6-tablet is-12-mobile")

    for banner_html in banners_html:
        banner_name = banner_html.find('p').decode_contents()
        banner_link = banner_html.find('a', role="button")['href']
        banner_date = banner_html.find('span', slot="customSubtitle").decode_contents()
        banner_item = SecretBannerData(banner_name, banner_link, getDate(banner_date))
        logging.debug(banner_item)
        banner_list.append(banner_item)
    
    return banner_list


def getDate(date_str):
    return datetime.datetime.strptime(date_str, "Released on %B %dth, %Y")