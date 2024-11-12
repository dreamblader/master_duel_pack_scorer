from scrapper import Scrapper
from models.secret_banner_data import SecretBannerData
from models.secret_pack_data import SecretPackData
from datetime import datetime
import time
import logging
import reader
import writer


def main():
    #Look for logging config dictconfig to enable DEBUG and disable 3rd party debug logs
    start_time = time.perf_counter()
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_name = f"logs/{timestamp}_info.log"
    print("Running Scorer...")
    print(f"for more information check the generated {file_name} log file")
    logging.basicConfig(filename= file_name, level=logging.INFO)
    scrapper = Scrapper()
    banners = reader.get_banners(scrapper.get_secret_packs_source())
    secret_packs = search_banners(scrapper, banners)
    writer.generate_csv(secret_packs)
    end_time = start_time = time.perf_counter()
    print(f"Script finished with succes after {start_time-end_time} seconds...")
    #TODO check card in konami DB is missing ocg dates (use konami_id from YGO PRO)... 
    #FIXME Check why some cards are not in the api? Gigantic%20%E2%80%9CChampion%E2%80%9D%20Sargas???
    

def search_banners(scrapper: Scrapper, banners: list[SecretBannerData]) -> list[SecretPackData]:
    secret_packs = []
    retry_list = []
    
    for banner in banners:
        try:
            pack: SecretPackData = reader.get_secret_pack(scrapper, banner)
            logging.info(f"Adding {pack}")
            secret_packs.append(pack)
        except:
            logging.warning(f"Error related to Banner[{banner.name}], sending it to retry list")
            logging.exception("Stacktrace:")
            retry_list.append(banner)
    
    
    if len(retry_list) > 0:
        secret_packs.extend(search_banners(scrapper, retry_list))
    
    
    return secret_packs


if __name__ == "__main__":
    main()
    

#Banner example:
#INFO:root:Banner: Beloved Dolls(/articles/sets/beloved-dolls/)[19/01/2022]
#INFO:root:Banner: Blooming in Adversity(/articles/sets/blooming-in-adversity/)[19/01/2022]
