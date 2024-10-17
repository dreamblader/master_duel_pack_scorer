from scrapper import Scrapper
from fetcher import Fetcher
from models.secret_banner_data import SecretBannerData
from models.secret_pack_data import SecretPackData
import logging
import reader


def main():
    #Look for logging config dictconfig to enable DEBUG and disable 3rd party debug logs
    logging.basicConfig(level=logging.INFO)
    scrapper = Scrapper()
    banners = reader.get_banners(scrapper.get_secret_packs_source())
    secret_packs = search_banners(scrapper, banners)
    

def search_banners(scrapper: Scrapper, banners: list[SecretBannerData]) -> list[SecretPackData]:
    secret_packs = []
    for banner in banners:
        pack: SecretPackData = reader.get_secret_pack(scrapper, banner)
        logging.info(f"Adding {pack}")
        secret_packs.append(pack)
        break #TODO: Remove is for a singular test only
    return secret_packs


if __name__ == "__main__":
    main()
    

#Banner example:
#INFO:root:Banner: Beloved Dolls(/articles/sets/beloved-dolls/)[19/01/2022]
#INFO:root:Banner: Blooming in Adversity(/articles/sets/blooming-in-adversity/)[19/01/2022]
