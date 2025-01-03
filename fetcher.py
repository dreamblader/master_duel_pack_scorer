import sqlite3
import json
import time
import logging
import urllib.parse
import web_elements
import urllib
import parser
import utils
from datetime import date
from scrapper import Scrapper
from models.card_data import CardData
from models.enums import DateRuleSet
from models.secret_banner_data import SecretBannerData
from models.secret_pack_data import SecretPackData

"""
YGO PRO API NOTE:
Rate Limiting on the API is enabled. 
The rate limit is 20 requests per 1 second. 
If you exceed this, you are blocked from accessing the API for 1 hour. 
We will monitor this rate limit for now and adjust accordingly.
"""

class Fetcher():

    def __init__(self, scrapper:Scrapper):
        self.scrapper = scrapper
        self.max_api_fetch = 20
        self.api_time_consumed = 0
        self.fetch_count = 0
        self.connect_db()


    def connect_db(self):
        self.connnect = sqlite3.connect("cards.db")
        self.cursor = self.connnect.cursor()
        create_query = """CREATE TABLE IF NOT EXISTS "Cards"(
                        "NAME" TEXT PRIMARY KEY,
                        "TYPE" TEXT,
                        "RARITY" TEXT,
                        "TCG_DATE" TEXT,
                        "OCG_DATE" TEXT,
                        "TCG_SCORE" INTEGER,
                        "OCG_SCORE" INTEGER
                        );"""
        self.cursor.execute(create_query)


    def fetch_secret_packs(self) -> list[SecretPackData]:
        banners = parser.html_to_SecretBannerData_list(self.scrapper.get_secrets_packs_source())
        return self.fetch_from_banners(banners)


    def fetch_from_banners(self, banners):
        secret_packs = []
        retry_list = []
        count = 1
        
        print(f"Pack Progress: 0/{len(banners)}")
        for banner in banners:
            try:
                pack: SecretPackData = SecretPackData(banner.name, banner.date)
                cards = parser.html_to_cards_names(self.scrapper.get_detailed_secret_pack_source(banner.link))
                pack.cards = self.fetch_cards(cards)
                pack.calculate_score()
                logging.info(f"Adding {pack}")
                secret_packs.append(pack)
                print(f"Pack Progress: {count}/{len(banners)}")
                count+=1
            except KeyboardInterrupt:
                raise Exception("Kill Command")
            except:
                logging.warning(f"Error related to Banner[{banner.name}], sending it to retry list")
                logging.exception("Stacktrace:")
                retry_list.append(banner)
            
        if len(retry_list) > 0:
            secret_packs.extend(self.fetch_from_banners(retry_list))
        
        return secret_packs


    def fetch_cards(self, cards:list[str]) -> list[CardData]:
        cards = []
        for card_name in cards:
            cards.append(self.fetch_card(card_name))
        return cards


    def fetch_card(self, card_name:str) -> CardData:
        card: CardData = CardData(card_name)
        start_req = time.perf_counter()
        db_data = self.__fetch_from_db(card.name)
        
        #TODO add DB_DATA and API Data to the Parser Module
        if db_data == None:
            self.fetch_count += 1
            logging.info(f"\"{card.name}\" NOT FOUND in local database")
            api_json = self.__fetch_from_api(card.name)
            api_data = api_json["data"][0]
            info = api_data["misc_info"][0]
            card.type = api_data["type"]
            card.rarity = info.get("md_rarity", "N/A")
            self.key_warning("md_rarity", info)
            konami_id = info.get("konami_id", -1)
            ocg_date = self.__fetch_from_ygo_db(konami_id, DateRuleSet.OCG) if self.key_warning("ocg_date", info) else info["ocg_date"]
            tcg_date = self.__fetch_from_ygo_db(konami_id, DateRuleSet.TCG) if self.key_warning("tcg_date", info) else info["tcg_date"]
            card.set_dates(ocg_date, tcg_date)
            self.__save_in_db(card)
        else:
            card.type = db_data[1]
            card.rarity = db_data[2]
            card.set_dates(db_data[4], db_data[3])
        
        end_req = time.perf_counter()
        self.api_time_consumed += end_req - start_req
        
        if self.fetch_count == self.max_api_fetch:
            self.fetch_count = 0
            logging.info(f"Number of API fetchs passed 20 request in {self.api_time_consumed} seconds...")
            
            if self.api_time_consumed < 1:
                logging.warning(f"Waiting {1-self.api_time_consumed} to resume operations")
                time.sleep(1-self.api_time_consumed)
            
            self.api_time_consumed = 0
        
        return card


    def key_warning(self, key:str, dictionay:dict) -> bool:
        #Add a Console Print Warning to check logs for current card
        if key not in dictionay.keys():
            logging.warning(f"Value {key} not found in API. Need to check in another source and UPDATE the Database")
            return True
        return False


    def __fetch_from_db(self, name:str):
        logging.info(f"Fetching \"{name}\" in local database")
        query = "SELECT * FROM \"Cards\" WHERE NAME = ?"
        params = [name]
        response = self.cursor.execute(query, params)
        return response.fetchone()


    def __fetch_from_api(self, name:str):
        logging.info(f"Fetching \"{name}\" from YGOPRO API")
        clean_name = utils.clean_characters(name)
        endpoint = web_elements.ygo_pro_api_endpoint+urllib.parse.quote(clean_name) 
        json_str = self.scrapper.get_api_json(endpoint)
        return json.loads(json_str)


    def __fetch_from_ygo_db(self, id:str, rule_set:DateRuleSet) -> str:
        try:
            if id == -1:
               raise Exception("No Konami ID Found") 
            logging.info(f"Checking YGO DB for {id} because it missed the above attribute")
            locale = web_elements.ocg_locale if rule_set == DateRuleSet.OCG else web_elements.tcg_locale
            endpoint = web_elements.ygo_db_endpoint+str(id)+locale
            return parser.konami_db_html_to_date(self.scrapper.get_missing_time_from_ygo_db(endpoint))
        except:
            logging.exception("Exception -")
            logging.warning(f"{id} not found for {rule_set} forcing #TODAY# as release date for this card")
            return date.today().strftime("%Y-%m-%d")


    def __save_in_db(self, card:CardData):
        logging.info(f"Saving [{card}] in Database")
        query = """INSERT OR REPLACE INTO \"Cards\" (NAME, TYPE, RARITY, TCG_DATE, OCG_DATE, TCG_SCORE, OCG_SCORE) 
                VALUES (?, ?, ?, ?, ?, ?, ?); """
        params = [card.name, card.type, card.rarity, card.tcg_date, card.ocg_date, card.tcg_score, card.ocg_score]
        self.cursor.execute(query, params)
        self.connnect.commit()