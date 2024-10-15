import sqlite3
import json
import time
import web_elements
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
                        "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
                        "NAME" TEXT,
                        "TYPE" TEXT,
                        "TCG_DATE" TEXT,
                        "OCG_DATE" TEXT
                        );"""
        self.cursor.execute(create_query)


    def fetch_card(self, scrapper:Scrapper, card:CardData):
        start_req = time.perf_conter()
        db_data = self.__fetch_from_db(card.name)
        
        if db_data == None:
            self.__fetch_from_api(scrapper, card.name)
            self.fetch_count += 1
        else:
            print("DB:", db_data)
        
        end_req = time.perf_conter()
        self.api_time_consumed += end_req - start_req
        
        if self.fetch_count == self.max_api_fetch:
            self.fetch_count = 0
            if self.api_time_consumed < 1:
                time.sleep(1-self.api_time_consumed)

        


    def __fetch_from_db(self, name:str):
        query = f"SELECT * FROM \"Cards\" WHERE NAME = {name}"
        response = self.cursor.execute(query)
        return response.fetchone()


    def __fetch_from_api(self, scrapper:Scrapper, name:str):
        endpoint = web_elements.ygo_pro_api_endpoint+name
        content = scrapper.get_url(endpoint) #TODO
        pass