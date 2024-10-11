from scrapper import Scrapper
from models.secret_banner_data import SecretBannerData
import logging
import adapter


if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG) #need to find a way to disable Selenium debug log outputs
    scrapper = Scrapper()
    banners: SecretBannerData = adapter.get_banners(scrapper.get_secret_packs_source())
