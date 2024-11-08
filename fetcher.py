import sqlite3
import json
import time
import logging
import urllib.parse
import web_elements
import urllib
from datetime import date
from scrapper import Scrapper
from models.card_data import CardData

"""
YGO PRO API NOTE:
Rate Limiting on the API is enabled. 
The rate limit is 20 requests per 1 second. 
If you exceed this, you are blocked from accessing the API for 1 hour. 
We will monitor this rate limit for now and adjust accordingly.
"""

class Fetcher():

    def __init__(self):
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


    def fetch_card(self, scrapper:Scrapper, card:CardData):
        start_req = time.perf_counter()
        db_data = self.__fetch_from_db(card.name)
        
        if db_data == None:
            self.fetch_count += 1
            logging.info(f"\"{card.name}\" NOT FOUND in local database")
            api_json = self.__fetch_from_api(scrapper, card.name)
            api_data = api_json["data"][0]
            info = api_data["misc_info"][0]
            card.type = api_data["type"]
            card.rarity = info.get("md_rarity", "N/A")
            card.set_dates(info.get("ocg_date", date.today().strftime("%Y-%m-%d")),
                            info.get("tcg_date", date.today().strftime("%Y-%m-%d")))
            self.key_warning("md_rarity", info)
            self.key_warning("ocg_date", info)
            self.key_warning("tcg_date", info)
            self.__save_in_db(card)
        else:
            card.type = db_data[1]
            card.rarity = db_data[2]
            card.set_dates(db_data[4], db_data[3])
        
        end_req = time.perf_counter()
        self.api_time_consumed += end_req - start_req
        
        if self.fetch_count == self.max_api_fetch:
            self.fetch_count = 0
            
            if self.api_time_consumed < 1:
                logging.warning(f"Number of API fetch passed 20 and time {self.api_time_consumed} is less than 1 second...")
                logging.warning(f"Waiting {1-self.api_time_consumed} to resume operations")
                time.sleep(1-self.api_time_consumed)
            
            self.api_time_consumed = 0


    def key_warning(self, key:str, dictionay:dict):
        if key not in dictionay.keys():
                logging.warning(f"Value {key} not found in API. Need to check in another source and UPDATE the Database")


    def __fetch_from_db(self, name:str):
        logging.info(f"Fetching \"{name}\" in local database")
        query = "SELECT * FROM \"Cards\" WHERE NAME = ?"
        params = [name]
        response = self.cursor.execute(query, params)
        return response.fetchone()


    def __fetch_from_api(self, scrapper:Scrapper, name:str):
        logging.info(f"Fetching \"{name}\" from YGOPRO API")
        endpoint = web_elements.ygo_pro_api_endpoint+urllib.parse.urlencode(name) 
        json_str = scrapper.get_api_json(endpoint)
        return json.loads(json_str)


    def __save_in_db(self, card:CardData):
        logging.info(f"Saving [{card}] in Database")
        query = """INSERT OR REPLACE INTO \"Cards\" (NAME, TYPE, RARITY, TCG_DATE, OCG_DATE, TCG_SCORE, OCG_SCORE) 
                VALUES (?, ?, ?, ?, ?, ?, ?); """
        params = [card.name, card.type, card.rarity, card.tcg_date, card.ocg_date, card.tcg_score, card.ocg_score]
        self.cursor.execute(query, params)
        self.connnect.commit()